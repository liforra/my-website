from flask import Flask, send_from_directory, request
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
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run()

