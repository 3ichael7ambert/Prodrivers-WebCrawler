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
    // document.addEventListener("DOMContentLoaded", function () {
    //     const loginForm = document.getElementById("login-form");
    //     const registerForm = document.getElementById("register-form");
    //     const toggleButton = document.getElementById("toggle-form");

    //     toggleButton.addEventListener("click", function () {
    //         loginForm.style.display = loginForm.style.display === "none" ? "block" : "none";
    //         registerForm.style.display = registerForm.style.display === "none" ? "block" : "none";

    //         if (loginForm.style.display === "none") {
    //             toggleButton.textContent = "Switch to Register";
    //         } else {
    //             toggleButton.textContent = "Switch to Login";
    //         }
    //     });
    // });