export const errorRules = [

  // =========================
  // API / AUTH ERRORS
  // =========================
  {
    match: /api key|invalid api|authentication failed|unauthorized/i,
    explanation: "Authentication failed because the API key or token is invalid or missing.",
    causes: [
      "API key is incorrect or expired",
      "API key not loaded from environment variables",
      "Authorization header missing"
    ],
    solutions: [
      "Verify API key in .env file",
      "Generate a new API key",
      "Restart the backend service"
    ]
  },

  // =========================
  // RATE LIMIT
  // =========================
  {
    match: /429|too many requests|rate limit/i,
    explanation: "The server rejected the request because too many requests were sent in a short time.",
    causes: [
      "API rate limit exceeded",
      "Free-tier quota reached",
      "Too many parallel requests"
    ],
    solutions: [
      "Wait and retry after some time",
      "Reduce request frequency",
      "Upgrade the API plan"
    ]
  },

  // =========================
  // SERVICE UNAVAILABLE
  // =========================
  {
    match: /503|service unavailable/i,
    explanation: "The service is temporarily unavailable and cannot handle the request.",
    causes: [
      "Server overload",
      "Service downtime or maintenance"
    ],
    solutions: [
      "Retry after a few minutes",
      "Check the service status page"
    ]
  },

  // =========================
  // GATEWAY TIMEOUT
  // =========================
  {
    match: /504|gateway timeout/i,
    explanation: "The server did not respond within the allowed time.",
    causes: [
      "Upstream service is slow",
      "Network latency issues"
    ],
    solutions: [
      "Increase request timeout",
      "Check upstream service health"
    ]
  },

  // =========================
  // DNS ERROR
  // =========================
  {
    match: /dns|nameresolutionerror|failed to resolve host/i,
    explanation: "The domain name could not be resolved to an IP address.",
    causes: [
      "Incorrect hostname",
      "DNS server issue",
      "No internet connection"
    ],
    solutions: [
      "Verify the hostname",
      "Check DNS and network settings"
    ]
  },

  // =========================
  // SSL / TLS
  // =========================
  {
    match: /ssl|certificate verify failed|sslhandshake/i,
    explanation: "SSL/TLS certificate verification failed.",
    causes: [
      "Expired or invalid certificate",
      "Incorrect system date and time",
      "Invalid certificate chain"
    ],
    solutions: [
      "Update certificates",
      "Check system time",
      "Verify HTTPS configuration"
    ]
  },

  // =========================
  // TIMEOUT (GENERAL)
  // =========================
  {
    match: /timeout|timed out/i,
    explanation: "The request exceeded the allowed response time.",
    causes: [
      "Slow or unstable internet connection",
      "External API service is down or overloaded",
      "Timeout value too low"
    ],
    solutions: [
      "Check your internet connection",
      "Increase request timeout",
      "Retry the request later"
    ]
  },

  // =========================
  // INVALID REQUEST
  // =========================
  {
    match: /invalid request|required|missing.*field|prompt field/i,
    explanation: "The request is missing required input fields.",
    causes: [
      "Prompt field not provided",
      "Empty or malformed request body"
    ],
    solutions: [
      "Provide all required fields",
      "Validate input before sending request"
    ]
  },

  // =========================
  // PYTHON MODULE ERROR
  // =========================
  {
    match: /(ModuleNotFoundError|No module named)/i,
    explanation: "Python cannot find the required module.",
    causes: [
      "Package not installed",
      "Wrong virtual environment"
    ],
    solutions: [
      "Run: pip install <package>",
      "Activate correct virtual environment"
    ]
  },

  // =========================
  // GENERIC FALLBACK (ALWAYS LAST)
  // =========================
  {
    match: /.*/i,
    explanation: "This error could not be classified automatically.",
    causes: [
      "Unknown or complex error"
    ],
    solutions: [
      "Check logs",
      "Search official documentation"
    ]
  }
];
