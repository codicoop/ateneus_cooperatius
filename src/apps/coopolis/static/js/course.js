function openSessionCard(event) {
  const card = event.target.parentElement
  // Adding class for styling
  card.classList.add("is-open")
  // Hidding the opening button
  const openBtn = card.querySelector(".action-open")
  openBtn.classList.add("is-hidden")
  // Showing the closing button
  const closeBtn = card.querySelector(".action-close")
  closeBtn.classList.remove("is-hidden")
}

function closeSessionCard(event) {
  const card = event.target.parentElement
  // Removing class for styling
  card.classList.remove("is-open")
  // Hidding the opening button
  const openBtn = card.querySelector(".action-open")
  openBtn.classList.remove("is-hidden")
  // Showing the closing button
  const closeBtn = card.querySelector(".action-close")
  closeBtn.classList.add("is-hidden")
}

function showDeleteModal(event) {
  const card = event.target.parentElement.parentElement.parentElement
  const modal = card.querySelector(".delete-modal")
  modal.classList.remove("is-hidden")
}

function copyVideocallUrl(link) {
  const alert = document.querySelector(".copied_alert")
  // Copiem el link
  navigator.clipboard.writeText(link)
  // Mostrem el missatge
  alert.classList.remove("is-hidden")
  // L'amaguem al cap de poc
  setTimeout(el => {
    alert.classList.add("is-hidden")
  }, 1000)
}

function toggleSection(event) {
  const parent = event.target.parentElement.parentElement
  const thisSection = event.target.parentElement
  const allSections = parent.querySelectorAll(".section")
  allSections.forEach(el => {
    el.classList.remove("is-open")
  });
  thisSection.classList.add("is-open")
}

function goToMyCourses(url) {
  console.log(url)
  window.location.replace(url)
}

function toggleSession(event) {
  const parent = event.target.parentElement.parentElement
  parent.classList.toggle("is-open")
}
