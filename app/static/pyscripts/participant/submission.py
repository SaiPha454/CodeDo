from js import console, document, window, fetch, Object
import json

async def submit_code(event):
    problem_id = event.currentTarget.getAttribute("data-problem_id")
    challenge_id = event.currentTarget.getAttribute("data-challenge_id")
    code_str = window.editor.getValue()

    # Prepare the payload
    payload = {
        "problem_id": problem_id,
        "challenge_id": challenge_id,
        "code": code_str
    }
    headers = Object.create(None)
    headers["Content-Type"] = "application/json"
    # Send the POST request to the API
    response = await fetch("/participants/submissions", {
        "method": "POST",
        "headers": headers,
        "body": json.dumps(payload)
    })
    if response.ok:
        # Parse the response JSON
        data = await response.json()
        submission_id = data["submission_id"]
        console.log(submission_id)
        window.location.href = f"/participants/submissions/{submission_id}/report"
    else:
        console.error("Failed to submit code")

