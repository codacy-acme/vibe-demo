"""
DAST Demo Flask Application

A simple Flask web application designed for Dynamic Application Security Testing (DAST).
Includes security headers, multiple endpoints, and forms for comprehensive testing.
"""
from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.after_request
def add_security_headers(response):
    """Add security headers to all responses."""
    response.headers['Content-Security-Policy'] = "default-src 'self'; frame-ancestors 'none'; form-action 'self'"
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    response.headers['X-Content-Type-Options'] = 'nosniff'

    if request.path in ['/robots.txt', '/sitemap.xml', '/']:
        response.headers['Cache-Control'] = 'public, max-age=3600'
    else:
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'

    response.headers.pop('Server', None)
    return response

@app.errorhandler(500)
def handle_500(_error):
    """Handle 500 internal server errors."""
    return 'An error occurred', 500

@app.errorhandler(404)
def handle_404(_error):
    """Handle 404 not found errors."""
    return 'Page not found', 404

@app.route('/')
def hello_world():
    """Home page with navigation links."""
    html_template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>DAST Demo App</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body>
        <h1>Hello, World!</h1>
        <p>This is a demo application for DAST scanning.</p>
        <ul>
            <li><a href="/about">About</a></li>
            <li><a href="/contact">Contact</a></li>
            <li><a href="/api/health">Health Check</a></li>
        </ul>
    </body>
    </html>
    '''
    return render_template_string(html_template)

@app.route('/about')
def about():
    """About page with information about the application."""
    html_template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>About - DAST Demo App</title>
    </head>
    <body>
        <h1>About Us</h1>
        <p>This is a simple Flask application designed for DAST security testing.</p>
        <a href="/">Home</a>
    </body>
    </html>
    '''
    return render_template_string(html_template)

@app.route('/contact')
def contact():
    """Contact form page."""
    html_template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Contact - DAST Demo App</title>
    </head>
    <body>
        <h1>Contact Us</h1>
        <form method="post" action="/contact">
            <label for="name">Name:</label><br>
            <input type="text" id="name" name="name"><br><br>
            <label for="email">Email:</label><br>
            <input type="email" id="email" name="email"><br><br>
            <label for="message">Message:</label><br>
            <textarea id="message" name="message"></textarea><br><br>
            <input type="submit" value="Submit">
        </form>
        <a href="/">Home</a>
    </body>
    </html>
    '''
    return render_template_string(html_template)

@app.route('/contact', methods=['POST'])
def contact_post():
    """Handle contact form submission."""
    return 'Thank you for your message!', 200

@app.route('/api/health')
def health_check():
    """Health check endpoint for monitoring."""
    return {'status': 'healthy', 'service': 'dast-demo-app'}, 200

@app.route('/robots.txt')
def robots():
    """Robots.txt file for web crawlers."""
    return 'User-agent: *\nDisallow: /admin\n'

@app.route('/sitemap.xml')
def sitemap():
    """XML sitemap for search engines."""
    return '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url><loc>http://localhost:3008/</loc></url>
    <url><loc>http://localhost:3008/about</loc></url>
    <url><loc>http://localhost:3008/contact</loc></url>
</urlset>'''

if __name__ == '__main__':
    # NOTE: host='0.0.0.0' is intentional for containerized deployment
    # In production, this should be behind a reverse proxy
    app.run(host='0.0.0.0', port=3008, debug=False)
