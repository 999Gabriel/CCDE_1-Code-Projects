const readline = require('readline');

// Configuration
const API_BASE = "http://127.0.0.1:5000/api";

// ANSI Colors for TUI
const COLORS = {
    reset: "\x1b[0m",
    bright: "\x1b[1m",
    red: "\x1b[31m",
    green: "\x1b[32m",
    yellow: "\x1b[33m",
    blue: "\x1b[34m",
    cyan: "\x1b[36m",
    white: "\x1b[37m",
    bgBlue: "\x1b[44m"
};

// UI Helpers
const clearScreen = () => process.stdout.write('\x1b[2J\x1b[0f');
const printHeader = (text) => {
    console.log(COLORS.bgBlue + COLORS.white + COLORS.bright);
    console.log(`  ${text}  `);
    console.log(COLORS.reset + "\n");
};

// State
let sessionCookie = null;

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

const question = (str) => new Promise(resolve => rl.question(COLORS.cyan + str + COLORS.reset, resolve));

// API Helper
async function apiCall(endpoint, method = 'GET', body = null) {
    try {
        const headers = { 'Content-Type': 'application/json' };
        if (sessionCookie) {
            headers['Cookie'] = sessionCookie;
        }

        const options = {
            method,
            headers,
            body: body ? JSON.stringify(body) : undefined
        };

        const response = await fetch(`${API_BASE}${endpoint}`, options);

        // Capture session cookie
        const setCookie = response.headers.get('set-cookie');
        if (setCookie) {
            sessionCookie = setCookie.split(';')[0];
        }

        if (!response.ok) {
            // Try to parse error message
            try {
                const errData = await response.json();
                return { error: errData.error || `HTTP ${response.status}` };
            } catch (e) {
                return { error: `HTTP ${response.status}` };
            }
        }
        return await response.json();
    } catch (error) {
        return { error: error.message };
    }
}

// Game Logic
async function startGame() {
    clearScreen();
    printHeader("MILLIONAIRE - CLI EDITION");
    console.log("Connecting to server...\n");

    const startData = await apiCall('/start', 'POST');
    if (startData.error) {
        console.log(COLORS.red + "Error starting game: " + startData.error + COLORS.reset);
        process.exit(1);
    }

    await gameLoop();
}

async function gameLoop() {
    while (true) {
        // Fetch Question
        const qData = await apiCall('/question');

        if (qData.error) {
            console.log(COLORS.red + "Error: " + qData.error + COLORS.reset);
            break;
        }

        if (qData.status === 'win') {
            clearScreen();
            printHeader("WINNER!");
            console.log(COLORS.green + COLORS.bright + `Congratulations! You won with score: ${qData.score}` + COLORS.reset);
            break;
        }

        // Display Question
        clearScreen();
        printHeader(`Level ${qData.level}  |  $$$`);
        console.log(COLORS.bright + qData.text + COLORS.reset + "\n");

        qData.answers.forEach((ans, idx) => {
            console.log(`${COLORS.yellow}[${idx}]${COLORS.reset} ${ans}`);
        });
        console.log(""); // Spacer

        // Get Input
        let answerIndex = -1;
        while (true) {
            const input = await question("Your Answer (0-3): ");
            const parsed = parseInt(input);
            if (!isNaN(parsed) && parsed >= 0 && parsed < 4) {
                answerIndex = parsed;
                break;
            }
            console.log(COLORS.red + "Invalid input. Please enter 0, 1, 2, or 3." + COLORS.reset);
        }

        // Submit Answer
        const result = await apiCall('/answer', 'POST', { answer_index: answerIndex });

        if (result.error) {
            console.log(COLORS.red + "Error submitting answer: " + result.error + COLORS.reset);
            break;
        }

        if (result.game_over) {
            console.log("\n" + COLORS.red + COLORS.bright + "WRONG ANSWER!" + COLORS.reset);
            console.log(`Game Over. Final Score: ${result.score}`);
            break;
        } else if (result.correct) {
            console.log("\n" + COLORS.green + "CORRECT!" + COLORS.reset);
            console.log(`Score: ${result.score}`);
            await new Promise(r => setTimeout(r, 1500)); // Pause for effect
        }
    }

    // Play again?
    console.log("\n");
    const again = await question("Play again? (y/n): ");
    if (again.toLowerCase().startsWith('y')) {
        await startGame();
    } else {
        console.log("Thanks for playing!");
        rl.close();
    }
}

// Start
if (require.main === module) {
    // Check if fetch is available (Node 18+)
    if (typeof fetch === 'undefined') {
        console.error(COLORS.red + "This script requires Node.js v18+ (Fetch API)." + COLORS.reset);
        process.exit(1);
    }
    startGame().catch(console.error);
}
