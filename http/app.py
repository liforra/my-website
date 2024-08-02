from flask import Flask, send_from_directory, request, redirect, url_for
import os

app = Flask(__name__, static_folder=os.getcwd())

def log_ip(ip_address):
    with open('ip_log.txt', 'a') as log_file:
        log_file.write(f'{ip_address}\n')

@app.before_request
def log_request_ip():
    # Log the client's IP address
    ip_address = request.remote_addr
    log_ip(ip_address)

    # Redirect HTTP to HTTPS
    if request.scheme == 'http':
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)

    # Redirect to liforra.de if not already there
    if request.host != 'liforra.de':
        url = request.url.replace(request.host, 'liforra.de', 1)
        return redirect(url, code=301)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    # Ensure the server is set up to handle HTTPS
    app.run(ssl_context=('cert.pem', 'key.pem'))

