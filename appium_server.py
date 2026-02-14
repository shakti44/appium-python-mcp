import http.server
import socketserver

class MCPServerHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Hello, this is the MCP server!')

if __name__ == '__main__':
    PORT = 8000
    with socketserver.TCPServer(('', PORT), MCPServerHandler) as httpd:
        print(f'Serving at port {PORT}')
        httpd.serve_forever()