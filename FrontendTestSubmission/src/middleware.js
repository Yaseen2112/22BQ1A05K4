export function Log(stack, level, packageName, message) {
    if (stack !== "frontend") {
        return Promise.reject(new Error("Stack must be 'frontend' for frontend logs"));
    }
    if (packageName !== "api") {
        return Promise.reject(new Error("Package must be 'api' for frontend logs"));
    }

    const payload = {
        stack,
        level,
        package: packageName,
        message
    };

    return fetch("http://20.244.56.144/evaluation-service/logs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    })
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        });
}
