# API Documentation

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. In production, consider implementing API keys or OAuth2.

## Response Format

All API responses follow a consistent JSON format:

### Success Response
```json
{
  "data": { ... },
  "message": "Success",
  "status": "ok"
}
```

### Error Response
```json
{
  "error": "Error message",
  "status": "error",
  "code": 400
}
```

## Endpoints

### Health Check

#### GET /health

Check the health status of the API and model.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00Z",
  "model_loaded": true,
  "gpu_available": true,
  "cache_size": 150
}
```

**Status Codes:**
- `200` - Service is healthy
- `503` - Service unavailable

---

### Get Supported Languages

#### GET /languages

Retrieve the list of supported languages.

**Response:**
```json
{
  "en": "English",
  "de": "German",
  "fr": "French",
  "es": "Spanish",
  "it": "Italian",
  "pt": "Portuguese"
}
```

---

### Single Translation

#### POST /translate

Translate a single text from source language to target language.

**Request Body:**
```json
{
  "text": "Hello, how are you?",
  "target_language": "de",
  "source_language": "en",
  "max_length": 100,
  "temperature": 1.0,
  "beam_size": 1
}
```

**Parameters:**
- `text` (string, required): Text to translate (1-1000 characters)
- `target_language` (string, required): Target language code
- `source_language` (string, optional): Source language code (default: "en")
- `max_length` (integer, optional): Maximum output length (default: 100)
- `temperature` (float, optional): Sampling temperature (default: 1.0)
- `beam_size` (integer, optional): Beam search size (default: 1)

**Response:**
```json
{
  "translated_text": "Hallo, wie geht es dir?",
  "source_language": "en",
  "target_language": "de",
  "processing_time": 0.234,
  "confidence": 0.95
}
```

**Status Codes:**
- `200` - Translation successful
- `400` - Invalid request parameters
- `500` - Translation failed

---

### Batch Translation

#### POST /batch-translate

Translate multiple texts in a single request.

**Request Body:**
```json
{
  "texts": [
    "Hello, how are you?",
    "This is a test.",
    "Good morning!"
  ],
  "target_language": "de",
  "source_language": "en",
  "max_length": 100
}
```

**Parameters:**
- `texts` (array, required): List of texts to translate (max 100 items)
- `target_language` (string, required): Target language code
- `source_language` (string, optional): Source language code (default: "en")
- `max_length` (integer, optional): Maximum output length (default: 100)

**Response:**
```json
{
  "translations": [
    {
      "translated_text": "Hallo, wie geht es dir?",
      "source_language": "en",
      "target_language": "de",
      "processing_time": 0.234,
      "confidence": 0.95
    },
    {
      "translated_text": "Das ist ein Test.",
      "source_language": "en",
      "target_language": "de",
      "processing_time": 0.198,
      "confidence": 0.92
    },
    {
      "translated_text": "Guten Morgen!",
      "source_language": "en",
      "target_language": "de",
      "processing_time": 0.156,
      "confidence": 0.98
    }
  ],
  "total_processing_time": 0.588,
  "average_processing_time": 0.196
}
```

**Status Codes:**
- `200` - Batch translation successful
- `400` - Invalid request parameters
- `500` - Translation failed

---

### Model Information

#### GET /model/info

Get information about the loaded translation model.

**Response:**
```json
{
  "model_name": "Transformer NMT",
  "supported_languages": ["en", "de", "fr", "es", "it", "pt"],
  "model_size": 100000000,
  "is_loaded": true,
  "last_updated": "2024-01-01T12:00:00Z"
}
```

---

### Reload Model

#### POST /model/reload

Reload the translation model from a checkpoint.

**Request Body:**
```json
{
  "model_path": "/path/to/model.pt"
}
```

**Parameters:**
- `model_path` (string, optional): Path to model checkpoint

**Response:**
```json
{
  "message": "Model reloaded successfully"
}
```

**Status Codes:**
- `200` - Model reloaded successfully
- `500` - Model reload failed

---

### Clear Cache

#### DELETE /cache

Clear the translation cache.

**Response:**
```json
{
  "message": "Cache cleared successfully"
}
```

---

### Get Metrics

#### GET /metrics

Get API usage and performance metrics.

**Response:**
```json
{
  "total_translations": 1250,
  "cache_hit_rate": 0.85,
  "average_response_time": 0.5,
  "uptime": "24h"
}
```

## Error Handling

### Common Error Codes

- `400 Bad Request` - Invalid request parameters
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - Service temporarily unavailable

### Error Response Format

```json
{
  "error": "Detailed error message",
  "status": "error",
  "code": 400,
  "details": {
    "field": "specific field error"
  }
}
```

## Rate Limiting

Currently, no rate limiting is implemented. In production, consider implementing:

- Per-IP rate limiting
- Per-API-key rate limiting
- Burst protection
- DDoS protection

## Caching

The API implements caching for:

- Translation results
- Model predictions
- Language mappings

Cache TTL: 1 hour (configurable)

## Examples

### cURL Examples

#### Single Translation
```bash
curl -X POST "http://localhost:8000/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, world!",
    "target_language": "de",
    "source_language": "en"
  }'
```

#### Batch Translation
```bash
curl -X POST "http://localhost:8000/batch-translate" \
  -H "Content-Type: application/json" \
  -d '{
    "texts": ["Hello", "World"],
    "target_language": "fr"
  }'
```

### Python Examples

#### Using requests
```python
import requests

# Single translation
response = requests.post('http://localhost:8000/translate', json={
    'text': 'Hello, world!',
    'target_language': 'de',
    'source_language': 'en'
})
result = response.json()
print(result['translated_text'])

# Batch translation
response = requests.post('http://localhost:8000/batch-translate', json={
    'texts': ['Hello', 'World'],
    'target_language': 'fr'
})
results = response.json()
for translation in results['translations']:
    print(translation['translated_text'])
```

#### Using httpx (async)
```python
import httpx
import asyncio

async def translate_text():
    async with httpx.AsyncClient() as client:
        response = await client.post('http://localhost:8000/translate', json={
            'text': 'Hello, world!',
            'target_language': 'de'
        })
        return response.json()

result = asyncio.run(translate_text())
print(result['translated_text'])
```

### JavaScript Examples

#### Using fetch
```javascript
// Single translation
const response = await fetch('http://localhost:8000/translate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    text: 'Hello, world!',
    target_language: 'de',
    source_language: 'en'
  })
});

const result = await response.json();
console.log(result.translated_text);
```

## SDKs and Libraries

### Python SDK
```python
from translator_client import TranslatorClient

client = TranslatorClient('http://localhost:8000')

# Single translation
result = client.translate('Hello, world!', 'de')
print(result.translated_text)

# Batch translation
results = client.batch_translate(['Hello', 'World'], 'fr')
for result in results:
    print(result.translated_text)
```

### JavaScript SDK
```javascript
import { TranslatorClient } from 'translator-client';

const client = new TranslatorClient('http://localhost:8000');

// Single translation
const result = await client.translate('Hello, world!', 'de');
console.log(result.translated_text);

// Batch translation
const results = await client.batchTranslate(['Hello', 'World'], 'fr');
results.forEach(result => console.log(result.translated_text));
```

## Webhooks

Currently, webhooks are not implemented. Future versions may include:

- Translation completion notifications
- Model update notifications
- Error alerts
- Usage statistics

## API Versioning

The API uses URL-based versioning:

- Current version: v1 (default)
- Future versions: v2, v3, etc.

Example: `http://localhost:8000/v1/translate`

## OpenAPI Specification

The API provides an OpenAPI (Swagger) specification at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`



