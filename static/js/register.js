const username = document.getElementById('username')
const email = document.getElementById('email')


username.addEventListener('keyup', (e) => {
    const username = e.target.value;

    // reset
    e.target.classList.remove('is-invalid');
    e.target.nextElementSibling.innerText = '';

    fetch('/authentication/validate-username', {
        method:'POST',
        body:JSON.stringify({username})
    }).then((res) => res.json()).then((data) => {
        if (data.status == 'error') {
            e.target.classList.add('is-invalid');
            e.target.nextElementSibling.innerText = data.msg;
        }
    })
})


email.addEventListener('keyup', (e) => {
    const email = e.target.value;

    // reset
    e.target.classList.remove('is-invalid');
    e.target.nextElementSibling.innerText = '';

    fetch('/authentication/validate-email', {
        method:'POST',
        body:JSON.stringify({email})
    }).then((res) => res.json()).then((data) => {
        if (data.status == 'error') {
            e.target.classList.add('is-invalid');
            e.target.nextElementSibling.innerText = data.msg;
        }
    })
})