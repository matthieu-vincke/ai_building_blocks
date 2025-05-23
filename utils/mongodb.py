import os
from pymongo import MongoClient

def delete_all_documents(
    db_name: str,
    collection_name: str,
    connection_string: str = None,
) -> int:
    """
    Deletes all documents from the specified MongoDB collection.

    Args:
        connection_string (str): MongoDB connection URI. Falls back to `MONGO_CONNECTION_STRING` env var.
        db_name (str): Database name. Falls back to `MONGO_DB` env var.
        collection_name (str): Collection name. Falls back to `MONGO_COLLECTION` env var.

    Returns:
        int: Number of documents deleted.
    """
    connection_string = connection_string or os.getenv("MONGO_CONNECTION_STRING")
    db_name = db_name # Don't use env var for db_name to avoid unintended deletions...
    collection_name = collection_name  # Don't use env var for db_name to avoid unintended deletions...

    if not connection_string or not db_name or not collection_name:
        raise ValueError("Missing connection string, DB name, or collection name.")

    client = MongoClient(connection_string)
    collection = client[db_name][collection_name]

    result = collection.delete_many({})
    return result.deleted_count
