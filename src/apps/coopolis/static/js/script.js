// Obrir i tancar el menú
function openMenu() {
  const menu = document.querySelector(".sidebar")
  menu.classList.add("menu-is-open")
}
function closeMenu() {
  const menu = document.querySelector(".sidebar")
  menu.classList.remove("menu-is-open")
}
// Mostrar el formulari de login
function showLoginFloat() {
  const login = document.querySelector(".login")
  login.classList.remove("is-hidden")
  window.scrollTo(top)
}
function hideLoginFloat() {
  const login = document.querySelector(".login")
  login.classList.add("is-hidden")
}
function toggleDistrict() {
  // Mostrant districte només si Barcelona
  const townInput = document.querySelector("#id_town")
  const districtField = document.querySelector("#id_district").parentElement
  
  if (townInput.value === "90") {
    districtField.classList.remove("is-hidden")
  } else {
    districtField.classList.add("is-hidden")
    districtField.value = ""
  }
}
function hideMessageModal(event) {
  if (event.target.classList.contains("modal__close")) {
    const modal = event.target.parentElement.parentElement
    modal.classList.add("is-hidden")
  }
  if (event.target.classList.contains("modal__background")) {
    const modal = event.target.parentElement
    modal.classList.add("is-hidden")
  }
}
function showModal(event) {
  const card = event.target.parentElement.parentElement.parentElement
  const modal = card.querySelector(".modal")
  modal.classList.remove("is-hidden")
}

function hideModal(event) {
  if (event.target.classList.contains("modal__close")) {
    const modal = event.target.parentElement.parentElement
    modal.classList.add("is-hidden")
  }
  if (event.target.classList.contains("modal__background")) {
    const modal = event.target.parentElement
    modal.classList.add("is-hidden")
  }
}

function blockIdNumber() {
  const idInput = document.getElementById("id_id_number")
  const idInputType = document.getElementById("id_id_number_type")
  const newValue = idInputType.value
  const helptext = idInput.parentElement.querySelector(".helptext")

  if (newValue === "NO_DNI") {
    // Bloquejar el camp del número
    idInput.value = ""
    idInput.disabled = true
    // Ensenyar el camp helptext
    helptext.style.display = "block"
  } else {
    // Habilitar el camp del número
    idInput.disabled = false
    // Amagar el camp helptext
    helptext.style.display = "none"
  }
}