from ast import Tuple
from typing import Any, List
from backend.db_operations.database_manager import DatabaseManager
from backend.Exceptions.kv_exceptions import KVStoreError
import logging 

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class Transactions:
    """
    Transactions class for the Key-Value Store
    
    Attributes:
        db_manager: DatabaseManager instance
        pending_transactions: Dictionary to store pending transactions
        in_transaction: Boolean to check if a transaction is in progress
    
    Methods:
        begin: Begin a new transaction
        _clear_pending: Helper to clear pending operations and reset transaction state
        rollback: Rollback the current transaction
        set: Set a value into the database
        update: Update a value in the database
        delete: Delete a value from the database
        commit: Commit the current transaction
    """
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.pending_transactions = {
            "set": [],
            "update": [],
            "delete": []
        }
        self.in_transaction = False
        # Create table once on init
        try:
            self.db_manager.create_table()
        except:
            pass  # Table might already exist
        
        
    
    def begin(self) -> None:
        """Begin a new transaction"""
        self._clear_pending()
        
        
    
    def _clear_pending(self):
        """
        helper to clear pending operations and reset transaction state
        """
        self.pending_transactions = {
            "set": [],
            "update": [],
            "delete": []
        }
        self.in_transaction = True  
    
    
    def rollback(self) -> None:
        """
        Rollback the current transaction
        """
        self.pending_transactions = {
            "set": [],
            "update": [],
            "delete": []
        }
        self.in_transaction = False 

        

    def set(self, key: str, value: Any) -> None:
        """
        
        set a value into the database
        Args:
            key: The key to set the value for
            value: The value to set into the database
            
        """
        if self.in_transaction:
            self.pending_transactions["set"].append((key, value))
        else:
            self.db_manager.put(key, value)
    
    
    
    def get(self, key: str) -> Any:
        """
        
        get a value from the database
        Args:
            key: The key to get the value for
            
            
        """
        try:
            return self.db_manager.get(key)
        
        except KVStoreError as e:
            log.error(f"Error setting value: {e}")
                
    
    def update(self, key: str, value: Any) -> None:
        """
        update a value in the database
        
        Args:
            key: The key to update the value for
            value: The value to update the database
        """
        if self.in_transaction:
            self.pending_transactions["update"].append((key, value))
        else:
            self.db_manager.update(key, value)
    
    
    def delete(self, key: str) -> None:
        """
        delete a value from the database
        
        Args:
            key: The key to delete the value for
           
        """
        if self.in_transaction:
            self.pending_transactions["delete"].append(key)
        else:
            self.db_manager.delete(key)
            
            
        
        
    def commit(self) -> None:
        """
        Commit the current transaction
        """
        try:
            for key, value in self.pending_transactions["set"]:
                self.db_manager.put(key, value)
            
            for key, value in self.pending_transactions["update"]:
                self.db_manager.update(key, value)
            
            for key in self.pending_transactions["delete"]:
                self.db_manager.delete(key)

            self._clear_pending()
    
        
        except KVStoreError as e:
            log.error(f"Error committing transactions: {e}")
            self.rollback()
            
            
            
            
            
            
        