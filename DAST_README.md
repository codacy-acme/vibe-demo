# DAST Security Scanning Setup

This repository includes automated DAST (Dynamic Application Security Testing) using OWASP ZAP and Codacy integration.

## 🚀 Quick Start

### Local Testing

1. **Build and run the application:**
   ```bash
   docker-compose up -d --build
   ```

2. **Test the application:**
   ```bash
   curl http://localhost:3008/api/health
   ```

3. **Run local DAST scan:**
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
   ```

## 🔧 GitHub Actions Setup

### Required Secrets

Add the following secret to your GitHub repository:

- `CODACY_API_TOKEN`: Your Codacy API token

To add secrets:
1. Go to your repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add `CODACY_API_TOKEN` with your token value

### Workflows

This repository includes two DAST workflows:

1. **Full DAST Scan** (`dast-scan.yml`)
   - Runs on push to main/develop branches
   - Performs comprehensive security testing
   - Uploads results to Codacy

2. **PR DAST Scan** (`dast-pr-scan.yml`)
   - Runs on pull requests
   - Performs baseline security testing (faster)
   - Comments results on the PR
   - Uploads results to Codacy

## 📊 Application Endpoints

The demo application includes several endpoints for testing:

- `/` - Home page with navigation
- `/about` - About page
- `/contact` - Contact form (GET/POST)
- `/api/health` - Health check endpoint
- `/robots.txt` - Robots file
- `/sitemap.xml` - XML sitemap

## 🔒 Security Features

The application includes several security headers:
- Content Security Policy
- X-Frame-Options
- X-Content-Type-Options
- Cache-Control
- Permissions-Policy

## 📈 Codacy Integration

DAST scan results are automatically uploaded to Codacy using the API:

```bash
curl -X POST https://app.codacy.com/api/v3/organizations/gh/codacy-acme/security/tools/dast/ZAP/reports \
  -H 'api-token: YOUR_TOKEN' \
  -H 'Content-Type: multipart/form-data' \
  -H 'Accept: application/json' \
  -F 'file=@./zap_output/zap_report.json' \
  -F 'reportFormat=json'
```

## 🛠️ Customization

### Scan Configuration

You can customize the ZAP scans by:

1. **Adding scan rules:** Modify the ZAP command in the workflow files
2. **Excluding URLs:** Add `-I` flag with ignore patterns
3. **Custom context:** Create ZAP context files and mount them

### Application Modification

The Flask application can be extended with:
- Additional routes for testing
- Database connections
- Authentication mechanisms
- API endpoints

## 📝 Troubleshooting

### Common Issues

1. **Application not starting:** Check if port 3008 is available
2. **ZAP scan fails:** Ensure the application is fully started before scanning
3. **Codacy upload fails:** Verify your API token is correct

### Debugging

Check the GitHub Actions logs for detailed error messages and scan results.
