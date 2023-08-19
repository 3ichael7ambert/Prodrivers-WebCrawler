    // Get the login and dashboard link elements
    const loginLink = document.getElementById('login-link');
    const dashboardLink = document.getElementById('dashboard-link');

    // Check if the user is authenticated and adjust the visibility of links accordingly
    if (isAuthenticated) {
        loginLink.style.display = 'none';
        dashboardLink.style.display = 'block';
    } else {
        loginLink.style.display = 'block';
        dashboardLink.style.display = 'none';
    }





    // LOGIN REGISTER
    document.addEventListener('DOMContentLoaded', function () {
        const loginForm = document.getElementById('login-form');
        const registerForm = document.getElementById('register-form');
        const toggleButton = document.getElementById('toggle-form');
        
        let login = {% if login %}true{% else %}false{% endif %};
    
        toggleButton.addEventListener('click', function () {
            login = !login;
            
            if (login) {
                loginForm.style.display = 'block';
                registerForm.style.display = 'none';
                toggleButton.textContent = 'Switch to Register';
            } else {
                loginForm.style.display = 'none';
                registerForm.style.display = 'block';
                toggleButton.textContent = 'Switch to Login';
            }
        });
    });