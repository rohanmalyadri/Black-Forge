import argparse
import sys
from pydantic import ValidationError
from runner import run_experiment

def main():
    parser = argparse.ArgumentParser(description="AutoReason Marketing Copy Optimizer")
    parser.add_argument("--goal", type=str, required=True, help="The marketing goal/context (e.g., 'Launch a new AI tool')")
    parser.add_argument("--platform", type=str, choices=["X/Twitter", "LinkedIn", "Instagram"], required=True, help="Target platform")
    parser.add_argument("--draft", type=str, required=False, help="Initial draft of the copy. If not provided, you will be prompted.")
    parser.add_argument("--max_rounds", type=int, default=5, help="Maximum number of rounds to run before terminating.")
    
    args = parser.parse_args()
    
    draft = args.draft
    if not draft:
        print("Please enter your initial draft (Press Enter twice to submit):")
        lines = []
        while True:
            line = sys.stdin.readline()
            if line == '\n':
                break
            lines.append(line)
        draft = "".join(lines).strip()
    
    if not draft:
        print("Error: No initial draft provided.")
        return

    try:
        run_experiment(args.goal, args.platform, draft, args.max_rounds)
    except Exception as e:
        print(f"An error occurred during execution: {e}")

if __name__ == "__main__":
    main()
