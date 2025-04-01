from js import document, console, fetch, Object, window
import json

console.log("Loading problem_creation_form.py")

def create_problem(event):
    event.preventDefault()
    challenge_id = event.currentTarget.getAttribute('data-challenge-id')
    console.log("Challenge ID:", challenge_id)
    # Get form inputs
    title_input = document.getElementById('title')
    statement_input = document.getElementById('statement')
    input_format_input = document.getElementById('input')
    output_format_input = document.getElementById('output')
    error_message_div = document.getElementById('error-message')

    if not title_input or not statement_input or not input_format_input or not output_format_input:
        console.log("Error: One or more form fields are missing.")
        return

    # Validate required fields
    if not title_input.value.strip():
        error_message_div.textContent = "Error: Title is required."
        error_message_div.style.display = "block"
        return
    if not statement_input.value.strip():
        error_message_div.textContent = "Error: Problem statement is required."
        error_message_div.style.display = "block"
        return
    if not input_format_input.value.strip():
        error_message_div.textContent = "Error: Input format is required."
        error_message_div.style.display = "block"
        return
    if not output_format_input.value.strip():
        error_message_div.textContent = "Error: Output format is required."
        error_message_div.style.display = "block"
        return

    # Collect form data
    form_data = {
        "challenge_id": challenge_id,  # Use the passed challenge_id
        "title": title_input.value,
        "problem_definition": statement_input.value.replace("\n", "\\n"),  # Preserve newlines
        "input_format": input_format_input.value.replace("\n", "\\n"),
        "output_format": output_format_input.value.replace("\n", "\\n")
    }

    # Define success and error handlers
    def on_success(response):
        console.log(response.status)
        if response.status == 303 or response.status == 200:
            console.log("Success:", response.url)
            window.location.href = response.url
        elif response.status == 404:
            error_message_div.textContent = "Error: Challenge not found."
            error_message_div.style.display = "block"
        else:
            response.text().then(lambda text: setattr(error_message_div, 'textContent', text))
            error_message_div.style.display = "block"

    def on_error(error):
        error_message_div.textContent = 'Failed to create problem: ' + str(error)
        error_message_div.style.display = "block"

    # Create headers using Object from js
    headers = Object.create(None)
    headers['Content-Type'] = 'application/json'

    # Send POST request
    fetch(f"/questioners/challenges/{challenge_id}/problems/", {
        'method': 'POST',
        'headers': headers,
        'body': json.dumps(form_data)
    }).then(on_success).catch(on_error)

def confirm_delete_problem(event):
    # Define success and error handlers
    modal = document.getElementById('deleteProblemModal')
    
    challenge_id = modal.getAttribute('data-challenge-id')
    problem_id = modal.getAttribute('data-problem-id')
    error_message = document.getElementById('deleteProblemError')
    error_message.style.display = "none"  # Hide the error message initially
    
    def on_success(response):
        if response.status == 303 or response.status == 200:
            window.location.href = f"/questioners/challenges/{challenge_id}/problems"
        else:
            error_message.style.display = "block"
            error_message.textContent = "Failed to delete problem. Please try again later."

    def on_error(error):
        error_message.style.display = "block"
        error_message.textContent = f"Error deleting problem: {error}"

    # Create headers using Object from js
    headers = Object.create(None)
    headers['Content-Type'] = 'application/json'
    
    # Send DELETE request
    fetch(f"/questioners/challenges/{challenge_id}/problems/{problem_id}", {
        'method': 'DELETE',
        'headers': headers
    }).then(on_success).catch(on_error)

def update_problem(event):
    # Prevent default form submission
    console.log("Loading update_problem.py")

    # Get problem and challenge IDs from the button's data attributes
    button = event.currentTarget
    problem_id = button.getAttribute('data-problem-id')
    challenge_id = button.getAttribute('data-challenge-id')

    # Get form inputs
    title_input = document.getElementById('title')
    statement_input = document.getElementById('statement')
    input_format_input = document.getElementById('input')
    output_format_input = document.getElementById('output')
    error_message_div = document.getElementById('error-message')

    # Validate required fields
    if not title_input.value.strip():
        error_message_div.textContent = "Error: Title is required."
        error_message_div.style.display = "block"
        return
    if not statement_input.value.strip():
        error_message_div.textContent = "Error: Problem statement is required."
        error_message_div.style.display = "block"
        return
    if not input_format_input.value.strip():
        error_message_div.textContent = "Error: Input format is required."
        error_message_div.style.display = "block"
        return
    if not output_format_input.value.strip():
        error_message_div.textContent = "Error: Output format is required."
        error_message_div.style.display = "block"
        return

    # Collect form data
    form_data = {
        "title": title_input.value,
        "problem_definition": statement_input.value.replace("\n", "\\n"),
        "input_format": input_format_input.value.replace("\n", "\\n"),
        "output_format": output_format_input.value.replace("\n", "\\n")
    }

    # Define success and error handlers
    def on_success(response):
        if response.status == 303 or response.status == 200:
            window.location.href = f"/questioners/challenges/{challenge_id}/problems"
        else:
            response.text().then(lambda text: setattr(error_message_div, 'textContent', text))
            error_message_div.style.display = "block"

    def on_error(error):
        error_message_div.textContent = f"Failed to update problem: {error}"
        error_message_div.style.display = "block"

    # Create headers using Object from js
    headers = Object.create(None)
    headers['Content-Type'] = 'application/json'

    # Send PUT request
    fetch(f"/questioners/challenges/{challenge_id}/problems/{problem_id}/", {
        'method': 'PUT',
        'headers': headers,
        'body': json.dumps(form_data)
    }).then(on_success).catch(on_error)