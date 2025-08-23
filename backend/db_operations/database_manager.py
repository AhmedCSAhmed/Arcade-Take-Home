import sqlite3
import logging
import pickle
from typing import Any
from backend.Exceptions.kv_exceptions import KVStoreError

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class DatabaseManager:
    
    def create_session(self) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
        try:
            log.info(f"Creating session")
            conn = sqlite3.connect("kv_store.db")
            cursor = conn.cursor()
            return conn, cursor
        
        except Exception as e:
            log.error(f"Error creating session: {e}")
            raise KVStoreError("create_session", str(e))
    
    
    
    def create_table(self) -> None:
        """
        Create a table in the database
        
        This should only be called once, when the database is created
        """
        try:
            
            log.info(f"Creating table")
            conn, cursor = self.create_session()
            
            # Want to note here that the Key can be anything besides a String but having it as a blob will be way slower and be very inefcient
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS kv_store(
                            key TEXT PRIMARY KEY,
                            value BLOB
                            )
                           """)
            
            conn.commit()
            conn.close()
            
            log.info(f"Table created successfully")

        except sqlite3.Error as e:
            log.error(f"Error creating table: {e}")
            raise KVStoreError("create_table", str(e))
        
    
    
    def get(self, key: str) -> Any:
        """
        Get a value from the database
        
        Args:
            key: The key to get the value for
            
        Returns:
            The value for the key
        """
        # Sanity check
        if not key:
            log.info(f"Key cannot be empty")
            raise KVStoreError("get", "Key cannot be empty")
        
        try:
            
            conn, cursor = self.create_session()
            cursor.execute("SELECT value FROM kv_store WHERE key = ?", (key,))
            query_result = cursor.fetchone()
            conn.close()
            
            if not query_result:
                log.info(f"Key not found")
                return None
            
            result = pickle.loads(query_result[0]) # converts from bytes to the original object
    
            log.info(f"Value retrieved successfully")
            
            return result
        
        except sqlite3.Error as e:
            log.error(f"Error getting value: {e}")
            raise KVStoreError("get", str(e), key)
        except Exception as e:
            log.error(f"Error deserializing value: {e}")
            raise KVStoreError("get", f"Failed to deserialize value: {str(e)}", key)
    
    
    def put(self, key: str, value: Any) -> None:
        """
        Put a value into the database
        
        Args:
            key: The key to put the value for
            value: The value to put into the database
        """
        
        if not key:
            log.info(f"Key cannot be empty")
            raise KVStoreError("put", "Key cannot be empty")

        
        try:
            conn, cursor = self.create_session()
            value_bytes = pickle.dumps(value) # converts the value to bytes
            
            cursor.execute("INSERT INTO kv_store (key, value) VALUES (?, ?)", (key, value_bytes))
            conn.commit()
            conn.close()
            log.info(f"Value put successfully")
            
        except sqlite3.Error as e:
            log.error(f"Error putting value: {e}")
            raise KVStoreError("put", str(e), key)
        except Exception as e:
            log.error(f"Error serializing value: {e}")
            raise KVStoreError("put", f"Failed to serialize value: {str(e)}", key)
            
    
    
    def update(self, key: str, value: Any) -> None:
        """
        Update a value in the database
        
        Args:
            key: The key to update the value for
            value: The value to update in the database
        
        Returns:
            None
        """
        
        if not key:
            log.info(f"Key cannot be empty")
            raise KVStoreError("update", "Key cannot be empty")
        
        try:
            conn, cursor = self.create_session()
            value_bytes = pickle.dumps(value)
            cursor.execute("UPDATE kv_store SET value = ? WHERE key = ?", (value_bytes, key))
            
            if cursor.rowcount == 0:
                raise KVStoreError("update", "Key does not exist", key)
            
            conn.commit()
            conn.close()
        
        except sqlite3.Error as e:
            log.error(f"Error updating value: {e}")
            raise KVStoreError("update", str(e), key)
        except Exception as e:
            log.error(f"Error serializing value: {e}")
            raise KVStoreError("update", f"Failed to serialize value: {str(e)}", key)
    
    
    
    def delete(self, key: str) -> None:
        """
        Delete a kv pair from the database
        
        Args:
            key: The key to delete the value for
        
        Returns:
            None
        """
        if not key:
            log.info(f"Key cannot be empty")
            raise KVStoreError("delete", "Key cannot be empty")
        
        try:
            conn, cursor = self.create_session()
            cursor.execute("DELETE FROM kv_store WHERE key = ?", (key,))
            
            if cursor.rowcount == 0:
                raise KVStoreError("delete", "Key does not exist", key)
                
            conn.commit()
            conn.close()
        
        except sqlite3.Error as e:

            log.error(f"Error deleting value: {e}")
            raise KVStoreError("delete", str(e), key)
            
            
    
        
            

        
