// Referencias a elementos del DOM
const formulario = document.getElementById("formulario");
const registros = []; // arreglo de objetos
const alerta = document.getElementById("alerta");
const divRegistros = document.getElementById("registros");

// Evento de envío del formulario
formulario.addEventListener("submit", function (e) {
  e.preventDefault();
  validarFormulario();
});

// Función de validación
function validarFormulario() {
  const nombre = document.getElementById("nombre2");
  const descripcion = document.getElementById("descripcion");
  const categoria = document.getElementById("categoria");
  let valido = true;

  // Validación nombre
  if (nombre.value.trim().length < 3) {
    nombre.classList.add("is-invalid");
    nombre.classList.remove("is-valid");
    valido = false;
  } else {
    nombre.classList.remove("is-invalid");
    nombre.classList.add("is-valid");
  }

  // Validación descripción
  if (descripcion.value.trim().length < 10) {
    descripcion.classList.add("is-invalid");
    descripcion.classList.remove("is-valid");
    valido = false;
  } else {
    descripcion.classList.remove("is-invalid");
    descripcion.classList.add("is-valid");
  }

  // Validación categoría
  if (categoria.value === "") {
    categoria.classList.add("is-invalid");
    categoria.classList.remove("is-valid");
    valido = false;
  } else {
    categoria.classList.remove("is-invalid");
    categoria.classList.add("is-valid");
  }

  // Si todo es válido, guardar registro en arreglo
  if (valido) {
    const spinner = document.getElementById("spinnerRegistro");
    spinner.classList.remove("d-none");

    setTimeout(() => {
      registros.push({
        nombre: nombre.value,
        descripcion: descripcion.value,
        categoria: categoria.value,
      });

      mostrarMensaje("Registro exitoso", "success");
      formulario.reset();

      nombre.classList.remove("is-valid");
      descripcion.classList.remove("is-valid");
      categoria.classList.remove("is-valid");

      spinner.classList.add("d-none");
    }, 1500);
  }
}

// Función para mostrar mensajes
function mostrarMensaje(texto, tipo) {
  alerta.innerHTML = `<div class="alert alert-${tipo}">${texto}</div>`;
}

// Botón Mostrar
document.getElementById("mostrar").addEventListener("click", () => {
  divRegistros.innerHTML = "";

  if (registros.length === 0) {
    divRegistros.innerHTML = `<div class="alert alert-warning">No hay registros disponibles</div>`;
    return;
  }

  registros.forEach((r, i) => {
    const card = document.createElement("div");
    card.className = "card mb-2 p-2";
    card.innerHTML = `<strong>${i + 1}. ${r.nombre}</strong> - ${r.descripcion} <span class="badge bg-info">${r.categoria}</span>`;
    divRegistros.appendChild(card);
  });
});

// Botón Contar
document.getElementById("contar").addEventListener("click", () => {
  mostrarMensaje(`Total registros: ${registros.length}`, "info");
});

// Botón Eliminar
document.getElementById("eliminar").addEventListener("click", () => {
  registros.length = 0;
  divRegistros.innerHTML = "";
  mostrarMensaje("Todos los registros fueron eliminados", "warning");
});

