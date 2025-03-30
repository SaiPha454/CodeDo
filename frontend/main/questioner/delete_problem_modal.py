from js import document, console
console.log("Loading delete_problem_modal.py")
def show_delete_modal(event):
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

def hide_delete_modal(event):
    modal = document.getElementById('deleteProblemModal')
    modal.removeAttribute('data-problem-id')
    modal.removeAttribute('data-challenge-id')
    modal.classList.remove('show')