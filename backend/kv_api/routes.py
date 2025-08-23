"""
Routes for the Key-Value Store API
"""

from flask import jsonify, request
from backend.Transactions.transactions import Transactions
from backend.db_operations import DatabaseManager
from backend.Exceptions import KVStoreError

db_manager = DatabaseManager()
import logging 
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def register_routes(app):
    """
    Register all routes with the Flask app
    
    Args:
        app: Flask application instance
    """
    
    transactions = Transactions() 
    
    @app.route('/put/kv/<key>', methods=['PUT'])
    def put_value(key: str):
        """
        put a value into the database
        Args:
            key: The key to put the value for
            
        """
        try:
            data = request.get_json()
            value = data['value']
            
            transactions.set(key, value)
            return jsonify({'response': 'success'})
        
        except KVStoreError as e:
            log.error(f"KVStoreError: {e}")
            return jsonify({'response': 'error', 'message': str(e)})
        

    
    @app.route('/get/kv/<key>', methods=['GET'])
    def get_value(key: str):
        """
        get a value from the database
        Args:
            key: The key to get the value for
            
        """
        try:
            value = transactions.get(key)
            return jsonify({'response': 'success', 'key': key, 'value': value})
            
        except KVStoreError as e:
            log.error(f"KVStoreError: {e}")
            return jsonify({'response': 'error', 'message': str(e)})
    
    
    
    @app.route('/update/kv/<key>', methods=['UPDATE'])
    def update_value(key: str):
        """
        update a value in the database
        Args:
            key: The key to update the value for            
        """
        
        try:
            data = request.get_json()
            value = data['value']
            
            transactions.update(key, value)
            return jsonify({'response': 'success'})
        
        except KVStoreError as e:
            log.error(f"KVStoreError: {e}")
            return jsonify({'response': 'error', 'message': str(e)})
        
        
    @app.route('/delete/kv/<key>', methods=['DELETE'])
    def delete_value(key: str):
        """
        delete a value from the database
        Args:
            key: The key to delete the value for
            
        Returns:
            None
        """
        try:
            transactions.delete(key)
            return jsonify({'response': 'success'})
        
        except KVStoreError as e:
            log.error(f"KVStoreError: {e}")
            return jsonify({'response': 'error', 'message': str(e)})