document.addEventListener("DOMContentLoaded", async () => {
    await fetchCategoryTypes();
    populateYearFilter();
    createFilterRow(); // ✅ Agregar filtros en la parte superior
    document.getElementById("yearFilter").addEventListener("change", applyFilters);
});

const addedCategoryTypes = new Set();

const months = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
];

async function fetchCategoryTypes() {
    try {
        const response = await fetch('/api/balance/categoryTypes');
        if (!response.ok) throw new Error('Error al obtener categoryTypes');

        const categoryTypes = await response.json();
        
        for (const categoryType of categoryTypes) {
            await fetchCategories(categoryType);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function fetchCategories(categoryType) {
    try {
        const response = await fetch(`/api/balance/category?category_type_id=${categoryType.id}`);
        if (!response.ok) throw new Error('Error al obtener categorías');

        const categories = await response.json();
        
        for (const category of categories) {
            await fetchSubCategories(categoryType, category);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function fetchSubCategories(categoryType, category) {
    try {
        const response = await fetch(`/api/balance/subCategory?category_id=${category.id}`);
        if (!response.ok) throw new Error('Error al obtener subcategorías');

        const subCategories = await response.json();

        renderRow(categoryType, category, subCategories);
        renderCategory(categoryType, category, subCategories);
    } catch (error) {
        console.error('Error:', error);
    }
}

function renderRow(categoryType, category, subCategories) {
    const tableBody = document.getElementById("balanceTableBody");
    if (!tableBody) {
        console.error("Elemento balanceTableBody no encontrado");
        return;
    }

    let categoryTypeName = "";
    if (!addedCategoryTypes.has(categoryType.name)) {
        categoryTypeName = categoryType.name;
        addedCategoryTypes.add(categoryType.name);
    }

    if (subCategories.length === 0) {
        tableBody.innerHTML += `
            <tr>
                <td class="border p-2">${categoryTypeName}</td>
                <td class="border p-2">${category.name}</td>
                <td class="border p-2">${createMonthSelect()}</td>
                <td class="border p-2">${createMonthSelect()}</td>
            </tr>`;
    } else {
        subCategories.forEach((subCategory, index) => {
            tableBody.innerHTML += `
                <tr>
                    <td class="border p-2">${index === 0 ? categoryTypeName : ""}</td>
                    <td class="border p-2">${index === 0 ? category.name : ""}</td>
                    <td class="border p-2">${subCategory.name || createMonthSelect()}</td>
                    <td class="border p-2">${createMonthSelect()}</td>
                </tr>`;
        });
    }
}

function createMonthSelect() {
    let select = `<select class="border p-1 rounded w-full">
        <option value="">...</option>`; // Opción vacía inicial
    ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        .forEach((month, index) => {
            select += `<option value="${index + 1}">${month}</option>`;
        });
    select += `</select>`;
    return select;
}

function renderCategory(categoryType, category, subCategories) {
    const container = document.getElementById("balanceContainer");
    if (!container) {
        console.error("Elemento balanceContainer no encontrado");
        return;
    }

    let categoryHTML = "";

    if (!addedCategoryTypes.has(categoryType.name)) {
        categoryHTML += `
            <div class="mb-4">
                <h2 class="text-xl font-bold text-gray-800 text-center bg-gray-200 p-2 rounded-md">${categoryType.name}</h2>
            </div>`;
        addedCategoryTypes.add(categoryType.name);
    }

    categoryHTML += `
        <div class="border bg-gray-300 p-2 rounded-t-lg text-center font-semibold">${category.name}</div>
        <div class="border border-t-0 p-2 space-y-1">`;

    subCategories.forEach(subCategory => {
        categoryHTML += `
            <div class="flex space-x-2 bg-white p-2 border rounded shadow-sm">
                <div class="flex-1">${subCategory.name}</div>
                <input type="text" class="border p-1 rounded w-24 text-center" placeholder="..." />
                <input type="text" class="border p-1 rounded w-24 text-center" placeholder="..." />
            </div>`;
    });

    categoryHTML += `
        <button class="w-full bg-yellow-500 text-white py-1 mt-2 rounded hover:bg-yellow-600"
            onclick="openAddSubCategoryModal(${category.id})">
            + Añadir
        </button>
    </div>`;

    container.innerHTML += categoryHTML;
}

function openAddSubCategoryModal(categoryId) {
    const modal = document.getElementById("addSubCategoryModal");
    const modalContent = modal.querySelector("div");

    document.getElementById("categoryIdInput").value = categoryId;
    modal.classList.remove("hidden");

    setTimeout(() => {
        modalContent.classList.remove("scale-95", "opacity-0");
        modalContent.classList.add("scale-100", "opacity-100");
    }, 50);
}

function closeAddSubCategoryModal() {
    const modal = document.getElementById("addSubCategoryModal");
    const modalContent = modal.querySelector("div");

    modalContent.classList.remove("scale-100", "opacity-100");
    modalContent.classList.add("scale-95", "opacity-0");

    setTimeout(() => {
        modal.classList.add("hidden");
    }, 300);
}

async function submitSubCategory() {
    const categoryId = document.getElementById("categoryIdInput").value;
    const subCategoryName = document.getElementById("subCategoryNameInput").value;

    if (!subCategoryName.trim()) {
        alert("Por favor ingrese un nombre válido.");
        return;
    }

    const requestBody = {
        category_id: parseInt(categoryId),
        sub_category_name: subCategoryName
    };

    try {
        const response = await fetch('/api/balance/subCategory', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });

        if (!response.ok) throw new Error('Error al agregar subcategoría');

        showNotification("✅ Subcategoría añadida con éxito.", "success");
        closeAddSubCategoryModal();
        setTimeout(() => location.reload(), 1500);
    } catch (error) {
        console.error('Error:', error);
        showNotification("❌ Hubo un error al añadir la subcategoría.", "error");
    }
}
// ✅ Logout
function logout() {
    Swal.fire({
        title: "¿Estás seguro?",
        text: "Tu sesión se cerrará y serás redirigido al inicio de sesión.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: "Sí, cerrar sesión",
        cancelButtonText: "Cancelar"
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                title: "Cerrando sesión...",
                text: "Espere un momento.",
                icon: "success",
                timer: 2000,
                showConfirmButton: false
            }).then(() => {
                window.location.href = "/api/users/login";
            });
        }
    });
}

// ✅ Mostrar notificación
function showNotification(message, type = "success") {
    const notificationContainer = document.getElementById("notificationContainer");

    const bgColor = type === "success" ? "bg-green-500" : "bg-red-500";
    const notification = document.createElement("div");
    notification.className = `flex items-center ${bgColor} text-white px-4 py-2 rounded shadow-md`;
    notification.innerHTML = `<span class="flex-1">${message}</span>
        <button class="ml-4 text-white font-bold" onclick="this.parentElement.remove()">✖</button>`;

    notificationContainer.appendChild(notification);
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

function populateYearFilter() {
    const yearFilter = document.getElementById("yearFilter");
    const currentYear = new Date().getFullYear();
    
    for (let year = currentYear; year >= currentYear - 10; year--) {
        const option = document.createElement("option");
        option.value = year;
        option.textContent = year;
        yearFilter.appendChild(option);
    }
}

document.getElementById('menuToggle').addEventListener('click', function () {
    let menu = document.getElementById('menuMobile');
    menu.classList.toggle('hidden');

    if (!menu.classList.contains('hidden')) {
        menu.classList.remove('scale-95', 'opacity-0');
        menu.classList.add('scale-100', 'opacity-100');
    } else {
        menu.classList.remove('scale-100', 'opacity-100');
        menu.classList.add('scale-95', 'opacity-0');
    }
});

function applyFilters() {
    const selectedYear = document.getElementById("yearFilter").value;
    console.log(`Filtrando por el año: ${selectedYear}`);

    // Aquí puedes agregar lógica para filtrar los datos basados en el año seleccionado
}
function createFilterRow() {
    const tableHead = document.getElementById("balanceTableHead");
    if (!tableHead) {
        console.error("Elemento balanceTableHead no encontrado");
        return;
    }

    tableHead.innerHTML = `
        <tr>
            <th class="border p-2">Categoría</th>
            <th class="border p-2">Subcategoría</th>
            <th class="border p-2">
                Año: ${createYearSelect("yearFilter1")} 
                Mes: ${createMonthSelect("monthFilter1")}
            </th>
            <th class="border p-2">
                Año: ${createYearSelect("yearFilter2")} 
                Mes: ${createMonthSelect("monthFilter2")}
            </th>
        </tr>`;

    document.getElementById("yearFilter1").addEventListener("change", applyFilters);
    document.getElementById("monthFilter1").addEventListener("change", applyFilters);
    document.getElementById("yearFilter2").addEventListener("change", applyFilters);
    document.getElementById("monthFilter2").addEventListener("change", applyFilters);
}

window.logout = logout;
window.openAddSubCategoryModal = openAddSubCategoryModal;
window.closeAddSubCategoryModal = closeAddSubCategoryModal;
window.submitSubCategory = submitSubCategory;