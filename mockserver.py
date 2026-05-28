#!/usr/bin/env python3
"""
MockServer-CLI - Lightweight Terminal HTTP API Mock Server
A zero-dependency Python CLI tool for quick API mocking.
"""

import argparse
import json
import os
import re
import sys
import time
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

__version__ = "1.0.0"
__author__ = "MockServer-CLI Team"

# Default configuration
DEFAULT_CONFIG = {
    "host": "127.0.0.1",
    "port": 8080,
    "cors": True,
    "delay": 0,
    "error_rate": 0,
    "routes": {
        "/api/health": {
            "method": "GET",
            "status": 200,
            "response": {"status": "ok", "timestamp": "{{timestamp}}"}
        },
        "/api/users": {
            "method": "GET",
            "status": 200,
            "response": {
                "users": [
                    {"id": 1, "name": "Alice"},
                    {"id": 2, "name": "Bob"}
                ]
            }
        },
        "/api/users/:id": {
            "method": "GET",
            "status": 200,
            "response": {"id": "{{params.id}}", "name": "User {{params.id}}"}
        }
    }
}


class MockRequestHandler(BaseHTTPRequestHandler):
    """Custom HTTP request handler for mock server."""
    
    config = None
    request_log = []
    log_lock = threading.Lock()
    
    def log_message(self, format, *args):
        """Override to customize logging."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {self.client_address[0]} - {format % args}")
    
    def _send_cors_headers(self):
        """Send CORS headers if enabled."""
        if self.config.get("cors", True):
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS, PATCH")
            self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
    
    def _send_json_response(self, status_code, data):
        """Send JSON response."""
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self._send_cors_headers()
        self.end_headers()
        
        if isinstance(data, (dict, list)):
            data = json.dumps(data, ensure_ascii=False, indent=2)
        
        self.wfile.write(data.encode("utf-8"))
    
    def _parse_path_params(self, pattern, path):
        """Parse path parameters from URL."""
        # Convert pattern to regex
        regex_pattern = re.sub(r':(\w+)', r'(?P<\1>[^/]+)', pattern)
        regex_pattern = f"^{regex_pattern}$"
        
        match = re.match(regex_pattern, path)
        if match:
            return match.groupdict()
        return None
    
    def _match_route(self, path, method):
        """Find matching route for the request."""
        routes = self.config.get("routes", {})
        
        # First try exact match
        if path in routes:
            route = routes[path]
            route_method = route.get("method", "GET")
            if route_method == method or route_method == "*":
                return route, {}
        
        # Try pattern match with path parameters
        for pattern, route in routes.items():
            if ":" in pattern:
                params = self._parse_path_params(pattern, path)
                if params:
                    route_method = route.get("method", "GET")
                    if route_method == method or route_method == "*":
                        return route, params
        
        return None, None
    
    def _process_template(self, obj, params=None, request_body=None):
        """Process template variables in response."""
        if params is None:
            params = {}
        if request_body is None:
            request_body = {}
        
        if isinstance(obj, str):
            # Replace template variables
            obj = obj.replace("{{timestamp}}", datetime.now().isoformat())
            obj = obj.replace("{{random}}", str(int(time.time() * 1000) % 10000))
            
            # Replace path params
            for key, value in params.items():
                obj = obj.replace(f"{{{{params.{key}}}}}", str(value))
            
            # Replace request body fields
            for key, value in request_body.items():
                if isinstance(value, (str, int, float, bool)):
                    obj = obj.replace(f"{{{{body.{key}}}}}", str(value))
            
            return obj
        elif isinstance(obj, dict):
            return {k: self._process_template(v, params, request_body) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._process_template(item, params, request_body) for item in obj]
        return obj
    
    def _should_return_error(self):
        """Check if should simulate error based on error rate."""
        error_rate = self.config.get("error_rate", 0)
        if error_rate > 0:
            import random
            return random.random() < (error_rate / 100)
        return False
    
    def _apply_delay(self):
        """Apply configured delay."""
        delay = self.config.get("delay", 0)
        if delay > 0:
            time.sleep(delay / 1000)  # Convert ms to seconds
    
    def _log_request(self, method, path, status, response_time):
        """Log request details."""
        with self.log_lock:
            self.request_log.append({
                "timestamp": datetime.now().isoformat(),
                "method": method,
                "path": path,
                "status": status,
                "response_time_ms": response_time
            })
            # Keep only last 1000 requests
            if len(self.request_log) > 1000:
                self.request_log = self.request_log[-1000:]
    
    def _handle_request(self, method):
        """Handle HTTP request."""
        start_time = time.time()
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Apply delay simulation
        self._apply_delay()
        
        # Handle CORS preflight
        if method == "OPTIONS":
            self.send_response(200)
            self._send_cors_headers()
            self.end_headers()
            return
        
        # Check for error simulation
        if self._should_return_error():
            self._send_json_response(500, {"error": "Simulated server error"})
            response_time = int((time.time() - start_time) * 1000)
            self._log_request(method, path, 500, response_time)
            return
        
        # Find matching route
        route, params = self._match_route(path, method)
        
        if route is None:
            self._send_json_response(404, {"error": "Route not found", "path": path, "method": method})
            response_time = int((time.time() - start_time) * 1000)
            self._log_request(method, path, 404, response_time)
            return
        
        # Parse request body for POST/PUT/PATCH
        request_body = {}
        if method in ["POST", "PUT", "PATCH"]:
            content_length = self.headers.get("Content-Length")
            if content_length:
                body = self.rfile.read(int(content_length))
                try:
                    request_body = json.loads(body.decode("utf-8"))
                except json.JSONDecodeError:
                    pass
        
        # Process response
        status = route.get("status", 200)
        response = route.get("response", {})
        processed_response = self._process_template(response, params, request_body)
        
        self._send_json_response(status, processed_response)
        response_time = int((time.time() - start_time) * 1000)
        self._log_request(method, path, status, response_time)
    
    def do_GET(self):
        self._handle_request("GET")
    
    def do_POST(self):
        self._handle_request("POST")
    
    def do_PUT(self):
        self._handle_request("PUT")
    
    def do_DELETE(self):
        self._handle_request("DELETE")
    
    def do_PATCH(self):
        self._handle_request("PATCH")
    
    def do_OPTIONS(self):
        self._handle_request("OPTIONS")


def load_config(config_path):
    """Load configuration from file."""
    if not config_path or not os.path.exists(config_path):
        print(f"⚠️  Config file not found: {config_path}")
        print("📄 Using default configuration")
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            if config_path.endswith(".json"):
                user_config = json.load(f)
            elif config_path.endswith(".yaml") or config_path.endswith(".yml"):
                # Simple YAML parser (for basic cases)
                user_config = parse_yaml(f.read())
            else:
                print(f"❌ Unsupported config format: {config_path}")
                return DEFAULT_CONFIG.copy()
        
        # Merge with defaults
        config = DEFAULT_CONFIG.copy()
        config.update(user_config)
        print(f"✅ Loaded config from: {config_path}")
        return config
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return DEFAULT_CONFIG.copy()


def parse_yaml(content):
    """Simple YAML parser for basic use cases."""
    # For simplicity, we'll use JSON-like parsing
    # In production, you might want to use PyYAML
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Very basic YAML to dict conversion
        result = {}
        current_key = None
        current_list = None
        
        for line in content.split("\n"):
            line = line.rstrip()
            if not line or line.startswith("#"):
                continue
            
            if ":" in line and not line.startswith("-"):
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                
                if value:
                    # Try to parse as JSON
                    try:
                        value = json.loads(value)
                    except:
                        pass
                    result[key] = value
                    current_key = None
                    current_list = None
                else:
                    current_key = key
                    result[key] = {}
            elif line.startswith("-") and current_key:
                value = line[1:].strip()
                if current_key not in result:
                    result[current_key] = []
                try:
                    result[current_key].append(json.loads(value))
                except:
                    result[current_key].append(value)
        
        return result


def create_sample_config(output_path):
    """Create a sample configuration file."""
    sample_config = {
        "host": "127.0.0.1",
        "port": 8080,
        "cors": True,
        "delay": 0,
        "error_rate": 0,
        "routes": {
            "/api/health": {
                "method": "GET",
                "status": 200,
                "response": {
                    "status": "healthy",
                    "version": "1.0.0",
                    "timestamp": "{{timestamp}}"
                }
            },
            "/api/users": {
                "method": "GET",
                "status": 200,
                "response": {
                    "data": [
                        {"id": 1, "name": "Alice", "email": "alice@example.com"},
                        {"id": 2, "name": "Bob", "email": "bob@example.com"}
                    ],
                    "total": 2
                }
            },
            "/api/users": {
                "method": "POST",
                "status": 201,
                "response": {
                    "id": "{{random}}",
                    "name": "{{body.name}}",
                    "created_at": "{{timestamp}}"
                }
            },
            "/api/users/:id": {
                "method": "GET",
                "status": 200,
                "response": {
                    "id": "{{params.id}}",
                    "name": f"User {{params.id}}",
                    "profile": {
                        "bio": "This is a mock user profile",
                        "joined": "2024-01-01"
                    }
                }
            },
            "/api/users/:id": {
                "method": "PUT",
                "status": 200,
                "response": {
                    "id": "{{params.id}}",
                    "name": "{{body.name}}",
                    "updated_at": "{{timestamp}}"
                }
            },
            "/api/users/:id": {
                "method": "DELETE",
                "status": 204,
                "response": {}
            }
        }
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(sample_config, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Created sample config: {output_path}")


def print_stats():
    """Print request statistics."""
    log = MockRequestHandler.request_log
    if not log:
        print("\n📊 No requests recorded yet")
        return
    
    total = len(log)
    success = sum(1 for r in log if 200 <= r["status"] < 300)
    errors = sum(1 for r in log if r["status"] >= 400)
    avg_time = sum(r["response_time_ms"] for r in log) / total
    
    print("\n" + "=" * 50)
    print("📊 Request Statistics")
    print("=" * 50)
    print(f"Total Requests: {total}")
    print(f"Successful (2xx): {success}")
    print(f"Errors (4xx/5xx): {errors}")
    print(f"Avg Response Time: {avg_time:.2f}ms")
    print("=" * 50)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="MockServer-CLI - Lightweight HTTP API Mock Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Start with default config
  %(prog)s -c config.json           # Start with custom config
  %(prog)s -p 3000                  # Start on port 3000
  %(prog)s --init                   # Create sample config file
  %(prog)s --stats                  # Show request statistics
        """
    )
    
    parser.add_argument("-c", "--config", help="Path to configuration file (JSON or YAML)")
    parser.add_argument("-p", "--port", type=int, help="Port to listen on (default: 8080)")
    parser.add_argument("-H", "--host", help="Host to bind to (default: 127.0.0.1)")
    parser.add_argument("--init", action="store_true", help="Create a sample configuration file")
    parser.add_argument("--stats", action="store_true", help="Show request statistics")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    
    args = parser.parse_args()
    
    if args.init:
        create_sample_config("mockserver.config.json")
        return
    
    if args.stats:
        print_stats()
        return
    
    # Load configuration
    config = load_config(args.config)
    
    # Override with command line arguments
    if args.port:
        config["port"] = args.port
    if args.host:
        config["host"] = args.host
    
    # Set config for handler
    MockRequestHandler.config = config
    
    host = config["host"]
    port = config["port"]
    
    # Create server
    server = HTTPServer((host, port), MockRequestHandler)
    
    print("=" * 60)
    print("🚀 MockServer-CLI v" + __version__)
    print("=" * 60)
    print(f"📡 Server running at http://{host}:{port}")
    print(f"📄 CORS enabled: {config.get('cors', True)}")
    print(f"⏱️  Delay: {config.get('delay', 0)}ms")
    print(f"❌ Error rate: {config.get('error_rate', 0)}%")
    print(f"🛣️  Routes: {len(config.get('routes', {}))}")
    print("=" * 60)
    print("Press Ctrl+C to stop the server")
    print("")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down server...")
        server.shutdown()
        print_stats()
        print("👋 Goodbye!")


if __name__ == "__main__":
    main()
