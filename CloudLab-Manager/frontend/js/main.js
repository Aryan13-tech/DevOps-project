const BACKEND_URL = "http://127.0.0.1:5000/analyze-error";

const analyzeBtn = document.getElementById("analyzeBtn");
const errorInput = document.getElementById("errorInput");
const explanation = document.getElementById("explanation");
const causes = document.getElementById("causes");
const solutions = document.getElementById("solutions");
const categoryBadge = document.getElementById("categoryBadge");

analyzeBtn.addEventListener("click", async () => {
  const errorText = errorInput.value.trim();
  if (!errorText) {
    alert("Enter an error message");
    return;
  }

  // UI: loading state
  analyzeBtn.disabled = true;
  analyzeBtn.textContent = "Analyzing...";
  categoryBadge.textContent = "Analyzing...";
  categoryBadge.className = "badge waiting";

  explanation.textContent = "Analyzing error...";
  causes.innerHTML = "<li>Analyzing...</li>";
  solutions.innerHTML = "<li>Analyzing...</li>";

  try {
    const res = await fetch(BACKEND_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ error: errorText })
    });

    if (!res.ok) {
      throw new Error(`Backend returned ${res.status}`);
    }

    const data = await res.json();

    if (!data.success) {
      throw new Error(data.message || "Analysis failed");
    }

    // Fill UI
    explanation.textContent =
      data.summary || "No explanation available.";

    causes.innerHTML = (data.why_it_happened || [])
      .map(c => `<li>${c}</li>`)
      .join("") || "<li>No causes provided.</li>";

    solutions.innerHTML = (data.how_to_fix || [])
      .map(s => `<li>${s}</li>`)
      .join("") || "<li>No solutions provided.</li>";

    // Badge styling based on source
    categoryBadge.textContent = data.error_category || "Unknown";

    if (data.source === "rule-engine") {
      categoryBadge.className = "badge rule-based";
    } else if (data.source === "gemini-ai") {
      categoryBadge.className = "badge ai-based";
    } else {
      categoryBadge.className = "badge error";
    }

  } catch (err) {
    console.error("Analysis failed:", err);

    // Safe UI fallback
    explanation.textContent =
      "Failed to analyze the error. Please try again.";

    causes.innerHTML = "<li>Backend unavailable or error occurred.</li>";
    solutions.innerHTML = "<li>Check server logs and retry.</li>";

    categoryBadge.textContent = "Error";
    categoryBadge.className = "badge error";
  }

  // UI: restore button
  analyzeBtn.disabled = false;
  analyzeBtn.textContent = "Analyze Error";
});
