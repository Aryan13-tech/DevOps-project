import { errorRules } from "./errorRules.js";

const BACKEND_URL = "http://127.0.0.1:5000/analyze-error";

const analyzeBtn = document.getElementById("analyzeBtn");
const errorInput = document.getElementById("errorInput");
const explanation = document.getElementById("explanation");
const causes = document.getElementById("causes");
const solutions = document.getElementById("solutions");
const categoryBadge = document.getElementById("categoryBadge");

analyzeBtn.addEventListener("click", analyzeError);

function extractErrorMessage(input) {
  try {
    const parsed = JSON.parse(input);
    return typeof parsed.error === "string"
      ? parsed.error.toLowerCase()
      : input.toLowerCase();
  } catch {
    return input.toLowerCase();
  }
}

async function analyzeError() {
  const rawInput = errorInput.value.trim();
  if (!rawInput) return alert("Please enter an error message");

  const cleanError = extractErrorMessage(rawInput);

  analyzeBtn.textContent = "Analyzing...";
  analyzeBtn.classList.add("loading");
  analyzeBtn.disabled = true;

  explanation.textContent = "Analyzing error...";
  causes.innerHTML = "";
  solutions.innerHTML = "";
  categoryBadge.textContent = "";

  // ✅ STEP 1: OFFLINE RULES
  for (const rule of errorRules) {
    if (rule.match.test(cleanError)) {
      categoryBadge.textContent = "Rule-Based Offline";
      categoryBadge.className = "badge rule-based";

      explanation.textContent = rule.explanation;
      causes.innerHTML = rule.causes.map(c => `<li>${c}</li>`).join("");
      solutions.innerHTML = rule.solutions.map(s => `<li>${s}</li>`).join("");

      resetButton();
      return;
    }
  }

  // ✅ STEP 2: BACKEND / GEMINI
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 8000);

    const res = await fetch(BACKEND_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ error: cleanError }),
      signal: controller.signal
    });

    clearTimeout(timeout);

    const data = await res.json();
    if (!data.success) throw new Error("Backend failed");

    categoryBadge.textContent =
      data.source === "gemini"
        ? "Gemini AI (Online)"
        : "Rule-Based Backend";

    categoryBadge.className =
      data.source === "gemini"
        ? "badge gemini"
        : "badge rule-based";

    explanation.textContent = data.explanation;
    causes.innerHTML = data.causes.map(c => `<li>${c}</li>`).join("");
    solutions.innerHTML = data.solutions.map(s => `<li>${s}</li>`).join("");

  } catch {
    categoryBadge.textContent = "Unclassified Error";
    categoryBadge.className = "badge error";

    explanation.textContent =
      "This error could not be analyzed automatically.";

    causes.innerHTML = "<li>No matching rule or backend unavailable</li>";
    solutions.innerHTML = "<li>Check logs or add a new rule</li>";
  }

  resetButton();
}

function resetButton() {
  analyzeBtn.textContent = "Analyze Error";
  analyzeBtn.classList.remove("loading");
  analyzeBtn.disabled = false;
}
