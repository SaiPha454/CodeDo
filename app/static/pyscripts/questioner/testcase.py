from js import document, console, fetch, Object, window
import json

# def add_parameter(event):
#     test_case_id = event.currentTarget.getAttribute('data-test-case-id')
#     params_container_id = f"test-case-{test_case_id}-params"
#     params_container = document.getElementById(params_container_id)
#     new_param_id = params_container.children.length + 1

#     # Create a new parameter row
#     new_param = document.createElement("div")
#     new_param.className = "parameter-row"
#     new_param.innerHTML = f"""
#         <div class='parameter-value'>
#             <label>Parameter {new_param_id}</label>
#             <input type='text' placeholder='e.g. [1, 2, 3], 10, 5'>
#         </div>
#         <button class='remove-param-button' mpy-click='remove_parameter'>
#             <svg width='16' height='16' viewBox='0 0 16 16' fill='none'>
#                 <path d='M2.667 4H13.334M12 4V13.333C12 13.702 11.702 14 11.334 14H4.667C4.299 14 4 13.702 4 13.333V4M6 4V2.667C6 2.298 6.299 2 6.667 2H9.334C9.702 2 10 2.298 10 2.667V4' stroke='currentColor' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'/>
#             </svg>
#         </button>
#     """
#     params_container.appendChild(new_param)

# def remove_parameter(event):
#     button = event.currentTarget
#     parameter_row = button.closest(".parameter-row")
#     params_container = parameter_row.parentElement
#     parameter_row.remove()

#     # Reassign IDs to remaining parameters
#     for index, param in enumerate(params_container.children):
#         label = param.querySelector(".parameter-value label")
#         if label:
#             label.textContent = f"Parameter {index + 1}"

def add_test_case(event):
    test_cases_container = document.getElementById("test-cases-container")
    # problem_id = event.currentTarget.getAttribute('data-problem-id')

    # Assign a new unique test case ID within the scope of the problem
    new_test_case_id = test_cases_container.children.length + 1

    # Create a new test case card
    new_test_case = document.createElement("div")
    new_test_case.className = "test-case-card"
    new_test_case.id = f"test-case-{new_test_case_id}"

    new_test_case.innerHTML = f"""
        <div class='test-case-header'>
            <h3 class='test-case-title'>Test Case {new_test_case_id}</h3>
            <button class='remove-button' mpy-click='remove_test_case'>
                <svg width='16' height='16' viewBox='0 0 16 16' fill='none'>
                    <path d='M2.667 4H13.334M12 4V13.333C12 13.702 11.702 14 11.334 14H4.667C4.299 14 4 13.702 4 13.333V4M6 4V2.667C6 2.298 6.299 2 6.667 2H9.334C9.702 2 10 2.298 10 2.667V4' stroke='currentColor' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'/>
                </svg>
                Remove
            </button>
        </div>
        <div class='parameters-section'>
            <div class='parameter-value'>
                <label>Input</label>
                <textarea class='testcase-input' type='text' placeholder='e.g. [1, 2, 3], 10, 5'></textarea>
            </div>
        </div>
        <div class='output-section'>
            <label>Expected Output</label>
            <textarea class='testcase-output' placeholder='Enter expected output...'></textarea>
        </div>
    """
    test_cases_container.appendChild(new_test_case)

def remove_test_case(event):
    button = event.currentTarget
    test_case_card = button.closest(".test-case-card")
    test_cases_container = test_case_card.parentElement
    test_case_card.remove()
    problem_id = event.currentTarget.getAttribute('data-problem-id')
    # Reassign IDs to remaining test cases
    for index, test_case in enumerate(test_cases_container.children):
        # problem_id = document.getElementById("problem-id").value
        test_case.id = f"test-case-{index + 1}"
        title = test_case.querySelector(".test-case-title")
        if title:
            title.textContent = f"Test Case {index + 1}"

        # Update data-test-case-id for add-param-button
        add_param_button = test_case.querySelector(".add-param-button")
        if add_param_button:
            add_param_button.setAttribute("data-test-case-id", f"{index + 1}")
            # add_param_button.setAttribute("data-problem-id", problem_id)

        # Update parameters section ID
        params_section = test_case.querySelector(".parameter-inputs")
        if params_section:
            params_section.id = f"test-case-{index + 1}-params"

def submit_test_cases(event):
    test_cases = []
    test_cases_container = document.getElementById("test-cases-container")
    problem_id = event.currentTarget.getAttribute('data-problem-id')

    for test_case in test_cases_container.children:
        test_case_id = test_case.id.split("-")[2]

        params_input = test_case.querySelector(".testcase-input").value
        expected_output = test_case.querySelector(".testcase-output").value
        test_cases.append({
            "id": int(test_case_id),
            "input_data": params_input,
            "expected_output": expected_output
        })
    # Prepare the payload
    payload = {
        "problem_id": int(problem_id),
        "test_cases": test_cases
    }
    console.log("Payload:", payload)
    payload = json.dumps(payload)
    headers = Object.create(None)
    headers["Content-Type"] = "application/json"

    def on_success(response):
        if response.url:
            window.location.href = response.url
    # Send the data to the backend
    fetch("./", {
        "method": "POST",
        "headers": headers,
        "body": json.dumps(test_cases)
    }).then(on_success).catch(lambda error: console.error("Error:", error))