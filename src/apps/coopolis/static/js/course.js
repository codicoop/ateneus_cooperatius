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
  window.scrollTo(0,200)
}

function goToMyCourses(url) {
  window.location.replace(url)
}

function toggleSession(event) {
  const parent = event.target.parentElement
  parent.classList.toggle("is-open")
}
