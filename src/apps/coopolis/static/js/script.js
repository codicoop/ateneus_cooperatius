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
  window.scrollTo(0,0)
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
  if (event.target.classList.contains("overlay__close")) {
    const overlay = event.target.parentElement.parentElement.parentElement
    overlay.classList.add("is-hidden")
  }
  if (event.target.classList.contains("overlay__background")) {
    console.log(event.target)
    const overlay = event.target.parentElement
    overlay.classList.add("is-hidden")
  }
}
function toggleFilterOption(event) {
  const parent = event.target.parentElement
  const overlay = parent.querySelector(".overlay__option-list")
  const separator = parent.querySelector(".list-separator")
  overlay.classList.toggle("is-hidden")
  separator.classList.toggle("is-hidden")
  parent.classList.toggle("is-open")
}
function toggleFilterDates(event) {
  const parent = event.target.parentElement
  const overlay = parent.querySelector(".overlay__option-dates")
  const separator = parent.querySelector(".list-separator")
  overlay.classList.toggle("is-hidden")
  separator.classList.toggle("is-hidden")
  parent.classList.toggle("is-open")
}
function showCalendarView() {
  let calendar = document.querySelector(".courses-list__calendar")
  let list = document.querySelector(".courses-list__grid")
  let calendarBtn = document.querySelector(".calendar-view-btn")
  let listBtn = document.querySelector(".list-view-btn")
  calendar.classList.remove("is-hidden")
  list.classList.add("is-hidden")
  calendarBtn.classList.add("is-active")
  listBtn.classList.remove("is-active")
}
function showListView() {
  let calendar = document.querySelector(".courses-list__calendar")
  let list = document.querySelector(".courses-list__grid")
  let calendarBtn = document.querySelector(".calendar-view-btn")
  let listBtn = document.querySelector(".list-view-btn")
  calendar.classList.add("is-hidden")
  list.classList.remove("is-hidden")
  calendarBtn.classList.remove("is-active")
  listBtn.classList.add("is-active")
}
// Perfil - input imatge
function clickUserProfileFileInput() {
  let input = document.getElementById("profile_image")
  input.click()
}
function clickProjectLogoInput() {
  let input = document.getElementById("id_logo")
  input.click()
}
// Acompanyament - dropdown
function openThisDropdown(event) {
  const thisTopbar = event
  const thisBottom = thisTopbar.nextElementSibling
  thisTopbar.classList.add("is-hidden")
  thisBottom.classList.remove("is-hidden")
}
function closeThisDropdown(event) {
  const thisBottom = event
  const thisTopbar = thisBottom.previousElementSibling
  thisTopbar.classList.remove("is-hidden")
  thisBottom.classList.add("is-hidden")
}