const messages = document.querySelectorAll('.message')

messages.forEach((message)=>{
    setTimeout(() => {
        message.style.transition = 'opacity 0.5s ease-out'
        message.style.opacity = '0'
        setTimeout(()=> message.remove(),500)
    }, 2500);
})