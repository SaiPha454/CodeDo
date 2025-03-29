from js import document

def show_modal(event):
    modal = document.getElementById('createModal')
    modal.classList.add('show')

def hide_modal(event):
    modal = document.getElementById('createModal')
    challenge_nameInput = document.getElementById('challengeName')
    challenge_nameInput.value = ''
    modal.classList.remove('show')