
// Estilar checkboxes
function onLoadFunction(){
  console.log("Executing onLoadFunction")
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
    if (el.type === "number") {
      let numberParent = el.parentElement
      numberParent.classList.add("field")
      numberParent.classList.add("field-number")
    }
    if (el.type === "file") {
      let fileParent = el.parentElement
      fileParent.classList.add("field")
      fileParent.classList.add("field-file")
    }
  })
  // Afegint clases pels selects
  const allSelects = document.querySelectorAll("select")
  allSelects.forEach(el => {
    let selectParent = el.parentElement
    selectParent.classList.add("field")
    selectParent.classList.add("field-select")
  })

  // Afegint clases per les textareas
  const allTeextareas = document.querySelectorAll("textarea")
  allTeextareas.forEach(el => {
    let textareaParent = el.parentElement
    textareaParent.classList.add("field")
    textareaParent.classList.add("field-textarea")
  })

  const registerPage = document.querySelector("signup")

  if (registerPage) {
    // Afegint una clase a casos específics de checkbox
    const readAcceptedOne = document.querySelector("#id_accept_conditions").parentElement
    const readAcceptedTwo = document.querySelector("#id_accept_conditions2").parentElement
  
    readAcceptedOne.classList.add("field-checkbox--long")
    readAcceptedTwo.classList.add("field-checkbox--long")
  }
}