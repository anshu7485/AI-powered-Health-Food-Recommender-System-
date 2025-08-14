document.getElementById('signupForm').addEventListener('submit', function(e) {
    const password = document.querySelector('input[name="password"]').value;
    const confirm = document.querySelector('input[name="confirm_password"]').value;
    if (password !== confirm) {
        alert('Passwords do not match!');
        e.preventDefault();
    }
});
