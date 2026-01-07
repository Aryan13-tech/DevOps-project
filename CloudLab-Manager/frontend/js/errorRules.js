export const errorRules = [

  // Python missing module
  {
    match: /ModuleNotFoundError: No module named ['"](.+)['"]/i,
    explanation: "Python cannot find the required module in your environment.",
    causes: [
      "The package is not installed",
      "Wrong virtual environment is active"
    ],
    solutions: [
      "Install the package using pip install <package-name>",
      "Activate the correct virtual environment"
    ]
  },

  // Pydantic BaseSettings (VERY IMPORTANT)
  {
    match: /BaseSettings.*pydantic/i,
    explanation: "This error occurs because Pydantic v2 moved BaseSettings to a new package.",
    causes: [
      "You are using Pydantic version 2",
      "Your code was written for Pydantic v1"
    ],
    solutions: [
      "Install pydantic-settings",
      "Change import to: from pydantic_settings import BaseSettings",
      "OR downgrade pydantic to version 1"
    ]
  },

  // Connection refused
  {
    match: /ConnectionError|connection refused|Errno 111/i,
    explanation: "The application failed to connect to a server.",
    causes: [
      "Backend server is not running",
      "Wrong host or port",
      "Firewall blocking the connection"
    ],
    solutions: [
      "Start the backend server",
      "Verify host and port",
      "Check firewall or antivirus"
    ]
  },

  // Docker / Kubernetes image pull
  {
    match: /failed to pull image|pod sandbox/i,
    explanation: "The container runtime failed to download the required image.",
    causes: [
      "Incorrect image name",
      "Private registry authentication required",
      "No internet connection"
    ],
    solutions: [
      "Verify the image name",
      "Login to the container registry",
      "Check network connectivity"
    ]
  },

  // HTTP 401 Unauthorized
  {
    match: /401 Unauthorized|HTTPError: 401/i,
    explanation: "The request was rejected due to missing or invalid authentication.",
    causes: [
      "Missing API key or token",
      "Expired credentials"
    ],
    solutions: [
      "Provide valid authentication credentials",
      "Regenerate API token"
    ]
  }
];
