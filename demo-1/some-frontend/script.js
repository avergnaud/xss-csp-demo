// XSS Demo Script - Vulnerable by design for educational purposes

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('xssForm');
    const userInput = document.getElementById('userInput');
    const output = document.getElementById('output');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent page refresh

        const inputValue = userInput.value;

        // VULNERABILITY: Direct innerHTML assignment without sanitization
        // This allows any HTML/JavaScript to be executed
        output.innerHTML = inputValue;
    });
});
