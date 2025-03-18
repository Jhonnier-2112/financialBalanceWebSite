document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.getElementById("registerForm");
    const toastContainer = document.getElementById("toast-container");
    const passwordInput = document.getElementById("password");
    const confirmPasswordInput = document.getElementById("confirmPassword");
    const togglePassword = document.getElementById("togglePassword");
    const toggleConfirmPassword = document.getElementById("toggleConfirmPassword");

    // Función para alternar la visibilidad de la contraseña
    function togglePasswordVisibility(input, icon) {
        if (input.type === "password") {
            input.type = "text";
            icon.classList.replace("fa-eye", "fa-eye-slash");
        } else {
            input.type = "password";
            icon.classList.replace("fa-eye-slash", "fa-eye");
        }
    }

    togglePassword.addEventListener("click", () => togglePasswordVisibility(passwordInput, togglePassword.firstElementChild));
    toggleConfirmPassword.addEventListener("click", () => togglePasswordVisibility(confirmPasswordInput, toggleConfirmPassword.firstElementChild));

    // Validación de contraseña
    function validarPassword(password) {
        const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{6,}$/;
        return regex.test(password);
    }

    registerForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const name = document.getElementById("name").value.trim();
        const email = document.getElementById("email").value.trim();
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;

        if (!validarPassword(password)) {
            mostrarNotificacion("⚠ La contraseña debe tener al menos 6 caracteres, una mayúscula, una minúscula y un carácter especial.", "error");
            return;
        }

        if (password !== confirmPassword) {
            mostrarNotificacion("❌ Las contraseñas no coinciden.", "error");
            return;
        }

        const userData = { name, email, password };

        try {
            const response = await fetch("http://127.0.0.1:5000/api/users/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(userData),
            });

            const result = await response.json();

            if (response.ok) {
                mostrarNotificacion("✅ ¡Registro exitoso!", "success");
                registerForm.reset();
                setTimeout(() => window.location.href = "http://127.0.0.1:5000/api/users/login", 2000);
            } else {
                mostrarNotificacion(`❌ ${result.error}`, "error");
            }
        } catch (error) {
            mostrarNotificacion("⚠ Error al conectar con el servidor.", "error");
        }
    });

    // Función para mostrar notificaciones
    function mostrarNotificacion(mensaje, tipo) {
        const toast = document.createElement("div");
        toast.className = `relative flex items-center px-4 pr-12 py-3 rounded-md shadow-md opacity-0 transition-all duration-300 border ${
            tipo === "success" ? "bg-green-100 text-green-700 border-green-400" : "bg-red-100 text-red-700 border-red-400"
        }`;

        toast.innerHTML = `
            <span class="flex items-center">
                <i class="${tipo === "success" ? "fa fa-check-circle text-green-600" : "fa fa-exclamation-circle text-red-600"} text-lg mr-2"></i>
                ${mensaje}
            </span>
            <button class="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-800" onclick="this.parentElement.remove()">
                <i class="fa fa-times text-lg"></i>
            </button>
        `;

        toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.classList.remove("opacity-0");
            toast.classList.add("opacity-100");
        }, 100);

        setTimeout(() => {
            toast.classList.remove("opacity-100");
            toast.classList.add("opacity-0");
            setTimeout(() => toast.remove(), 400);
        }, 3000);
    }
});
