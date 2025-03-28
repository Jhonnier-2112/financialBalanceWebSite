document.getElementById("resetPasswordForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const currentPassword = document.getElementById("current_password").value;
    const newPassword = document.getElementById("new_password").value;
    const confirmPassword = document.getElementById("confirm_password").value;

    // Validar que las contraseñas coincidan
    if (newPassword !== confirmPassword) {
        showToast("❌ Las contraseñas no coinciden", "error");
        return;
    }

    try {
        const response = await fetch("/api/users/reset_password", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                email: email,
                current_password: currentPassword,
                new_password: newPassword
            })
        });

        const data = await response.json();

        if (response.ok) {
            showToast("✅ " + (data.message || "Contraseña actualizada con éxito."), "success");
        } else {
            showToast("❌ " + (data.error || "Error al actualizar contraseña."), "error");
        }
    } catch (error) {
        showToast("❌ Error al conectar con el servidor.", "error");
    }
});

// 🔥 Mostrar notificación de éxito o error
function showToast(message, type = "error") {
    const toast = document.createElement("div");
    toast.classList.add("toast", type);
    toast.innerHTML = message;

    document.getElementById("toast-container").appendChild(toast);
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// 👁️ Alternar visibilidad de las contraseñas
document.querySelectorAll(".toggle-password").forEach(button => {
    button.addEventListener("click", function () {
        const passwordInput = this.previousElementSibling;
        const icon = this.querySelector("i");

        passwordInput.type = passwordInput.type === "password" ? "text" : "password";
        icon.classList.toggle("fa-eye");
        icon.classList.toggle("fa-eye-slash");
    });
});
