# Information Extraction API

A FastAPI application for extracting information from PDF documents, specifically designed to parse Certificate of Enrollment (CoE) and visa documents.

## Features

- PDF parsing and information extraction
- Secure API endpoints with token authentication
- CORS support
- Modular architecture following FastAPI best practices

## Installation

1. Clone the repository
2. Install dependencies using [uv](https://github.com/astral-sh/uv):

```bash
uv sync --frozen --no-cache
```

Alternatively, install with pip:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file with the following variables:

```
API_SECRET_KEY=your_api_key_here
QUERY_SECRET_KEY=your_query_key_here
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

## Running the Application

### Using Docker

```bash
docker build -t info-extraction .
docker run -p 80:80 info-extraction
```

### Local Development

```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Certificate of Enrollment (CoE) Parser

```http
POST /extract/coe
```

Extracts information from a CoE PDF document.

**Returns:**
- `provider`: Educational institution name
- `course`: Course name
- `start_date`: Course start date (DD/MM/YYYY)
- `end_date`: Course end date (DD/MM/YYYY)

### Visa Document Parser

```http
POST /extract/visa
```

Extracts information from visa documents.

**Returns:**
- `type`: Visa type (e.g., "Student (500)", "Temporary Graduate (485)")
- `expiry_date`: Visa expiry date (YYYY-MM-DD)
- `sector`: Sector information (if available)
- `status`: Visa status ("Active" or "Not Active")

## Authentication

All endpoints require two types of authentication:
1. Query token (`token` query parameter)
2. API token (`X-Token` header for admin routes)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - See LICENSE file for details

Made by [Camilo caceres](https://github.com/camilocaceres)