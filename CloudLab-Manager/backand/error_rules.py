import re

ERROR_RULES = [

    {
        "category": "API / Authentication",
        "pattern": re.compile(r"api key|invalid api|unauthorized|authentication failed", re.I),
        "summary": "Authentication failed due to an invalid or missing API key.",
        "why_it_happened": [
            "The API key is missing, incorrect, or expired",
            "Authorization headers were not sent properly"
        ],
        "how_to_fix": [
            "Verify that the API key is correct",
            "Regenerate the API key if needed",
            "Ensure headers are passed correctly"
        ],
        "real_world_tip": "Always store API keys in environment variables, never in code."
    },

    {
        "category": "Rate Limiting",
        "pattern": re.compile(r"429|too many requests|rate limit", re.I),
        "summary": "The service rejected the request due to too many requests.",
        "why_it_happened": [
            "API rate limit exceeded",
            "Free-tier usage limit reached"
        ],
        "how_to_fix": [
            "Reduce request frequency",
            "Add retry with exponential backoff",
            "Upgrade your API plan"
        ],
        "real_world_tip": "Production systems implement request throttling and retries."
    },

    {
        "category": "Python Environment",
        "pattern": re.compile(r"modulenotfounderror|no module named", re.I),
        "summary": "Python could not locate the required module.",
        "why_it_happened": [
            "The module is not installed",
            "Wrong virtual environment is active"
        ],
        "how_to_fix": [
            "Install the missing module using pip",
            "Activate the correct virtual environment"
        ],
        "real_world_tip": "Use virtual environments and dependency files like requirements.txt."
    },

    {
        "category": "Network / DNS",
        "pattern": re.compile(r"dns|failed to resolve host|nameresolutionerror", re.I),
        "summary": "The hostname could not be resolved.",
        "why_it_happened": [
            "Incorrect hostname",
            "DNS server or network issue"
        ],
        "how_to_fix": [
            "Verify the hostname",
            "Check DNS and network connectivity"
        ],
        "real_world_tip": "Always validate service endpoints in production environments."
    },

    {
        "category": "Timeout",
        "pattern": re.compile(r"timeout|timed out|504", re.I),
        "summary": "The request took too long and timed out.",
        "why_it_happened": [
            "Slow server response",
            "Network latency"
        ],
        "how_to_fix": [
            "Retry the request",
            "Optimize backend or increase timeout limits"
        ],
        "real_world_tip": "Production systems define strict timeout and retry policies."
    },

    {
        "category": "Kubernetes",
        "pattern": re.compile(r"back-off restarting failed container|crashloopbackoff", re.I),
        "summary": "The Kubernetes container is repeatedly failing and restarting.",
        "why_it_happened": [
            "Application crashes during startup",
            "Incorrect environment variables or secrets",
            "Missing dependencies or incorrect command"
        ],
        "how_to_fix": [
            "Check container logs using kubectl logs",
            "Verify environment variables and secrets",
            "Test the container locally before deployment"
        ],
        "real_world_tip": "Always validate container startup locally before pushing to Kubernetes."
    },

    {
        "category": "AWS / IAM",
        "pattern": re.compile(r"accessdenied|not authorized|s3:putobject", re.I),
        "summary": "The AWS request was denied due to insufficient IAM permissions.",
        "why_it_happened": [
            "IAM role or user lacks required permissions",
            "Incorrect or missing IAM policy"
        ],
        "how_to_fix": [
            "Update the IAM policy to allow the required action",
            "Verify the correct IAM role is attached"
        ],
        "real_world_tip": "Use least-privilege IAM policies and audit them regularly."
    },

    {
        "category": "CI/CD",
        "pattern": re.compile(r"exit code 1|build failed|test failures", re.I),
        "summary": "The CI/CD pipeline failed during the build or test stage.",
        "why_it_happened": [
            "Unit or integration tests failed",
            "Build configuration is incorrect",
            "Required environment variables are missing"
        ],
        "how_to_fix": [
            "Review pipeline logs carefully",
            "Fix failing tests",
            "Validate pipeline configuration"
        ],
        "real_world_tip": "Fail-fast pipelines save time and prevent broken deployments."
    },

    {
        "category": "Database",
        "pattern": re.compile(r"psycopg2\.operationalerror|could not connect to server", re.I),
        "summary": "The application failed to connect to the database.",
        "why_it_happened": [
            "Database server is not running",
            "Incorrect database host, port, or credentials",
            "Network access to the database is blocked"
        ],
        "how_to_fix": [
            "Ensure the database server is running",
            "Verify database connection details",
            "Check firewall and network rules"
        ],
        "real_world_tip": "Always monitor database health and connection limits in production."
    },

    {
        "category": "Docker",
        "pattern": re.compile(r"pull access denied|repository does not exist|docker login", re.I),
        "summary": "Docker failed to pull the image from the registry.",
        "why_it_happened": [
            "Docker image does not exist",
            "User is not authenticated to the registry",
            "Incorrect image name or tag"
        ],
        "how_to_fix": [
            "Run docker login",
            "Verify image name and tag",
            "Ensure the image exists in the registry"
        ],
        "real_world_tip": "Always version Docker images and verify registry access in CI."
    },

    {
        "category": "C / C++ Runtime",
        "pattern": re.compile(r"segmentation fault|core dumped|undefined reference", re.I),
        "summary": "The C/C++ program crashed due to memory or linking issues.",
        "why_it_happened": [
            "Invalid memory access",
            "Uninitialized pointers",
            "Missing library during linking"
        ],
        "how_to_fix": [
            "Check pointer usage",
            "Compile with warnings enabled",
            "Use debugging tools like gdb"
        ],
        "real_world_tip": "Memory safety issues are common in C/C++ and must be handled carefully."
    },

    {
        "category": "Java Runtime",
        "pattern": re.compile(r"nullpointerexception|classnotfoundexception|outofmemoryerror", re.I),
        "summary": "The Java application encountered a runtime exception.",
        "why_it_happened": [
            "Null object access",
            "Missing class dependency",
            "Insufficient JVM memory"
        ],
        "how_to_fix": [
            "Add null checks",
            "Fix dependency configuration",
            "Increase JVM heap size"
        ],
        "real_world_tip": "Use proper exception handling and JVM monitoring in production."
    },

    {
        "category": "JavaScript / TypeScript",
        "pattern": re.compile(r"typeerror|referenceerror|syntaxerror|unhandled promise rejection", re.I),
        "summary": "The JavaScript/TypeScript application failed due to a runtime or syntax error.",
        "why_it_happened": [
            "Undefined variables",
            "Incorrect data types",
            "Unhandled promise rejection"
        ],
        "how_to_fix": [
            "Validate variables",
            "Fix syntax issues",
            "Handle promises correctly"
        ],
        "real_world_tip": "Use linting and strict typing to prevent runtime errors."
    },

    {
        "category": "Python Runtime",
        "pattern": re.compile(r"keyerror|valueerror|indexerror|runtimeerror", re.I),
        "summary": "The Python application encountered a runtime exception.",
        "why_it_happened": [
            "Invalid key or index access",
            "Incorrect input values",
            "Unhandled runtime condition"
        ],
        "how_to_fix": [
            "Validate input data",
            "Add exception handling",
            "Review stack trace"
        ],
        "real_world_tip": "Structured logging helps diagnose Python runtime issues quickly."
    },

    {
        "category": "Go Runtime",
        "pattern": re.compile(r"panic|nil pointer dereference", re.I),
        "summary": "The Go application crashed due to a panic.",
        "why_it_happened": [
            "Nil pointer access",
            "Unexpected runtime condition"
        ],
        "how_to_fix": [
            "Add nil checks",
            "Use recover where appropriate"
        ],
        "real_world_tip": "Always guard critical Go routines against panics."
    },

    {
        "category": "Rust Compile / Runtime",
        "pattern": re.compile(r"borrow checker|lifetime error|compilation failed", re.I),
        "summary": "The Rust application failed due to ownership or lifetime rules.",
        "why_it_happened": [
            "Invalid borrowing",
            "Incorrect lifetime annotations"
        ],
        "how_to_fix": [
            "Refactor code to satisfy ownership rules",
            "Review Rust compiler messages"
        ],
        "real_world_tip": "Rust errors prevent unsafe behavior and should be fixed, not bypassed."
    },

    {
        "category": "Shell / Bash",
        "pattern": re.compile(r"command not found|permission denied|exit status", re.I),
        "summary": "The shell script failed during execution.",
        "why_it_happened": [
            "Missing command",
            "Script lacks execute permission"
        ],
        "how_to_fix": [
            "Verify command availability",
            "Run chmod +x on the script"
        ],
        "real_world_tip": "Validate shell scripts in CI before production execution."
    },

    {
        "category": "PHP Runtime",
        "pattern": re.compile(r"fatal error|undefined function|parse error", re.I),
        "summary": "The PHP application encountered a fatal error.",
        "why_it_happened": [
            "Calling an undefined function",
            "Syntax error in code"
        ],
        "how_to_fix": [
            "Check function definitions",
            "Fix syntax errors"
        ],
        "real_world_tip": "Enable error reporting in development, disable in production."
    },

    {
        "category": "Ruby Runtime",
        "pattern": re.compile(r"undefined method|nomethoderror|loaderror", re.I),
        "summary": "The Ruby application failed due to a runtime error.",
        "why_it_happened": [
            "Calling a method that does not exist",
            "Missing gem dependency"
        ],
        "how_to_fix": [
            "Verify method definitions",
            "Install missing gems"
        ],
        "real_world_tip": "Lock Ruby dependencies using Bundler."
    },

    {
        "category": "C# / .NET Runtime",
        "pattern": re.compile(r"nullreferenceexception|assembly not found|runtime exception", re.I),
        "summary": "The .NET application encountered a runtime exception.",
        "why_it_happened": [
            "Null object reference",
            "Missing assembly dependency"
        ],
        "how_to_fix": [
            "Add null checks",
            "Restore NuGet packages"
        ],
        "real_world_tip": "Use structured exception handling in .NET applications."
    },

    # ✅ NEW RULE — ZeroDivisionError
    {
        "category": "Python Runtime",
        "pattern": re.compile(r"zerodivisionerror", re.I),
        "summary": "A number was divided by zero, which is mathematically undefined.",
        "why_it_happened": [
            "Dividing a variable whose value is 0",
            "Unexpected zero input from user or calculation",
            "Missing validation before division"
        ],
        "how_to_fix": [
            "Check if the denominator is zero before dividing",
            "Add input validation",
            "Use try-except to handle ZeroDivisionError"
        ],
        "real_world_tip": "Always validate numeric inputs before performing arithmetic operations."
    },

    # ✅ NEW RULE — NameError
    {
        "category": "Python Runtime",
        "pattern": re.compile(r"nameerror", re.I),
        "summary": "A variable or function name was used before it was defined.",
        "why_it_happened": [
            "Misspelled variable name",
            "Variable not declared before use",
            "Wrong scope (local vs global)"
        ],
        "how_to_fix": [
            "Define the variable before using it",
            "Fix spelling mistakes",
            "Check variable scope"
        ],
        "real_world_tip": "Use linters and IDE warnings to catch undefined names early."
    }

]
