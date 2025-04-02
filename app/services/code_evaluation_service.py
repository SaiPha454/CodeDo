import sys
import io
import asyncio

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
                # Directly execute the user's code without restrictions for testing purposes
                exec(user_code, {})

                # Capture the output
                output = sys.stdout.getvalue().strip()

                # Compare the output with the expected output
                if output == expected_output.strip():
                    results.append({"status": "Pass", "output": output})
                else:
                    results.append({"status": "Fail", "output": output, "expected": expected_output})
            except Exception as e:
                # Handle any exceptions during execution
                results.append({"status": "Error", "error": str(e)})
            finally:
                # Restore stdin and stdout
                sys.stdin = stdin_backup
                sys.stdout = stdout_backup

        return results