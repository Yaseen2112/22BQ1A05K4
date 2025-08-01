const express = require('express');
const axios = require('axios');

const app = express();
const PORT = 3000;

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
            console.log('Log API Response:', res.data);
            return res.data;
        })
        .catch(err => {
            console.error('Logging failed:', err.response?.data || err.message);
            throw err;
        });
}

app.get('/test-log', async (req, res) => {
    try {
        await Log('backend', 'info', 'controller', 'Test log from backend controller');
        res.json({ success: true, message: 'Log sent successfully' });
    } catch (error) {
        res.status(500).json({ success: false, message: 'Logging failed', error: error.message });
    }
});

app.listen(PORT, () => {
    console.log(`Backend server running on http://localhost:${PORT}`);
});
