# server.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import subprocess

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Serve index.html as the default page
            self.path = '/index.html'
            
        if self.path == '/index.html':
            with open('index.html', 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(file.read())
        elif self.path == '/aseba.html':
            # Check if aseba.html file exists
            with open('aseba.html', 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(file.read())
        elif self.path == '/blockly_page.html':
            # Check if blockly_page.html file exists
            with open('blockly_page.html', 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(file.read())
 
    def do_POST(self):
        if self.path == '/run':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            code = data['code']
            output, success = self.execute_code(code)
            response = json.dumps({'output': output, 'success': success})
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(response.encode('utf-8'))

    def execute_code(self, code):
        try:
            result = subprocess.run(['python', '-c', code], capture_output=True, text=True)
            return result.stdout, True
        except Exception as e:
            return str(e), False
            

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Starting server...')
    httpd.serve_forever()
