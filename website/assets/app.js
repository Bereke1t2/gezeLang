// app.js
document.addEventListener("DOMContentLoaded", () => {
    // Hero terminal animation
    const termBody = document.querySelector('.terminal-body');
    if (termBody) {
        const amharicSource = "አሳይ('ሰላም ዓለም!')";
        const pythonOutput = "ሰላም ዓለም!";

        async function runAnimation() {
            termBody.innerHTML = '<span class="term-cursor"></span>';
            let currentText = "";

            // Type Amharic
            for (let i = 0; i < amharicSource.length; i++) {
                currentText += amharicSource[i];
                termBody.innerHTML = currentText + '<span class="term-cursor"></span>';
                await new Promise(r => setTimeout(r, 100));
            }

            await new Promise(r => setTimeout(r, 800));

            // Show run command
            currentText += "<br><br><span style='color: var(--gold)'>$ python translator.py hello.amh</span><br>";
            termBody.innerHTML = currentText + '<span class="term-cursor"></span>';

            await new Promise(r => setTimeout(r, 600));

            // Show output
            currentText += pythonOutput + "<br>";
            termBody.innerHTML = currentText + '<span class="term-cursor"></span>';

            await new Promise(r => setTimeout(r, 5000));
            runAnimation(); // Loop
        }

        runAnimation();
    }
});
