async function add() {
  const res = await fetch("http://127.0.0.1:8000/add-question", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      question: q.value,
      description: d.value,
      options: [o1.value, o2.value, o3.value, o4.value],
      correct_answer: c.value
    })
  });

  alert("Đã thêm");
}

async function loadScores() {
  const res = await fetch("http://127.0.0.1:8000/scores");
  const data = await res.json();

  let html = "";
  data.forEach(s => {
    html += `<p>${s.username}: ${s.score}/${s.total}</p>`;
  });

  document.getElementById("scores").innerHTML = html;
}

loadScores();