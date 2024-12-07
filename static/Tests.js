// Define the tests with their rotation angles, correct answers, and sizes
const tests = [
    { level: 1, rotation: 0, correctAnswer: "1", width: '50px' },
    { level: 2, rotation: 270, correctAnswer: "7", width: '36px' },
    { level: 3, rotation: 45, correctAnswer: "2", width: '24px' },
    { level: 4, rotation: 135, correctAnswer: "4", width: '24px' },
    { level: 5, rotation: 180, correctAnswer: "5", width: '18px' },
    { level: 6, rotation: 90, correctAnswer: "3", width: '18px' },
    { level: 7, rotation: 270, correctAnswer: "7", width: '18px' },
    { level: 8, rotation: 225, correctAnswer: "6", width: '12px' },
    { level: 9, rotation: 0, correctAnswer: "1", width: '12px' },
    { level: 10, rotation: 180, correctAnswer: "5", width: '12px' },
    { level: 11, rotation: 90, correctAnswer: "3", width: '12px' },
    { level: 12, rotation: 135, correctAnswer: "4", width: '8px' },
    { level: 13, rotation: 315, correctAnswer: "8", width: '8px' },
    { level: 14, rotation: 45, correctAnswer: "2", width: '6px' },
    { level: 15, rotation: 270, correctAnswer: "7", width: '6px' },
    { level: 16, rotation: 225, correctAnswer: "6", width: '4px' },
    { level: 17, rotation: 0, correctAnswer: "1", width: '4px' }
];

let currentTestIndex = 0;
let incorrectAnswers = 0;
let highestLevelPassed = 1; // Start at Level 1

// Function to load the test based on the current index
function loadTest() {
    const errorMessage = document.getElementById("error-message");
    errorMessage.style.display = "none";

    // Check if test is complete
    if (incorrectAnswers >= 3) {
        // Terminate test and show final level
        endTest();
        return;
    }

    if (currentTestIndex >= tests.length) {
        endTest();
        return;
    }

    const test = tests[currentTestIndex];

    // Rotate the littleCircle
    const littleCircle = document.querySelector(".littleCircle");
    littleCircle.style.transform = `rotate(${test.rotation}deg)`;
    littleCircle.style.width = test.width;

    // Update level display 
    const levelDisplay = document.getElementById("current-level");
    if (levelDisplay) {
        levelDisplay.textContent = `Current Level: ${test.level}`;
    }

    // Add click event listeners to paths
    const paths = document.querySelectorAll("svg path");
    paths.forEach((path) => {
        path.removeEventListener("click", handleClick);
        path.addEventListener("click", handleClick);
    });
}

// Function to end the test
function endTest() {
    const errorMessage = document.getElementById("error-message");
    
    // Create a detailed result message
    let resultMessage = `Test complete!\n`;
    resultMessage += `Highest Visual Acuity Level: ${highestLevelPassed}\n`;
    resultMessage += `Total Incorrect Answers: ${incorrectAnswers}`;

    // Show result in a more informative way
    alert(resultMessage);

    // Optionally, disable further interactions
    const paths = document.querySelectorAll("svg path");
    paths.forEach((path) => {
        path.removeEventListener("click", handleClick);
    });
}

// Function to handle click on paths
function handleClick(event) {
    const test = tests[currentTestIndex];
    const clickedId = event.target.id;

    const errorMessage = document.getElementById("error-message");

    if (clickedId === test.correctAnswer) {
        // Correct answer: Determine progression
        if (test.level <= 10) {
            // First 10 levels: progress by 2
            currentTestIndex += 2;
        } else {
            // After Level 10: progress by 1
            currentTestIndex += 1;
        }
        
        // Update highest level passed
        highestLevelPassed = Math.max(highestLevelPassed, test.level);
        
        loadTest();
    } else {
        // Incorrect answer
        incorrectAnswers++;

        // Immediate test termination on third incorrect answer
        if (incorrectAnswers >= 3) {
            errorMessage.textContent = "Maximum incorrect answers reached.";
            errorMessage.style.display = "block";
            endTest();
            return;
        }

        // Show error message
        errorMessage.textContent = "Wrong answer! Be careful.";
        errorMessage.style.display = "block";

        // Drop by 1 level after an incorrect answer
        currentTestIndex = Math.max(0, currentTestIndex - 1);
        
        loadTest();
    }
}

// Load the first test on page load
document.addEventListener("DOMContentLoaded", loadTest);
/**************************************************************************************************************** */