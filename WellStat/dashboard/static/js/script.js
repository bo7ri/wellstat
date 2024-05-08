document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const doctorId = document.getElementById('doctorId').value;
    const password = document.getElementById('password').value;
    console.log('Doctor ID:', doctorId, 'Password:', password);
    // Add your login logic here
});
