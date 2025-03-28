document.getElementById("generatePasswordForm").addEventListener("submit", async function (event) {
    event.preventDefault();
    const email = document.getElementById("email").value;

    try {
        const response = await fetch("/api/users/generate_password", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email }),
        });

        const data = await response.json();

        if (response.ok) {
            showToast("✅ " + (data.message || "Revisa tu correo para la nueva contraseña."), "success");
        } else {
            showToast("❌ " + (data.error || "Error al generar la contraseña."), "error");
        }
    } catch (error) {
        showToast("❌ Error en la solicitud.", "error");
    }
});


// 🔥 Mostrar notificación de éxito o error
function showToast(message, type = "error") {
    const toastContainer = document.getElementById("toast-container");
    const toast = document.createElement("div");
    toast.classList.add("toast", type);
    toast.innerHTML = message;
    
    toastContainer.appendChild(toast);
    setTimeout(() => {
        toast.remove();
    }, 3000);
}