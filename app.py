from flask import Flask, make_response, request

app = Flask(__name__)

@app.after_request
def add_security_headers(response):
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
def handle_500(error):
    return 'An error occurred', 500

@app.errorhandler(404)
def handle_404(error):
    return 'Page not found', 404

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/robots.txt')
def robots():
    return 'User-agent: *\nDisallow: '

@app.route('/sitemap.xml')
def sitemap():
    return '<?xml version="1.0" encoding="UTF-8"?><urlset></urlset>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3008, debug=False)