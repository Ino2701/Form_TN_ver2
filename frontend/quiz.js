let questions = [];

async function load() {
  const res = await fetch("http://127.0.0.1:8000/questions");
  questions = await res.json();

  let html = "";

  questions.forEach(q => {
    html += `<p>${q.question}</p>`;
    q.options.forEach(opt => {
      html += `<input type="radio" name="q${q.id}" value="${opt}">${opt}<br>`;
    });
  });

  document.getElementById("quiz").innerHTML = html;
}

async function submitQuiz() {
  const user = JSON.parse(localStorage.getItem("user"));

  const answers = questions.map(q => {
    const selected = document.querySelector(`input[name="q${q.id}"]:checked`);
    return {
      question_id: q.id,
      selected_answer: selected ? selected.value : ""
    };
  });

  const res = await fetch("http://127.0.0.1:8000/submit", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      username: user.username,
      answers
    })
  });

  const data = await res.json();

  document.getElementById("result").innerText =
    `Điểm: ${data.score}/${data.total}`;
}

load();