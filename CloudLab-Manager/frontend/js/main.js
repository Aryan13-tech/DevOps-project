const BACKEND_URL = "http://127.0.0.1:5000/analyze-error";

const analyzeBtn = document.getElementById("analyzeBtn");
const errorInput = document.getElementById("errorInput");
const explanation = document.getElementById("explanation");
const causes = document.getElementById("causes");
const solutions = document.getElementById("solutions");
const categoryBadge = document.getElementById("categoryBadge");

analyzeBtn.addEventListener("click", async () => {
  const errorText = errorInput.value.trim();
  if (!errorText) return alert("Enter an error message");

  analyzeBtn.disabled = true;
  analyzeBtn.textContent = "Analyzing...";
  categoryBadge.textContent = "Analyzing...";
  categoryBadge.className = "badge waiting";

  const res = await fetch(BACKEND_URL, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ error: errorText })
  });

  const data = await res.json();

  explanation.textContent = data.summary;
  categoryBadge.textContent = data.error_category;

  causes.innerHTML = data.why_it_happened.map(c => `<li>${c}</li>`).join("");
  solutions.innerHTML = data.how_to_fix.map(s => `<li>${s}</li>`).join("");

  analyzeBtn.disabled = false;
  analyzeBtn.textContent = "Analyze Error";
});
