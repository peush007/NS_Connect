document.addEventListener('DOMContentLoaded', () => {

    const form = document.getElementById('wizardForm');
    const step1 = document.getElementById('step1');
    const step2 = document.getElementById('step2');
    const stepperItems = document.querySelectorAll('.stepper-item');

    // --- Floating Label Logic ---
    const inputs = document.querySelectorAll('.input-group input, .input-group textarea, .input-group select');

    function updateLabelState(input) {
        const group = input.closest('.input-group');
        if (input.value && input.value.trim() !== '') {
            group.classList.add('has-value');
        } else {
            group.classList.remove('has-value');
        }
    }

    inputs.forEach(input => {
        // Function to check state
        const check = () => updateLabelState(input);

        // Events
        input.addEventListener('input', check);
        input.addEventListener('change', check);
        input.addEventListener('blur', check);
        input.addEventListener('focus', check);

        // Check repeatedly on load to catch autofill
        check();
        setTimeout(check, 100);
        setTimeout(check, 500);
        setTimeout(check, 1000);
    });


    // --- Wizard Navigation Logic ---

    window.nextStep = function () {
        if (validateStep1()) {
            // Visualize transition
            step1.classList.remove('active');
            step2.classList.add('active');

            // Update Stepper
            stepperItems[0].classList.remove('active'); // Account
            stepperItems[0].querySelector('.step-counter').innerHTML = '&#10003;'; // Checkmark
            stepperItems[1].classList.add('active'); // Business
        }
    };

    window.prevStep = function () {
        step2.classList.remove('active');
        step1.classList.add('active');

        // Update Stepper
        stepperItems[0].classList.add('active');
        stepperItems[0].querySelector('.step-counter').textContent = '1';
        stepperItems[1].classList.remove('active');
    };

    function validateStep1() {
        let valid = true;
        const requiredFields = step1.querySelectorAll('input[required]');

        // Simple client-side check
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                valid = false;
                // Highlight error visual manually if preferred
                field.closest('.input-group').style.animation = 'shake 0.3s';
                setTimeout(() => field.closest('.input-group').style.animation = '', 300);
            }
        });

        // Check for Django errors that might be rendered
        // If there are .errorlist elements inside step1, we might block or just show them.
        // For now, allow navigation, but generally if used serverside validation, 
        // the page reloads and we need to detect which step to show.

        // Strategy: If inputs are empty, block.
        // If simply returning from server with errors, we need to know which step to show.

        return valid;
    }

    // --- Server validation Error Handling ---
    // If the page reloads with errors in Step 2 fields, we should jump to Step 2.
    const step2Errors = step2.querySelectorAll('.errorlist');
    if (step2Errors.length > 0) {
        // We have errors in step 2, show step 2 immediately
        step1.classList.remove('active');
        step2.classList.add('active');
        stepperItems[0].classList.remove('active');
        stepperItems[0].querySelector('.step-counter').innerHTML = '&#10003;';
        stepperItems[1].classList.add('active');
    }

    // Similarly check if step 1 has errors, stay on step 1 (default)
});

// CSS for Shake animation
const style = document.createElement('style');
style.innerHTML = `
@keyframes shake {
  0% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  50% { transform: translateX(5px); }
  75% { transform: translateX(-5px); }
  100% { transform: translateX(0); }
}
`;
document.head.appendChild(style);
