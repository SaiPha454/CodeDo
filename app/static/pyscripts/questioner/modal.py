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



def show_delete_problem_modal(event):
    modal = document.getElementById('deleteProblemModal')
    problem_id = event.currentTarget.getAttribute('data-problem-id')
    challenge_id = event.currentTarget.getAttribute('data-challenge-id')
    console.log("Problem ID:", problem_id)
    console.log("Challenge ID:", challenge_id)
    if not problem_id:
        console.log("Error: Problem ID not found.")
        return
    if not challenge_id:
        console.log("Error: Challenge ID not found.")
        return
    # Set the challenge ID in the modal
    modal.setAttribute('data-problem-id', problem_id)
    modal.setAttribute('data-challenge-id', challenge_id)
    modal.classList.add('show')

def hide_delete_problem_modal(event):
    modal = document.getElementById('deleteProblemModal')
    modal.removeAttribute('data-problem-id')
    modal.removeAttribute('data-challenge-id')
    modal.classList.remove('show')