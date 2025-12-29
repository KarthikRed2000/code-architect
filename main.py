import argparse
import os
from core.parser import parse_codebase
from core.database import store_code_in_db
from core.orchestrator import RefactorOrchestrator
import chromadb
from dotenv import load_dotenv

load_dotenv()

# export GEMINI_KEY="your_key_here"
GEMINI_KEY = os.getenv("GEMINI_KEY") 
DB_PATH = "./chroma_db"

def main():
    parser = argparse.ArgumentParser(description="CodeArchitect: AI-Powered LLD Refactorer")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 1. Index Command: python main.py index --path ./messy_project
    index_parser = subparsers.add_parser("index", help="Index a codebase into the Vector DB")
    index_parser.add_argument("--path", required=True, help="Path to the messy code directory")

    # 2. Refactor Command: python main.py refactor --query "User class" --pattern "Strategy"
    refactor_parser = subparsers.add_parser("refactor", help="Refactor a specific piece of code")
    refactor_parser.add_argument("--query", required=True, help="Search query to find the messy code")
    refactor_parser.add_argument("--pattern", default="Strategy Pattern", help="Design pattern to apply")

    args = parser.parse_args()

    # Initialize Chroma Client
    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_or_create_collection(name="codebase_index")

    if args.command == "index":
        print(f"🔍 Scanning codebase at {args.path}...")
        metadata = parse_codebase(args.path)
        if metadata:
            store_code_in_db(metadata, DB_PATH)
            print("✅ Indexing complete.")
        else:
            print("⚠️ No python files found or parsing failed.")

    elif args.command == "refactor":
        if not GEMINI_KEY:
            print("❌ Error: GEMINI_KEY environment variable not set.")
            return

        orchestrator = RefactorOrchestrator(collection, GEMINI_KEY)
        
        print(f"🤖 Searching for: '{args.query}'")
        print(f"🎨 Applying Pattern: {args.pattern}")
        
        # This triggers the Retrieval -> Gemini -> Linter -> Surgical Replace loop
        orchestrator.run_refactor_loop(args.query, args.pattern)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()