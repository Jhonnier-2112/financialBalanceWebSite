document.getElementById('generatePasswordForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const message = document.getElementById('message');
    
    try {
        const response = await fetch('/api/users/generate_password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            message.textContent = "✅ Revisa tu correo para la nueva contraseña.";
            message.classList.add("text-green-600");
        } else {
            message.textContent = "❌ " + (data.message || "Error al generar contraseña.");
            message.classList.add("text-red-600");
        }
    } catch (error) {
        message.textContent = "❌ Error en la solicitud.";
        message.classList.add("text-red-600");
    }
});