import sys
import io
import multiprocessing
import asyncio

def execute_code(user_code, input_data, expected_output, result_queue):
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
            result_queue.put({"status": "Pass", "output": output})
        else:
            result_queue.put({"status": "Fail", "output": output, "expected": expected_output})
    except Exception as e:
        # Handle any other exceptions during execution
        result_queue.put({"status": "Error", "error": str(e)})
    finally:
        # Restore stdin and stdout
        sys.stdin = stdin_backup
        sys.stdout = stdout_backup

def process_target(user_code, input_data, expected_output, result_queue):
    execute_code(user_code, input_data, expected_output, result_queue)

class CodeEvaluationService:
    @staticmethod
    async def evaluate_code(user_code: str, test_cases: list):
        results = []

        async def run_in_process(user_code, input_data, expected_output):
            loop = asyncio.get_event_loop()
            result_queue = multiprocessing.Queue()

            # Create a process
            process = multiprocessing.Process(
                target=process_target, args=(user_code, input_data, expected_output, result_queue)
            )
            process.start()

            try:
                # Wait for the process to complete with a timeout
                await loop.run_in_executor(None, process.join, 5)

                if process.is_alive():
                    # Terminate the process if it exceeds the timeout
                    process.terminate()
                    process.join()
                    return {"status": "Error", "error": "Execution time exceeded 5 seconds"}
                else:
                    # Get the result from the queue
                    return result_queue.get()
            finally:
                process.close()

        # Schedule all test cases to run concurrently
        tasks = [run_in_process(user_code, test_case.input_data, test_case.expected_output) for test_case in test_cases]
        results = await asyncio.gather(*tasks)

        # Prepare detailed report for each test case
        detailed_results = []
        for i, result in enumerate(results):
            test_case = test_cases[i]
            detailed_results.append({
                "test_case": {
                    "input": test_case.input_data,
                    "expected_output": test_case.expected_output
                },
                "result": result
            })

        return detailed_results
