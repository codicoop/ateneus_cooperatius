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
function showFilters(event) {
  const parent = event.target.parentElement
  const overlay = parent.querySelector(".overlay")
  overlay.classList.remove("is-hidden")
}
function hideFilters(event) {
  console.log(event.target)
  if (event.target.classList.contains("overlay__close")) {
    const overlay = event.target.parentElement.parentElement
    overlay.classList.add("is-hidden")
  }
  if (event.target.classList.contains("overlay__background")) {
    const overlay = event.target.parentElement
    overlay.classList.add("is-hidden")
  }
}
function toggleFilterOption(event) {
  console.log(event.target);
  const parent = event.target.parentElement
  const overlay = parent.querySelector(".overlay__option-list")
  const separator = parent.querySelector(".list-separator")
  overlay.classList.toggle("is-hidden")
  separator.classList.toggle("is-hidden")
  parent.classList.toggle("is-open")
}
function toggleFilterDates(event) {
  console.log(event.target);
  const parent = event.target.parentElement
  const overlay = parent.querySelector(".overlay__option-dates")
  const separator = parent.querySelector(".list-separator")
  overlay.classList.toggle("is-hidden")
  separator.classList.toggle("is-hidden")
  parent.classList.toggle("is-open")
}