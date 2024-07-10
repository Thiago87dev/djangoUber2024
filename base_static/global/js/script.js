const messages = document.querySelectorAll('.message')

messages.forEach((message)=>{
    setTimeout(() => {
        message.style.transition = 'opacity 0.5s ease-out'
        message.style.opacity = '0'
        setTimeout(()=> message.remove(),500)
    }, 2500);
})

const btnDelete = document.querySelector('[data-js="btn-delete"]')
const deleteForm = document.querySelector('[data-js="delete-form"]')

btnDelete.addEventListener('click',(e)=>{
    e.preventDefault()
    const confirmation = confirm("Are you sure ? This action is irreversible.")
    if(confirmation){
        deleteForm.submit()
    }
})