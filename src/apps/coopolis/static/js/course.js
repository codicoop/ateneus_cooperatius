$( document ).ready(function() {
  makeModal('#modal-confirm');

  var urlParams = new URLSearchParams(window.location.search);
  if (urlParams.has('act')) {
      var id = urlParams.get('act');
      $("#actButton" + id).click();
  }
});

function onInscriptionButtonClick (activityId, activityName, loginsignupUrl, waitingList) {
  console.log(activityId, activityName, loginsignupUrl, waitingList)
  $('#modal-title-text').text(activityName);
  $("#button1").attr("href", loginsignupUrl);
  $('#activity_id').val(activityId);

  if (waitingList) {
      $('#enroll_button').text("Incriure's-hi");
      $('.modal').height(220);
      $('.waiting_list_p').hide();
  } else {
      $('#enroll_button').text("Entrar en llista d'espera");
      $('.modal').height(290);
      $('.waiting_list_p').show();
  }
  showModal('#modal-confirm');
}

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