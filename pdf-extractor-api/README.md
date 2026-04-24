# PDF Page Extractor API

Extracts specific pages from a PDF based on page titles. Built for n8n Cloud integration.

## Pages Extracted
- POWER OF ATTORNEY
- TITLE AND REGISTRATION APPLICATION
- ODOMETER DISCLOSURE

## Deploy on Render.com (Free)

1. Push this folder to a GitHub repo
2. Go to https://render.com and sign up free
3. Click "New" → "Web Service"
4. Connect your GitHub repo
5. Render auto-detects settings from render.yaml
6. Click "Deploy" — done!

Your API URL will be: https://pdf-extractor-api.onrender.com

## API Endpoint

### POST /extract-pages
- **Input**: PDF file (multipart/form-data, field name = "file")
- **Output**: Extracted PDF binary

## n8n Setup (2 nodes only)

### Node 1 — HTTP Request
- Method: POST
- URL: https://your-api.onrender.com/extract-pages
- Body: Form Data
  - Field name: file
  - Value: {{ $binary.test }}
  - Type: File

### Node 2 — Use the returned PDF binary
- The response is the extracted PDF ready to use
