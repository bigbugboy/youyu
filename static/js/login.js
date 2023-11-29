const eyeIcon = document.getElementById('hide-password');
const pwdInput = document.getElementById('password');

eyeIcon.addEventListener('click', (e) => {
    let type = pwdInput.getAttribute('type')
    if (type === 'password') {
        pwdInput.setAttribute('type', 'text')
        eyeIcon.setAttribute('src', '/static/img/eye_off.svg')
    } else {
        pwdInput.setAttribute('type', 'password')
        eyeIcon.setAttribute('src', '/static/img/eye.svg')
    }
})