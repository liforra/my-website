import subprocess

def run_gunicorn(command):
    process = subprocess.Popen(command, shell=True)
    return process

def main():
    # Paths to SSL certificate and key
    certfile = '/etc/ssl/cert.pem'
    keyfile = '/etc/ssl/key.pem'

    # Command to run HTTP instance
    http_command = 'cd http && gunicorn -w 4 -b 0.0.0.0:80 app:app'
    
    # Command to run HTTPS instance
    https_command = f'cd ./https/ && gunicorn --certfile={certfile} --keyfile={keyfile} -w 4 -b 0.0.0.0:443 app:app'

    print("Starting HTTP server on port 80...")
    http_process = run_gunicorn(http_command)

    print("Starting HTTPS server on port 443...")
    https_process = run_gunicorn(https_command)

    # Wait for processes to finish (or handle them in a more sophisticated way if needed)
    http_process.wait()
    https_process.wait()

if __name__ == '__main__':
    main()

