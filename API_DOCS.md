# API Documentation

Base URL: `http://localhost:8000`

## Endpoints

### Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-12-12T13:40:00Z"
}
```

---

### Query Expert System

```http
POST /api/query
```

**Request Body:**
```json
{
  "query": "How do I fix audio dropouts in Cubase?",
  "context": {
    "version": "13",
    "os": "Windows 11"
  }
}
```

**Response:**
```json
{
  "answer": "Audio dropouts are typically caused by buffer size issues...",
  "confidence": 0.95,
  "sources": ["kb_audio_001", "kb_performance_003"],
  "suggestions": [
    "Increase buffer size to 512 or 1024 samples",
    "Disable unnecessary plugins",
    "Check ASIO driver settings"
  ],
  "related_topics": ["buffer_optimization", "asio_configuration"]
}
```

---

### Get Knowledge Base Entry

```http
GET /api/knowledge/{entry_id}
```

**Response:**
```json
{
  "id": "kb_audio_001",
  "title": "Audio Dropout Troubleshooting",
  "category": "performance",
  "content": "...",
  "tags": ["audio", "performance", "troubleshooting"],
  "last_updated": "2025-12-01"
}
```

---

### Search Knowledge Base

```http
GET /api/knowledge/search?q=audio&category=performance
```

**Query Parameters:**
- `q` (string, required): Search query
- `category` (string, optional): Filter by category
- `limit` (int, optional): Max results (default: 10)

**Response:**
```json
{
  "results": [
    {
      "id": "kb_audio_001",
      "title": "Audio Dropout Troubleshooting",
      "excerpt": "Audio dropouts are typically caused by...",
      "relevance": 0.92
    }
  ],
  "total": 1,
  "query": "audio"
}
```

---

### List Categories

```http
GET /api/categories
```

**Response:**
```json
{
  "categories": [
    {
      "id": "performance",
      "name": "Performance & Optimization",
      "count": 45
    },
    {
      "id": "audio",
      "name": "Audio Configuration",
      "count": 67
    }
  ]
}
```

---

### Submit Feedback

```http
POST /api/feedback
```

**Request Body:**
```json
{
  "query_id": "q_12345",
  "rating": 5,
  "comment": "Very helpful!",
  "helpful": true
}
```

**Response:**
```json
{
  "success": true,
  "message": "Feedback recorded"
}
```

---

## Error Responses

All endpoints return errors in this format:

```json
{
  "error": {
    "code": "INVALID_QUERY",
    "message": "Query cannot be empty",
    "details": {}
  }
}
```

**Common Error Codes:**
- `INVALID_QUERY` - Malformed or empty query
- `NOT_FOUND` - Resource not found
- `RATE_LIMIT` - Too many requests
- `INTERNAL_ERROR` - Server error

---

## Rate Limiting

- **Rate:** 100 requests per minute per IP
- **Headers:**
  - `X-RateLimit-Limit`: 100
  - `X-RateLimit-Remaining`: 95
  - `X-RateLimit-Reset`: 1702389600

---

## Authentication (Optional)

For production deployments, add API key:

```http
Authorization: Bearer YOUR_API_KEY
```

---

## WebSocket (Real-time)

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.send(JSON.stringify({
  type: 'query',
  data: { query: 'How to export audio?' }
}));

ws.onmessage = (event) => {
  const response = JSON.parse(event.data);
  console.log(response);
};
```

---

## SDK Examples

### Python

```python
import requests

response = requests.post('http://localhost:8000/api/query', json={
    'query': 'How to fix latency?',
    'context': {'version': '13'}
})

print(response.json())
```

### JavaScript

```javascript
const response = await fetch('http://localhost:8000/api/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'How to fix latency?',
    context: { version: '13' }
  })
});

const data = await response.json();
console.log(data);
```

---

## OpenAPI Spec

Full OpenAPI 3.0 specification available at:
```
http://localhost:8000/docs
```

Interactive API documentation (Swagger UI):
```
http://localhost:8000/redoc
```
