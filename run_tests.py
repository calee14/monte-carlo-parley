import os
import sys
import subprocess
import argparse


def run_specific_test(test_path):
    """Run a specific test module or file."""
    module_path = test_path.replace("/", ".").replace(".py", "")
    if module_path.endswith("."):
        module_path = module_path[:-1]

    print(f"Running test: {module_path}")
    result = subprocess.run([sys.executable, "-m", module_path])
    return result.returncode


def run_all_tests():
    """Run all tests in the tests directory."""
    print("Running all tests...")
    test_failures = 0

    # Walk through the tests directory
    for root, _, files in os.walk("tests"):
        for file in files:
            if file.startswith("test_") or file.endswith("_test.py"):
                if file != "__init__.py":
                    # Convert path to module format
                    rel_path = os.path.join(root, file)
                    test_failures += run_specific_test(rel_path)

    return test_failures


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run tests for monte-carlo-parley")
    parser.add_argument(
        "test_path", nargs="?", help="Specific test to run (e.g., tests/hand_test.py)"
    )

    args = parser.parse_args()

    if args.test_path:
        exit_code = run_specific_test(args.test_path)
    else:
        exit_code = run_all_tests()

    if exit_code:
        print("\n❌ Some tests failed")
    else:
        print("\n✅ All tests passed!")

    sys.exit(exit_code)
