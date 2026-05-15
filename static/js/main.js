// Local Storage Dark Mode State Machine Toggle Execution Logic
document.addEventListener('DOMContentLoaded', () => {
    const themeToggleBtn = document.getElementById('theme-toggle');
    const htmlEl = document.documentElement;

    // Run baseline diagnostic evaluation check
    if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        htmlEl.classList.add('dark');
    } else {
        htmlEl.classList.remove('dark');
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            if (htmlEl.classList.contains('dark')) {
                htmlEl.classList.remove('dark');
                localStorage.setItem('color-theme', 'light');
            } else {
                htmlEl.classList.add('dark');
                localStorage.setItem('color-theme', 'dark');
            }
        });
    }

    // Dynamic processing loading interface triggers
    const analysisForm = document.getElementById('analysis-form');
    const structuralLoadingScreen = document.getElementById('loading-screen');

    if (analysisForm && structuralLoadingScreen) {
        analysisForm.addEventListener('submit', () => {
            structuralLoadingScreen.classList.remove('hidden');
            structuralLoadingScreen.classList.add('flex');
            
            // Cycle descriptive application processing status strings
            const stateLabels = [
                "Initializing parsing sequence arrays...",
                "Decoding PDF structural matrix components...",
                "Running computational token cleanup...",
                "Matching keywords with dataset variables...",
                "Calculating context vector geometries...",
                "Compiling optimization feedback lists..."
            ];
            let counter = 0;
            const progressLabel = document.getElementById('loading-text');
            if (progressLabel) {
                setInterval(() => {
                    if (counter < stateLabels.length) {
                        progressLabel.textContent = stateLabels[counter];
                        counter++;
                    }
                }, 1800);
            }
        });
    }
});