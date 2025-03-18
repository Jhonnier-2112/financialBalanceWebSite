document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("registerForm");
    const passwordInput = document.getElementById("password");
    const togglePassword = document.getElementById("togglePassword");
    const toastContainer = document.getElementById("toast-container");

    // 👁️ Mostrar / Ocultar contraseña
    togglePassword.addEventListener("click", function () {
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
            togglePassword.innerHTML = '<i class="fa fa-eye-slash"></i>';
        } else {
            passwordInput.type = "password";
            togglePassword.innerHTML = '<i class="fa fa-eye"></i>';
        }
    });

    // 🔥 Mostrar notificación de éxito o error
    function showToast(message, type = "error") {
        const toast = document.createElement("div");
        toast.classList.add("toast", type);
        toast.innerHTML = message;

        toastContainer.appendChild(toast);
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }

    // 📡 Enviar formulario de login
    loginForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const email = document.getElementById("email").value;
        const password = passwordInput.value;

        try {
            const response = await fetch("/api/users/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem("token", data.token);
                showToast("✅ Inicio de sesión exitoso", "success");

                setTimeout(() => {
                    window.location.href = "/api/balance";
                }, 1000);
            } else {
                showToast("❌ " + (data.error || "Credenciales incorrectas"), "error");
            }
        } catch (error) {
            showToast("❌ Error en el servidor, intenta de nuevo.", "error");
            console.error("Error en login:", error);
        }
    });
});
