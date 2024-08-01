// logger.js
(function() {
    const ipApiUrl = 'https://api.ipify.org?format=json';

    function sendLogToServer(ip, path, userAgent) {
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/log-data', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({ ip: ip, path: path, userAgent: userAgent }));
    }

    function getIpAddress() {
        fetch(ipApiUrl)
            .then(response => response.json())
            .then(data => {
                const ip = data.ip;
                const path = window.location.pathname;
                const userAgent = navigator.userAgent;
                sendLogToServer(ip, path, userAgent);
            })
            .catch(error => console.error('Error fetching IP address:', error));
    }

    window.onload = getIpAddress;
})();

