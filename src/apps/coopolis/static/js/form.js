
// Estilar checkboxes
function onLoadFunction(){
  // Trobar els inputs de la pàgina
  const allInputs = document.querySelectorAll("input")
  // Afegint clases pels diferents tipus de inputs
  allInputs.forEach(el => {
    if (el.type === "text" || el.type === "email" || el.type === "password") {
      let checkboxParent = el.parentElement
      checkboxParent.classList.add("field")
    }
    if (el.type === "checkbox") {
      let checkboxParent = el.parentElement
      checkboxParent.classList.add("field-checkbox")
    }
  })
  // Afegint clases pels selects
  const allSelects = document.querySelectorAll("select")
  allSelects.forEach(el => {
    let selectParent = el.parentElement
    selectParent.classList.add("field")
    selectParent.classList.add("field-select")
  })
  // Afegint una clase a casos específics de checkbox
  const readAcceptedOne = document.querySelector("#id_accept_conditions").parentElement
  const readAcceptedTwo = document.querySelector("#id_accept_conditions2").parentElement

  readAcceptedOne.classList.add("field-checkbox--long")
  readAcceptedTwo.classList.add("field-checkbox--long")
}