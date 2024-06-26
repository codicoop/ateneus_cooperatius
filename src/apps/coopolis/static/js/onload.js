
// Estilar inputs
function onLoadFunction(){
  // Trobar els inputs de la pàgina
  const allInputs = document.querySelectorAll("input")
  allInputs.forEach(el => {
    // Afegint clases pels diferents tipus de inputs
    if (el.type === "text" || el.type === "email" || el.type === "password") {
      let parent = el.parentElement
      parent.classList.add("field")
    }
    if (el.type === "checkbox") {
      let checkboxParent = el.parentElement
      checkboxParent.classList.add("field-checkbox")
    }
    if (el.type === "radio") {
      let radioParent = el.parentElement.parentElement.parentElement
      let labelGeneralRadio = radioParent.previousElementSibling
      let superParent = radioParent.parentElement
      superParent.classList.remove("field")
      radioParent.classList.add("field")
      radioParent.classList.add("field-radio")
      labelGeneralRadio.classList.add("label-radio")
    }
    if (el.type === "number") {
      let numberParent = el.parentElement
      numberParent.classList.add("field-number")
      numberParent.classList.add("field")
    }
    if (el.type === "file") {
      let fileParent = el.parentElement
      let label = el.previousElementSibling
      fileParent.classList.add("field-file")
      fileParent.classList.add("field")
      label.classList.add("upload-icon")

      if (fileParent.classList.contains("field-checkbox")) {
        fileParent.classList.remove("field-checkbox")
        fileParent.classList.add("full")
      }
    }
  })
  // Afegint clases pels selects
  const allSelects = document.querySelectorAll("select")
  allSelects.forEach(el => {
    let selectParent = el.parentElement
    selectParent.classList.add("field-select")
    selectParent.classList.add("field")
  })

  // Afegint clases per les textareas
  const allTeextareas = document.querySelectorAll("textarea")
  allTeextareas.forEach(el => {
    let textareaParent = el.parentElement
    textareaParent.classList.add("field")
    textareaParent.classList.add("field-textarea")
  })

  // Pàgina de registre
  const registerPage = document.querySelector(".signup")

  if (registerPage) {
    // Afegint una clase a casos específics de checkbox
    const readAcceptedOne = document.querySelector("#id_accept_conditions").parentElement
    const readAcceptedTwo = document.querySelector("#id_accept_conditions2").parentElement
  
    readAcceptedOne.classList.add("field-checkbox--long")
    readAcceptedTwo.classList.add("field-checkbox--long")
  }

  // Pàgina de projectes
  const projectPage = document.querySelector(".project")
  const profilePage = document.querySelector(".profile")
  const supportPage = document.querySelector(".support")
  const signupPage = document.querySelector(".signup")

  if (projectPage || registerPage || profilePage || supportPage || signupPage) {
    // Mostrant districte només si Barcelona
    const townInput = document.querySelector("#id_town")
    const districtInput = document.querySelector("#id_district")
    if (districtInput) {
      const districtField = districtInput.parentElement
      districtField.classList.add("is-hidden")
      townInput.onchange = toggleDistrict
      
      if (townInput.value === "90") {
        districtField.classList.remove("is-hidden")
      } else {
        districtField.classList.add("is-hidden")
        districtField.value = ""
      }
    }
  }

  // // Pàgina de perfil
  // if (profilePage) {
  //   let input1 = document.getElementById("id_educational_level").parentElement
  //   let input2 = document.getElementById("id_employment_situation").parentElement
  //   let input3 = document.getElementById("id_discovered_us").parentElement
  //   let input4 = document.getElementById("id_project_involved").parentElement
  // }
}