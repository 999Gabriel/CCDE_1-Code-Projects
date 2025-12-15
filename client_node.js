const readline = require('readline');

const API_BASE = "http://127.0.0.1:5000/api";

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// Helper to get user input as a promise
function askQuestion(query) {
    return new Promise(resolve => rl.question(query, resolve));
}

// Helper for API calls
async function apiCall(endpoint, method = 'GET', body = null) {
    try {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json'
            }
        };

        // We need to maintain session cookies manually in a simple node script without a browser
        // However, fetch in Node doesn't automatically persist cookies like a browser.
        // We need to capture the 'set-cookie' header from the response and send it back.
        // This is a bit complex for a simple script without a library like 'axios-cookie-jar-support'.

        // WAIT! The Python requests.Session() handles cookies automatically.
        // In Node native fetch, we have to handle it.

        // Let's use a global variable to store the cookie.
        if (global.sessionCookie) {
            options.headers['Cookie'] = global.sessionCookie;
        }

        if (body) {
            options.body = JSON.stringify(body);
        }

        const response = await fetch(`${API_BASE}${endpoint}`, options);

        // Update cookie if present
        const setCookie = response.headers.get('set-cookie');
        if (setCookie) {
            // Simple extraction of the session cookie
            global.sessionCookie = setCookie.split(';')[0];
        }

        if (!response.ok) {
            const errText = await response.text();
            throw new Error(`API Error: ${response.status} - ${errText}`);
        }

        return await response.json();
    } catch (error) {
        console.error("Network error:", error.message);
        return null;
    }
}

async function startGame() {
    console.log("\n--- Starting New Game ---");
    const data = await apiCall('/start', 'POST');
    if (data && data.status === 'started') {
        console.log("Game Started!");
        await gameLoop();
    } else {
        console.log("Failed to start game.");
        rl.close();
    }
}

async function gameLoop() {
    while (true) {
        const qData = await apiCall('/question');

        if (!qData) break;

        if (qData.status === 'win') {
            console.log("\n***********************************");
            console.log("CONGRATULATIONS! YOU WON!");
            console.log(`Final Score: ${qData.score}`);
            console.log("***********************************\n");
            break;
        }

        if (qData.error) {
            console.log("Error:", qData.error);
            break;
        }

        console.log(`\nLevel: ${qData.level}`);
        console.log(`Question: ${qData.text}`);
        console.log("-----------------------------------");

        qData.answers.forEach((ans, idx) => {
            console.log(`${String.fromCharCode(65 + idx)}. ${ans}`);
        });
        console.log("-----------------------------------");

        let answerIndex = -1;
        while (answerIndex === -1) {
            const input = await askQuestion("Your answer (A/B/C/D): ");
            const charCode = input.toUpperCase().charCodeAt(0);
            if (input.length === 1 && charCode >= 65 && charCode <= 68) {
                answerIndex = charCode - 65;
            } else {
                console.log("Invalid input. Please enter A, B, C, or D.");
            }
        }

        const result = await apiCall('/answer', 'POST', { answer_index: answerIndex });

        if (!result) break;

        if (result.correct) {
            console.log("\n✅ CORRECT!");
            console.log(`Current Score: ${result.score}`);
            // Continue loop
        } else if (result.game_over) {
            console.log("\n❌ WRONG ANSWER!");
            console.log("GAME OVER");
            console.log(`Final Score: ${result.score}`);
            break;
        }
    }

    const playAgain = await askQuestion("\nPlay again? (y/n): ");
    if (playAgain.toLowerCase() === 'y') {
        await startGame();
    } else {
        console.log("Thanks for playing!");
        rl.close();
    }
}

console.log("Welcome to the Millionaire Node.js Client!");
startGame();

