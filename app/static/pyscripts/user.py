from js import document, console, fetch, Object
import json
console.log("PyScript loaded successfully!")
nameContainer = document.getElementById('nameContainer')
nameDisplay = document.getElementById('nameDisplay')
editNameBtn = document.getElementById('editNameBtn')
editControls = document.getElementById('editControls')
nameInput = document.getElementById('nameInput')
saveNameBtn = document.getElementById('saveNameBtn')

def start_editing(event):
    
    nameContainer.style.display = 'none'
    editControls.style.display = 'flex'
    nameInput.value = nameDisplay.textContent.strip()
    nameInput.focus()

async def save_changes(event):
    new_name = nameInput.value.strip()
    if new_name:
        headers = Object.create(None)
        response = await fetch('/me/profile', {
            'method': 'PUT',
            'headers': headers,
            'body': new_name
        })
        if response.ok:
            nameDisplay.textContent = new_name
            nameContainer.style.display = 'block'
            editControls.style.display = 'none'
        else:
            console.error("Failed to update name")