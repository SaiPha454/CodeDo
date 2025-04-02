import sys
import io
import asyncio
import traceback

class TimeoutException(Exception):
    pass

class CodeEvaluationService:
    @staticmethod
    async def evaluate_code(user_code: str, test_cases: list):
        results = []

        for test_case in test_cases:
            input_data = test_case.input_data
            expected_output = test_case.expected_output

            # Redirect stdin and stdout
            stdin_backup = sys.stdin
            stdout_backup = sys.stdout
            sys.stdin = io.StringIO(input_data)
            sys.stdout = io.StringIO()

            try:
                # Create a safe execution environment
                safe_globals = {
                    "__builtins__": {**__builtins__},
                    "eval": None,  # Disable eval
                    "exec": None,  # Disable exec
                    "open": None,  # Disable file operations
                    "os": None,    # Disable os module
                }
                safe_globals["input"] = input

                # Execute the user's code
                exec(user_code, safe_globals)

                # Capture the output
                output = sys.stdout.getvalue().strip()

                # Compare the output with the expected output
                if output == expected_output.strip():
                    results.append({"status": "Pass", "output": output})
                else:
                    results.append({"status": "Fail", "output": output, "expected": expected_output})
            except Exception as e:
                # Handle any other exceptions during execution
                results.append({"status": "Error", "error": str(e)})
            finally:
                # Restore stdin and stdout
                sys.stdin = stdin_backup
                sys.stdout = stdout_backup

        return results