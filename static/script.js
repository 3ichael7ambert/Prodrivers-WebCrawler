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


