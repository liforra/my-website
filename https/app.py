from flask import Flask, send_from_directory, request, abort, render_template
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

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_file(path):
    # Check if the path is a directory and if it contains an index.html file
    full_path = os.path.join(app.static_folder, path)
    if os.path.isdir(full_path):
        index_file = os.path.join(full_path, 'index.html')
        if os.path.exists(index_file):
            return send_from_directory(full_path, 'index.html')
    
    # If it's not a directory or doesn't contain index.html, serve the file directly
    if os.path.exists(full_path):
        return send_from_directory(app.static_folder, path)
    
    # If the file doesn't exist, return a 404
    return abort(404)

@app.errorhandler(404)
def page_not_found(e):
    # Serve the custom 404 page
    return send_from_directory(app.static_folder, '404.html'), 404

if __name__ == '__main__':
    app.run()

