from flask import Flask, send_from_directory, request, abort, jsonify
import os
from datetime import datetime
import ipaddress

app = Flask(__name__, static_folder=os.getcwd())

# Define the IP ranges to be checked
IP_RANGES = [
    ipaddress.ip_network('173.245.48.0/20'),
    ipaddress.ip_network('103.21.244.0/22'),
    ipaddress.ip_network('103.22.200.0/22'),
    ipaddress.ip_network('103.31.4.0/22'),
    ipaddress.ip_network('141.101.64.0/18'),
    ipaddress.ip_network('108.162.192.0/18'),
    ipaddress.ip_network('190.93.240.0/20'),
    ipaddress.ip_network('188.114.96.0/20'),
    ipaddress.ip_network('197.234.240.0/22'),
    ipaddress.ip_network('198.41.128.0/17'),
    ipaddress.ip_network('162.158.0.0/15'),
    ipaddress.ip_network('104.16.0.0/13'),
    ipaddress.ip_network('104.24.0.0/14'),
    ipaddress.ip_network('172.64.0.0/13'),
    ipaddress.ip_network('131.0.72.0/22')
]

def load_ip_ranges(filename):
    """Load IP ranges from a file and store them as ip_network objects."""
    global IP_RANGES
    IP_RANGES = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    try:
                        IP_RANGES.append(ipaddress.ip_network(line))
                    except ValueError:
                        print(f"Invalid IP range format: {line}")
    except FileNotFoundError:
        print(f"File not found: {filename}")

def is_ip_in_ranges(ip):
    """Check if the given IP address is within any of the specified IP ranges."""
    ip_addr = ipaddress.ip_address(ip)
    return any(ip_addr in network for network in IP_RANGES)

def log_data(ip_address, path, user_agent):
    """Log the data if the IP is not in the specified ranges."""
    if is_ip_in_ranges(ip_address):
        print(f"IP {ip_address} is in the excluded range. Data will not be logged.")
        return

    with open('log.txt', 'a') as log_file:
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        log_file.write(f'{timestamp} | {ip_address} | {path} | {user_agent}\n')

def get_client_ip():
    """Extract the real client IP address from Cloudflare headers."""
    # Cloudflare's header for client IP
    if 'CF-Connecting-IP' in request.headers:
        return request.headers.get('CF-Connecting-IP')
    
    # Fallback to X-Forwarded-For (might contain multiple IPs)
    if 'X-Forwarded-For' in request.headers:
        forwarded_for = request.headers.get('X-Forwarded-For')
        # The client IP is usually the first IP in the list
        return forwarded_for.split(',')[0].strip()
    
    # Fallback to remote address (could be Cloudflare's IP)
    return request.remote_addr

@app.before_request
def log_request_ip():
    # Only log the request IP if not logging via /log-data
    if request.endpoint != 'log_data':
        ip_address = get_client_ip()
        path = request.path
        user_agent = request.headers.get('User-Agent')
        log_data(ip_address, path, user_agent)

@app.route('/log-data', methods=['POST'])
def log_data_from_client():
    data = request.get_json()
    ip_address = data.get('ip')
    path = data.get('path')
    user_agent = data.get('userAgent')
    if ip_address and path and user_agent:
        log_data(ip_address, path, user_agent)
        return jsonify({'status': 'success'}), 200
    return jsonify({'status': 'error', 'message': 'Incomplete data'}), 400

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_file(path):
    full_path = os.path.join(app.static_folder, path)
    if os.path.isdir(full_path):
        index_file = os.path.join(full_path, 'index.html')
        if os.path.exists(index_file):
            return send_from_directory(full_path, 'index.html')
    
    if os.path.exists(full_path):
        return send_from_directory(app.static_folder, path)
    
    return abort(404)

@app.errorhandler(404)
def page_not_found(e):
    return send_from_directory(app.static_folder, '404.html'), 404

if __name__ == '__main__':
    load_ip_ranges('no_log_ips.txt')
    app.run()

