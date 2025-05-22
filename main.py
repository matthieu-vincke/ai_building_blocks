import argparse
import importlib.util
import os
import sys

def run_script(script_path):
    # Ensure project root is in PYTHONPATH
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    if not os.path.isfile(script_path):
        print(f"❌ Script not found: {script_path}")
        sys.exit(1)

    spec = importlib.util.spec_from_file_location("example_module", script_path)
    example = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(example)

def main():
    parser = argparse.ArgumentParser(description="Run example scripts with proper environment setup.")
    parser.add_argument(
        "script",
        help="Path to the script (e.g. examples/embeddings_mongodb.py)"
    )
    args = parser.parse_args()

    run_script(args.script)

if __name__ == "__main__":
    main()
