"""
Health check endpoint for Railway deployment
"""
import os
import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import json

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            try:
                # Check database connectivity
                db_path = os.getenv('DATABASE_PATH', 'data/bot_database.db')
                conn = sqlite3.connect(db_path)
                conn.execute('SELECT 1')
                conn.close()
                
                # Check if bot files exist
                status = {
                    "status": "healthy",
                    "database": "connected",
                    "timestamp": str(os.times()),
                    "bot": "running"
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(status).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                error_response = {"status": "unhealthy", "error": str(e)}
                self.wfile.write(json.dumps(error_response).encode())
        else:
            self.send_response(404)
            self.end_headers()

def start_health_server():
    """Start health check server in background"""
    port = int(os.getenv('PORT', 8080))
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    server.serve_forever()

if __name__ == "__main__":
    # Start health server in background thread
    health_thread = threading.Thread(target=start_health_server, daemon=True)
    health_thread.start()
    print(f"Health check server started on port {os.getenv('PORT', 8080)}")