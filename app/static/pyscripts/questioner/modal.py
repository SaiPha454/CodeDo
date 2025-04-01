from js import document, console, fetch, Object, window
import json
# Show the modal
def show_create_challenge_modal(event):
    modal = document.getElementById('createModal')
    modal.classList.add('show')

# Hide the modal
def hide_create_challenge_modal(event):
    modal = document.getElementById('createModal')
    challenge_name = document.getElementById('challenge_name')
    challenge_name.value = ''
    modal.classList.remove('show')


def show_delete_challenge_modal(event):
    modal = document.getElementById('deleteChallengeModal')
    modal.setAttribute('data-challenge-id', event.currentTarget.getAttribute('data-challenge-id'))
    modal.classList.add('show')

def hide_delete_challenge_modal(event):
    modal = document.getElementById('deleteChallengeModal')
    modal.classList.remove('show')