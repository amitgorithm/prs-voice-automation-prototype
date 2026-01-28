"""
PRS Automation System - Backend Server
Handles API calls to OpenAI GPT-4 Mini and serves the frontend
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
import logging
import traceback
import time
import hashlib

app = Flask(__name__)
CORS(app)

# Configure logging to output timestamps and level
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger('prs_server')

# # OpenAI API key (default embedded; override with env var OPENAI_API_KEY)
# DEFAULT_OPENAI_KEY = 'REPLACE_WITH_ENV_OPENAI_KEY_DEFAULT'
# OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', DEFAULT_OPENAI_KEY)
# OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-4o-mini')

# OpenAI configuration (prototype setup)
OPENAI_API_KEY = os.environ.get(
    'OPENAI_API_KEY',
    'REPLACE_WITH_ENV_OPENAI_KEY'  # fallback for prototype
)
OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-4o-mini')

# Simple in-memory cache for identical prompts to reduce latency on repeats
# cache: { key: (timestamp_seconds, response_text) }
_response_cache = {}
CACHE_TTL = int(os.environ.get('PRS_CACHE_TTL', '300'))  # seconds

def _cache_get(key):
    entry = _response_cache.get(key)
    if not entry:
        return None
    ts, val = entry
    if time.time() - ts > CACHE_TTL:
        try:
            del _response_cache[key]
        except KeyError:
            pass
        return None
    return val

def _cache_set(key, val):
    _response_cache[key] = (time.time(), val)

@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_from_directory('.', 'prs-voice-app.html')

@app.route('/api/score', methods=['POST'])
def score_response():
    """
    Score a patient response using OpenAI GPT-4 Mini
    """
    try:
        data = request.get_json(silent=True)
        logger.debug('Incoming /api/score request payload: %s', data)

        # Basic validation
        if not data:
            logger.warning('Bad request: empty JSON payload')
            return jsonify({'error': 'Bad Request', 'details': 'Expected JSON payload'}), 400

        if 'messages' not in data or not isinstance(data['messages'], list) or len(data['messages']) == 0:
            logger.warning('Bad request: missing messages field')
            return jsonify({'error': 'Bad Request', 'details': 'Missing messages array in payload'}), 400
        
        # Prepare input for Responses API: use a single string (system + user)
        model_input = (data.get('system', '') or '') + "\n\n" + (data.get('messages', [])[0].get('content', '') or '')
        logger.info('Calling OpenAI Responses API model=%s, input_len=%d', OPENAI_MODEL, len(model_input))

        # Check cache
        cache_key = hashlib.sha256((OPENAI_MODEL + '||' + model_input).encode('utf-8')).hexdigest()
        cached = _cache_get(cache_key)
        if cached is not None:
            logger.info('Cache hit for key %s (len %d)', cache_key[:8], len(cached))
            return jsonify({'content': [{'type': 'text', 'text': cached}]})

        try:
            response = requests.post(
                'https://api.openai.com/v1/responses',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {OPENAI_API_KEY}'
                },
                json={
                    'model': OPENAI_MODEL,
                    'input': model_input,
                    # 'temperature' removed because model may not support it
                    'max_output_tokens': 1000
                },
                timeout=60
            )

            # Raise for HTTP errors to handle uniformly
            response.raise_for_status()
        except requests.exceptions.RequestException as req_err:
            # Network-level or HTTP error
            logger.error('Request to OpenAI failed: %s', str(req_err))
            # If available, log upstream response body for debugging
            resp = getattr(req_err, 'response', None)
            if resp is not None:
                try:
                    logger.error('OpenAI returned status=%s body=%s', resp.status_code, resp.text)
                except Exception:
                    logger.debug('Could not read upstream response body', exc_info=True)

            logger.debug('Traceback:\n%s', traceback.format_exc())
            details = str(req_err)
            if resp is not None:
                details = f'status={resp.status_code} body={resp.text}'
            return jsonify({'error': 'Upstream API request failed', 'details': details}), 502

        # Parse Responses API output robustly
        try:
            openai_response = response.json()
        except ValueError as ve:
            logger.error('Failed to decode JSON from OpenAI response: %s', str(ve))
            logger.debug('OpenAI raw response text: %s', response.text if response is not None else None)
            return jsonify({'error': 'Invalid response from upstream API', 'details': 'Unable to parse JSON'}), 502
        result_text = ''

        # New Responses API returns an "output" list containing content blocks
        for out in openai_response.get('output', []):
            for chunk in out.get('content', []):
                # Try known content shapes
                if isinstance(chunk, dict):
                    # 'type': 'output_text' with 'text'
                    if chunk.get('type') == 'output_text' and 'text' in chunk:
                        result_text += chunk.get('text', '')
                    # older or alternate shapes
                    elif 'text' in chunk:
                        result_text += chunk.get('text', '')
                elif isinstance(chunk, str):
                    result_text += chunk

        # Fallbacks
        if not result_text:
            # try top-level "text" fields
            if 'text' in openai_response:
                result_text = openai_response['text']
            else:
                # try choices (compat)
                choices = openai_response.get('choices', [])
                if choices and isinstance(choices, list):
                    first = choices[0]
                    msg = first.get('message', {})
                    result_text = msg.get('content', '') if isinstance(msg, dict) else ''

        logger.info('Scoring result produced (%d chars)', len(result_text))
        # cache the result for subsequent identical prompts
        try:
            _cache_set(cache_key, result_text)
        except Exception:
            logger.debug('Failed to set cache', exc_info=True)

        return jsonify({'content': [{'type': 'text', 'text': result_text}]})
    
    except Exception as e:
        logger.exception('Unhandled exception in /api/score: %s', str(e))
        return jsonify({'error': 'Internal Server Error', 'details': 'An unexpected error occurred'}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    api_key_configured = OPENAI_API_KEY and OPENAI_API_KEY != DEFAULT_OPENAI_KEY
    return jsonify({
        'status': 'ok',
        'api_key_set': api_key_configured
    })

if __name__ == '__main__':
    print("=" * 60)
    print("PRS Automation System - Backend Server (OpenAI GPT-4 Mini)")
    print("=" * 60)
    
    # if OPENAI_API_KEY == DEFAULT_OPENAI_KEY or not OPENAI_API_KEY:
    #     logger.warning('\n⚠️  WARNING: OpenAI API key not set or using default placeholder!')
    #     logger.warning('Set your OpenAI API key: export OPENAI_API_KEY="sk-..."')
    # else:
    #     logger.info('✓ OpenAI API key configured')

    if not OPENAI_API_KEY:
        logger.warning('⚠️ OpenAI API key not set!')
    else:
        logger.info('✓ OpenAI API key configured')

    logger.info('Starting server...')
    logger.info('Open in browser: http://localhost:5003')

    try:
        app.run(host='0.0.0.0', port=5003)
        # app.run(host='0.0.0.0', port=5003, debug=True)
    except Exception:
        logger.exception('Server crashed while running')
