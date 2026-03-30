async function login() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const res = await fetch("http://127.0.0.1:8000/login", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ username, password })
  });

  const data = await res.json();

  if (data.role === "admin") {
    localStorage.setItem("user", JSON.stringify(data));
    window.location.href = "admin.html";
  } else if (data.role === "user") {
    localStorage.setItem("user", JSON.stringify(data));
    window.location.href = "quiz.html";
  } else {
    document.getElementById("msg").innerText = "Sai tài khoản";
  }
}