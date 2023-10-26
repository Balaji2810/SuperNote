const loginTab = document.getElementById("loginTab");
const signupTab = document.getElementById("signupTab");
const loginForm = document.getElementById("loginForm");
const signupForm = document.getElementById("signupForm");
const errorMessage = document.getElementById("errorMessage");

if (getCookie('token'))
{
    window.location.href='/'
}


loginTab.addEventListener("click", () => {
    loginTab.classList.add("active");
    signupTab.classList.remove("active");
    loginForm.style.display = "block";
    signupForm.style.display = "none";
    errorMessage.textContent = "";
});

signupTab.addEventListener("click", () => {
    loginTab.classList.remove("active");
    signupTab.classList.add("active");
    loginForm.style.display = "none";
    signupForm.style.display = "block";
    errorMessage.textContent = "";
});

loginForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const loginUsername = document.getElementById("loginUsername").value;
    const loginPassword = document.getElementById("loginPassword").value;
    // Add your login validation logic here
    // For a simple example, check if the fields are not empty
    if (loginUsername.trim() === "" || loginPassword.trim() === "") {
        errorMessage.textContent = "Username and password are required.";
    } else {
        const postData = { username: loginUsername.trim(), password: loginPassword.trim()};
        apiRequest('POST', "/api/login", postData)
        .then(data => {
            console.log('POST:', data);
            
            window.location.href="/index.html"
        })
        .catch(error => {
            console.error('POST error:', error);
        });
        
        errorMessage.textContent = "Login successful!";
    }
});

signupForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const signupUsername = document.getElementById("signupUsername").value;
    const signupPassword = document.getElementById("signupPassword").value;
    // Add your signup validation logic here
    // For a simple example, check if the fields are not empty
    if (signupUsername.trim() === "" || signupPassword.trim() === "") {
        errorMessage.textContent = "Username and password are required.";
    } else {
        const postData = { username: signupUsername.trim(), password: signupPassword.trim()};
        apiRequest('POST', "/api/signup", postData)
        .then(data => {
            console.log('POST:', data);
            
            window.location.href="/login.html"
        })
        .catch(error => {
            console.error('POST error:', error);
        });
        errorMessage.textContent = "Signup successful!";
    }
});
