const form = document.getElementById("registerForm");
const password = document.getElementById("password");
const confirmPassword = document.getElementById("confirmPassword");
const message = document.getElementById("message");

form.addEventListener("submit", async function (event) {
  event.preventDefault();

  message.className = "";

  if (password.value !== confirmPassword.value) {
    message.textContent = "Passwords do not match.";
    message.classList.add("error");
    confirmPassword.focus();
    return;
  }

  try {
    const response = await fetch("/register", {
      method: "POST",
      body: new FormData(form),
    });

    if (response.ok) {
      message.textContent = "Registration successful!";
      message.classList.add("success");
      form.reset();
    } else {
      message.textContent = "Registration failed.";
      message.classList.add("error");
    }
  } catch (err) {
    message.textContent = "Could not connect to server.";
    message.classList.add("error");
  }
});
