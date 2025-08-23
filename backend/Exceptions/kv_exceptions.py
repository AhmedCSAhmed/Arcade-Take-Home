"""
Custom exceptions for key-value store database operations
"""


class KVStoreError(Exception):
    """
    Base exception for all key-value store errors
    
    Attributes:
        operation: The operation that failed (get, put, update, delete, etc.)
        key: The key involved in the operation (if applicable)
        message: Human-readable error description
    """
    
    def __init__(self, operation: str, message: str, key: str = None):
        self.operation = operation
        self.key = key
        self.message = message
        
        if key:
            full_message = f"Operation '{operation}' failed for key '{key}': {message}"
        else:
            full_message = f"Operation '{operation}' failed: {message}"
            
        super().__init__(full_message)
        
    def __str__(self):
        return self.args[0]
