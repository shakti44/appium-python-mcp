#!/usr/bin/env python
"""
Main entry point for the Appium MCP Server

Run the server with:
    python main.py

Or with custom host/port:
    python main.py --host 0.0.0.0 --port 8000
"""

import sys
import argparse
import uvicorn

# Add current directory to path
sys.path.insert(0, '.')

from mcp_server.server import app


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Run the Appium MCP Server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind to (default: 8000)')
    parser.add_argument('--reload', action='store_true', help='Enable auto-reload for development')
    
    args = parser.parse_args()
    
    print(f"Starting Appium MCP Server on {args.host}:{args.port}")
    print(f"API documentation available at: http://{args.host}:{args.port}/docs")
    
    uvicorn.run(
        "mcp_server.server:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    )


if __name__ == '__main__':
    main()
