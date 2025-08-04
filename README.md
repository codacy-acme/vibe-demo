# DAST Demo Application

This repository contains a Flask web application designed for Dynamic Application Security Testing (DAST) with automated GitHub Actions integration and Codacy reporting.

## 🚀 Features

- **Flask Web Application**: Multi-endpoint application perfect for DAST testing
- **Security Headers**: Comprehensive security headers implementation
- **GitHub Actions**: Automated DAST scanning on commits and PRs
- **Codacy Integration**: Automatic upload of scan results to Codacy
- **Docker Support**: Containerized application for consistent testing
- **Multiple Scan Types**: Full scans for main branches, baseline scans for PRs
- **Security Updates**: All dependencies updated to latest secure versions

## 📦 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.9+
- GitHub repository with Actions enabled
- Codacy account with API token

### Local Development

1. **Clone and setup:**
   ```bash
   git clone <your-repo-url>
   cd vibe-demo
   ```

2. **Run with Docker:**
   ```bash
   docker-compose up -d --build
   ```

3. **Test the application:**
   ```bash
   python test_dast_app.py
   ```

4. **Run local DAST scan:**
   ```bash
   mkdir -p zap_output
   docker run --rm \
     -v $(pwd)/zap_output:/zap/wrk:rw \
     --network host \
     ghcr.io/zaproxy/zaproxy:stable \
     zap-baseline.py \
     -t http://localhost:3008 \
     -J /zap/wrk/zap_report.json \
     -r /zap/wrk/zap_report.html
## 🔧 GitHub Actions Setup

### 1. Add Codacy API Token

1. Go to your repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `CODACY_API_TOKEN`
4. Value: Your Codacy API token

### 2. Workflow Files

The repository includes two workflows:

- **`dast-scan.yml`**: Full DAST scan for main/develop branches
- **`dast-pr-scan.yml`**: Fast baseline scan for pull requests with PR comments

### 3. Trigger Scans

Scans are automatically triggered on:
- Push to `main`, `develop`, or `dast-*` branches
- Pull requests to `main` or `develop` branches

## 🔒 Application Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page with navigation |
| `/about` | GET | About page |
| `/contact` | GET | Contact form |
| `/contact` | POST | Form submission handler |
| `/api/health` | GET | Health check endpoint |
| `/robots.txt` | GET | Robots file |
| `/sitemap.xml` | GET | XML sitemap |

## 📊 Security Features

- Content Security Policy (CSP)
- X-Frame-Options header
- X-Content-Type-Options header
- Permissions-Policy header
- Cache-Control headers
- Server header removal
- Updated secure dependencies (requests 2.32.4, urllib3 2.5.0)

## 🛠️ Troubleshooting

### Common Issues

1. **Application not starting**: Check if port 3008 is available
2. **ZAP scan fails**: Ensure application is fully started before scanning
3. **Codacy upload fails**: Verify API token is correct
4. **Docker issues**: Ensure Docker daemon is running

### Debug Commands

```bash
# Check application logs
docker logs dast-app

# Test application manually
curl http://localhost:3008/api/health

# Validate ZAP report
python -m json.tool zap_output/zap_report.json
```

For more detailed information, see `DAST_README.md`.

This is a demonstration application. The weather API functionality requires a valid API key from OpenWeatherMap to work properly.
