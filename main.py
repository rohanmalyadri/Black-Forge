import argparse
import sys
from black_forge.branding import APP_NAME, CREDIT, has_api_key, print_banner, print_footer, print_missing_key

def main():
    parser = argparse.ArgumentParser(
        description=f"{APP_NAME} AutoReason Marketing Copy Optimizer",
        epilog=CREDIT,
    )
    parser.add_argument("--goal", type=str, required=True, help="The marketing goal/context (e.g., 'Launch a new AI tool')")
    parser.add_argument("--platform", type=str, choices=["X/Twitter", "LinkedIn", "Instagram"], required=True, help="Target platform")
    parser.add_argument("--draft", type=str, required=False, help="Initial draft of the copy. If not provided, you will be prompted.")
    parser.add_argument("--max_rounds", type=int, default=5, help="Maximum number of rounds to run before terminating.")
    
    args = parser.parse_args()
    print_banner("AutoReason Marketing Copy Optimizer")
    if not has_api_key():
        print_missing_key()
        sys.exit(1)

    draft = args.draft
    if not draft:
        print("Please enter your initial draft (Press Enter twice to submit):")
        lines = []
        while True:
            line = sys.stdin.readline()
            if line in ('\n', ''):  # blank line or EOF
                break
            lines.append(line)
        draft = "".join(lines).strip()
    
    if not draft:
        print("Error: No initial draft provided.")
        return

    try:
        # Imported here so --help and the API-key check work before the LLM clients are built
        from runner import run_experiment
        run_experiment(args.goal, args.platform, draft, args.max_rounds)
    except Exception as e:
        print(f"An error occurred during execution: {e}")
        sys.exit(1)
    finally:
        print_footer()

if __name__ == "__main__":
    main()
