# AI-Gen: Intelligent Content & Image Generator

> **An AI-powered full-stack application that combines intelligent web search with AI image generation**

Transform your queries into insights and your imagination into visuals with our cutting-edge platform that seamlessly integrates MCP (Model Context Protocol) servers for enhanced AI capabilities.

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-4169e1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Tailwind CSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

## ✨ What Makes AI-Gen Special?

- 🔍 **Smart Search**: Leverage DuckDuckGo's MCP integration with intelligent fallbacks
- 🎨 **AI Image Generation**: Create stunning visuals using Flux AI with Pollinations backup
- 📊 **Personal Dashboard**: Track and manage your search history and generated images
- 🔐 **Secure Authentication**: JWT-based user management with encrypted sessions
- 🌐 **Modern UI**: Responsive React interface with Tailwind CSS styling
- 🏗️ **Robust Architecture**: Full-stack solution with PostgreSQL persistence
  
  <img width="1900" height="756" alt="image" src="https://github.com/user-attachments/assets/9a4f0074-e6d4-419c-9d95-c49c22ae9315" />
  <img width="1892" height="925" alt="image" src="https://github.com/user-attachments/assets/ec3fd0e6-9769-4fe6-be07-3062fd91dd08" />
  <img width="1334" height="851" alt="image" src="https://github.com/user-attachments/assets/1366b2a1-0878-466d-a4d1-5655a25b7116" />



## 🎯 Core Features

### 🔍 Intelligent Search
- **Primary**: MCP DuckDuckGo server integration
- **Fallback**: Direct DuckDuckGo API when MCP is unavailable
- **Smart Results**: Curated, relevant search results with metadata

### 🖼️ AI Image Generation  
- **Primary**: MCP Flux ImageGen server
- **Fallback**: Pollinations API for reliable image creation
- **Customizable**: Adjustable dimensions, steps, and guidance parameters

### 📜 Personal Dashboard
- **History Management**: View all your searches and generated images
- **Smart Filtering**: Filter by type, date, or keywords
- **Easy Cleanup**: Delete items you no longer need
- **Export Options**: Download your generated images

### 🔐 Secure User System
- **JWT Authentication**: Secure token-based authentication
- **Password Encryption**: bcrypt hashing for user security
- **Session Management**: Automatic token refresh and validation
- **Protected Routes**: Role-based access control

## 🏗️ Architecture Overview

```mermaid
graph TD
    A[React Frontend] --> B[FastAPI Backend]
    B --> C[PostgreSQL Database]
    B --> D[MCP DuckDuckGo Server]
    B --> E[MCP Flux ImageGen]
    B --> F[Fallback APIs]
    D -.-> G[DuckDuckGo API]
    E -.-> H[Pollinations API]
    F --> G
    F --> H
```

### Tech Stack

**Frontend**
- ⚛️ React 18+ with modern hooks
- 🎨 Tailwind CSS for styling
- 🚦 React Router for navigation
- 📱 Responsive design patterns

**Backend**
- 🐍 FastAPI with async/await
- 🗃️ SQLAlchemy ORM with PostgreSQL
- 🔑 JWT authentication (OAuth2 flow)
- 🔌 MCP (Model Context Protocol) integration

**Database**
- 🐘 PostgreSQL for data persistence
- 📊 Optimized schemas for search/image history
- 🔄 Database migrations with Alembic

## ⚡ Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 12+
- Git

### 1. Clone & Setup

```bash
# Clone the repository
git clone https://github.com/your-username/ai-gen.git
cd Aigen

# Quick setup script (optional)
chmod +x setup.sh && ./setup.sh
```

### 2. Database Setup

```bash
# Install PostgreSQL (Ubuntu/Debian)
sudo apt install postgresql postgresql-contrib

# Create database
sudo -u postgres createdb aigen

# Create user (optional)
sudo -u postgres createuser --interactive aigen_user
```

### 3. Backend Configuration

```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database credentials and API keys
```

**Environment Variables (.env)**:
```env
# Database
DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/aigen

# JWT
SECRET_KEY=your-super-secret-jwt-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# MCP API Keys
DUCKDUCKGO_MCP_API_KEY=your-duckduckgo-api-key
FLUX_MCP_API_KEY=your-flux-api-key

# Fallback APIs
DUCKDUCKGO_API_URL=https://api.duckduckgo.com/
POLLINATIONS_API_URL=https://image.pollinations.ai/
```

### 4. Start Backend

```bash
# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or use the development script
python -m backend.main
```

**Backend will be available at:**
- 🌐 API: http://localhost:8000
- 📚 Documentation: http://localhost:8000/docs
- 🔧 Health Check: http://localhost:8000/health

### 5. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Frontend will be available at:**
- 🌐 Application: http://localhost:5173

## 📁 Project Structure

```
ai-gen/
├── backend/                    # FastAPI application
│   ├── routers/               # API route handlers
│   │   ├── auth.py           # Authentication endpoints
│   │   ├── search.py         # Search functionality
│   │   ├── image.py          # Image generation
│   │   └── dashboard.py      # User dashboard
│   ├── models/               # SQLAlchemy models
│   ├── schemas/              # Pydantic schemas
│   ├── mcp_clients.py        # MCP integration
│   ├── mcp_fallback.py       # Fallback implementations
│   ├── database.py           # Database configuration
│   ├── auth.py               # Authentication utilities
│   ├── main.py               # FastAPI app entry point
│   └── requirements.txt      # Python dependencies
├── frontend/                  # React application
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/           # Page components
│   │   ├── hooks/           # Custom React hooks
│   │   ├── services/        # API service functions
│   │   ├── utils/           # Utility functions
│   │   └── App.jsx          # Main app component
│   ├── public/              # Static assets
│   └── package.json         # Node.js dependencies
├── docs/                     # Documentation
├── scripts/                  # Deployment scripts
└── README.md                # You are here!
```

## 🛠️ API Reference

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/auth/register` | Create new account | ✅ |
| `POST` | `/auth/login` | Login and get JWT token | ✅ |

**Register Request:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Login Request:**
```json
{
  "username": "johndoe",
  "password": "securepassword123"
}
```

### Search

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/search?q={query}&limit={limit}` | Perform web search | ✅ |

**Response:**
```json
{
  "query": "artificial intelligence",
  "results": [
    {
      "title": "What is Artificial Intelligence?",
      "snippet": "AI refers to computer systems...",
      "url": "https://example.com/ai-guide",
      "source": "DuckDuckGo"
    }
  ],
  "search_id": "uuid-here"
}
```

### Image Generation

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/image` | Generate AI image | ✅ |

**Request:**
```json
{
  "prompt": "A futuristic cityscape at sunset",
  "width": 1024,
  "height": 1024,
  "steps": 30,
  "guidance": 7.5
}
```

**Response:**
```json
{
  "image_id": "uuid-here",
  "url": "https://generated-image-url.com/image.jpg",
  "prompt": "A futuristic cityscape at sunset",
  "parameters": {
    "width": 1024,
    "height": 1024,
    "steps": 30,
    "guidance": 7.5
  },
  "generated_at": "2024-01-15T10:30:00Z"
}
```

### Dashboard

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/dashboard` | Get user's history | ✅ |
| `DELETE` | `/dashboard/{item_id}` | Delete history item | ✅ |

## 🔧 Configuration Options

### MCP Integration

The application supports both MCP servers and fallback APIs:

**MCP Servers:**
- **DuckDuckGo**: `https://server.smithery.ai/@nickclyde/duckduckgo-mcp-server/mcp`
- **Flux ImageGen**: Custom MCP server for AI image generation

**Fallback APIs:**
- **DuckDuckGo Instant Answer API**: For search when MCP is unavailable
- **Pollinations**: For image generation when Flux MCP is unavailable

### Database Configuration

**PostgreSQL Setup:**
```python
# backend/database.py
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://user:password@localhost:5432/aigen"

# For development with SQLite (optional)
SQLALCHEMY_DATABASE_URL = "sqlite:///./ai_gen.db"
```

### CORS Configuration

```python
# backend/main.py
origins = [
    "http://localhost:5173",  # Vite dev server
    "http://localhost:3000",  # Alternative React dev
    "https://your-domain.com",  # Production domain
]
```

## 🚀 Deployment

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build separately
docker build -t ai-gen-backend ./backend
docker build -t ai-gen-frontend ./frontend
```

### Production Environment

1. **Environment Variables**: Set production values in `.env`
2. **Database**: Use managed PostgreSQL (AWS RDS, Google Cloud SQL)
3. **API Keys**: Secure your MCP and fallback API keys
4. **HTTPS**: Enable SSL/TLS certificates
5. **Monitoring**: Set up logging and health checks

### Deployment Platforms

- **Backend**: Railway, Render, DigitalOcean, AWS
- **Frontend**: Vercel, Netlify, GitHub Pages
- **Database**: AWS RDS, Google Cloud SQL, Railway PostgreSQL

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and test thoroughly
4. Commit with conventional commits: `git commit -m "feat: add amazing feature"`
5. Push to your branch: `git push origin feature/amazing-feature`
6. Create a Pull Request

### Code Standards

- **Backend**: Follow PEP 8 with Black formatting
- **Frontend**: ESLint + Prettier configuration
- **Commits**: Use conventional commit messages
- **Tests**: Write tests for new features

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI**: For the amazing Python web framework
- **React**: For the powerful frontend library
- **MCP**: For the Model Context Protocol integration
- **Tailwind CSS**: For the utility-first CSS framework
- **PostgreSQL**: For reliable data persistence

## 📞 Support

- 📧 **Email**: nsdhanush5@gmail.com


---

**Built with ❤️ by the AI-Gen Team**

*Transforming ideas into intelligent experiences, one query at a time.*


