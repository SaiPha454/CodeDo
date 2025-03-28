# import sys

# Add the pyslibs directory to the Python path
# sys.path.append('../pyslibs')

import js
from js import console, alert
from pyscript import document
from pyodide.http import pyfetch
from pyodide.ffi import create_proxy

console.log("Signup script loaded")

async def handle_signup(event):
    try:
        event.preventDefault()  # Prevent the default form submission behavior
        console.log("Handling signup event")

        # Collect form data
        form = document.getElementById("signup-form")
        username = form.querySelector("#username").value
        email = form.querySelector("#email").value
        password = form.querySelector("#password").value

        console.log(f"Collected data: username={username}, email={email}, password={password}")

        # Debugging: Log the Proxy object
        console.log("Event object:", event)
        console.log("Form object:", form)
        console.log("Proxy object:", username, email, password)

        # Ensure values are strings
        username = str(username)
        email = str(email)
        password = str(password)

        # Prepare request body
        body = f"username={js.encodeURIComponent(username)}&email={js.encodeURIComponent(email)}&password={js.encodeURIComponent(password)}"
        console.log("Request body:", body)

        # Send POST request to the server using pyfetch
        response = await pyfetch(
            url="/signup",  # Ensure the correct endpoint is used
            method="POST",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            body=body
        )
        console.log("Fetch response received")

        # Read response body
        response_text = await response.text()
        console.log("Response text:", response_text)
        alert(f"Response from server: {response_text}")

        if response.ok:
            try:
                result = js.JSON.parse(response_text)  # Parse JSON manually
                console.log("Signup successful:", result)
                alert("Signup successful!")
            except Exception as e:
                console.log("Failed to parse JSON:", e)
                alert(f"Unexpected response format: {response_text}")
        else:
            console.log("Signup failed with status:", response.status)
            alert(f"Signup failed: {response.status}\n{response_text}")
    except Exception as e:
        console.log("Error during signup:", e)
        alert(f"Error during signup: {e}")

# Attach the event listener to the form
form = document.getElementById("signup-form")
form.addEventListener("submit", create_proxy(handle_signup))
