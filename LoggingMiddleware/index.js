const axios = require('axios');

function Log(stack, level, packageName, message) {
    const allowedPackages = {
        backend: ["cache", "controller", "cron_job", "db", "domain", "handler", "repository", "route", "service"],
        frontend: ["api"]
    };

    if (!["backend", "frontend"].includes(stack)) throw new Error("Invalid stack");
    if (!["debug", "info", "warn", "error", "fatal"].includes(level)) throw new Error("Invalid level");
    if (!allowedPackages[stack].includes(packageName)) throw new Error("Invalid package");
    if (!message) throw new Error("Message required");

    const payload = {
        stack,
        level,
        package: packageName,
        message
    };

    return axios.post('http://20.244.56.144/evaluation-service/logs', payload)
        .then(res => {
            console.log('Log successful:', res.data);
            return res.data;
        })
        .catch(err => {
            console.error('Logging failed:', err.response?.data || err.message);
            throw err;
        });
}

module.exports = { Log };
