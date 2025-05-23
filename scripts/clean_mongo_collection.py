import argparse
from dotenv import load_dotenv
from utils.logger import get_logger
from utils.mongodb import delete_all_documents

logger = get_logger(__name__)

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Setup argument parser
    parser = argparse.ArgumentParser(description="Delete all documents from a MongoDB collection")
    parser.add_argument("db_name", type=str, help="Database name")
    parser.add_argument("collection_name", type=str, help="Collection name")
    parser.add_argument("--connection_string", type=str, default=None, help="MongoDB connection string (optional)")
    args = parser.parse_args()

    # Call the function with command line arguments
    deleted = delete_all_documents(args.db_name, args.collection_name, args.connection_string)
    logger.info(f"✅ Deleted {deleted} documents.")

if __name__ == "__main__":
    main()
