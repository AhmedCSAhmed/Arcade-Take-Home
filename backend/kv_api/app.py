"""
Flask application for Key-Value Store with Transactions
"""

from flask import Flask
from .routes import register_routes


def create_app():
    """
    Create and configure the Flask application
    
    Returns:
        Flask app instance
    """
    app = Flask(__name__)
    
    register_routes(app)
    
    return app


def main():
    """Run the Flask development server"""
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()