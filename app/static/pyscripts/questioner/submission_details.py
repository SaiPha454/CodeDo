from js import document, console


console.log('Loading submission_details.py')

code_tab = document.getElementById('codeTab')
test_tab = document.getElementById('testTab')
code_content = document.getElementById('codeContent')
test_content = document.getElementById('testContent')

def activate_code_tab(event):
    code_tab.classList.add('active')
    test_tab.classList.remove('active')
    code_content.style.display = 'block'
    test_content.style.display = 'none'

def activate_test_tab(event):
    test_tab.classList.add('active')
    code_tab.classList.remove('active')
    test_content.style.display = 'block'
    code_content.style.display = 'none'


 


