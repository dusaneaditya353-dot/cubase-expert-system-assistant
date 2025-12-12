# Installation Guide

## Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.9+
- **Git**

## Step 1: Clone Repository

```bash
git clone https://github.com/dusaneaditya353-dot/cubase-expert-system-assistant.git
cd cubase-expert-system-assistant
```

## Step 2: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend server
python main.py
```

Backend will run on `http://localhost:8000`

## Step 3: Frontend Setup

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on `http://localhost:3000`

## Step 4: Verify Installation

1. Open browser to `http://localhost:3000`
2. Test the expert system with a sample query
3. Check API health at `http://localhost:8000/health`

## Production Deployment

### Backend (Docker)

```bash
cd backend
docker build -t cubase-assistant-api .
docker run -p 8000:8000 cubase-assistant-api
```

### Frontend (Build)

```bash
cd frontend
npm run build
# Deploy dist/ folder to your hosting service
```

## Environment Variables

Create `.env` files:

**backend/.env:**
```
PORT=8000
LOG_LEVEL=info
CORS_ORIGINS=http://localhost:3000
```

**frontend/.env:**
```
VITE_API_URL=http://localhost:8000
```

## Troubleshooting

**Port already in use:**
```bash
# Change port in backend/main.py or frontend/vite.config.ts
```

**Module not found:**
```bash
# Reinstall dependencies
pip install -r backend/requirements.txt
npm install --prefix frontend
```

**CORS errors:**
```bash
# Update CORS_ORIGINS in backend/.env
```

## Next Steps

- Read [API Documentation](./API_DOCS.md)
- Explore knowledge base in `knowledge-base/`
- Run tests: `pytest backend/tests/`
