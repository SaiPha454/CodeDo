from js import document, console, fetch, Object, window
import json
# Create a challenge
def create_challenge(event):
    event.preventDefault()
    title_input = document.getElementById('challenge_name')
    if not title_input:
        console.log("Error: Element with ID 'challenge_name' not found.")
        return
    title = title_input.value

    def on_success(response):
        response.text().then(lambda text: setattr(document.body, 'innerHTML', text))

    def on_error(error):
        console.log('Failed to create challenge')
        console.log(error)

    # Create headers using Object from js
    headers = Object.create(None)
    fetch('/questioners/challenges/', {
        'method': 'POST',
        'headers': headers,
        'body': title
    }).then(on_success).catch(on_error)


def confirm_delete_challenge(event):
    modal = document.getElementById('deleteChallengeModal')
    challenge_id = modal.getAttribute('data-challenge-id')
    error_message = document.getElementById('deleteChallengeError')
    if not challenge_id:
        console.log("Error: Challenge ID not found.")
        return

    def on_success(response):
        response.text().then(lambda text: setattr(document.body, 'innerHTML', text))

    def on_error(error):
        console.log('Failed to delete challenge')
        error_message.style.display = 'block'

    # Create headers using Object from js
    headers = Object.create(None)
    fetch(f'/questioners/challenges/{challenge_id}/', {
        'method': 'DELETE',
        'headers': headers
    }).then(on_success).catch(on_error)

    # Hide the modal after the request
    hide_delete_challenge_modal(event)


