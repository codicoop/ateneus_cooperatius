
document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');

  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    locale: 'ca',
    firstDay: '1',
    dayHeaders: false,
    headerToolbar: {
      left: 'prev',
      center: 'title',
      right: 'next'
    },
    weekends: true,
    views: {
      dayGridMonth: {
        // Date Clicking & Selecting:
        selectable: true,
        selectMirror: false,
        // Time Grid:
        allDaySlot: false,
        expandRows: true,
      },
    },
    events: [
      {
        // Per cada event necessito aquests camps amb aquests noms
        // Per fer-los servir amb el Fullcalendar
        // Títol de l'esdeveniment
        'title': 'Event 1 hardcodejat de prova',
        // Data esdeveniment
        'start': '2024-06-05',
        'className': 'calendar-event',
        'display': 'block',
        // Codi de color
        'cercle': 'red',
        // Número de sessió
        'session_num': '1',
        // Total de sessions del pack
        'session_total': '3',
        // Url de la pàgina de la sessió. Important que aquesta
        // variable no es digui 'url' perquè necessitem saltar-nos
        // el comportament default del calendari per mostrar el 
        // modal, però encara necessito saber la url per després
        'url_page': '',
        
        // Però també necessito la resta de la info, perquè al fer click
        // al calendari s'obre un modal amb tota la fitxa
        // el format d'això dona igual, però necessito aquests camps
        'id': '12345', //li diu 'publicId'
        'cercle_title': 'Ecofeminismes',
        'description': 'Un programa formatiu i d’acompanyament que neix amb la voluntat d’augmentar i enfortir les iniciatives cooperatives, i de l’ESS, que treballen en pro de la transició ecològica en el context urbà.',
        // Adreçat a:
        'target': 'Persones i equips que volen crear o consolidar projectes socioeconòmics que situen el seu àmbit d’acció en sectors estratègics per la transició ecològica i/o que incorporen la sostenibilitat ambiental en la intencionalitat del projecte.',
        'tags': ['tag 1', 'tag2', 'Presencial'],
        'sessions': [
          // Per cada sessió
          {
            'date': '2302-12-12',
            'start_time': '12:00',
            'end_time': '14:00',
            'title': "Sessió de formació en FFCC"
          },
          {
            'date': '2302-12-14',
            'start_time': '12:00',
            'end_time': '14:00',
            'title': "Sessió de formació en FFCC"
          },
          {
            'date': '2302-12-16',
            'start_time': '12:00',
            'end_time': '14:00',
            'title': "Sessió de formació en FFCC"
          },
        ],
      },
      {
        // Per cada event necessito aquests camps amb aquests noms
        // Per fer-los servir amb el Fullcalendar
        // Títol de l'esdeveniment
        'title': 'Event 2 hardcodejat de prova',
        // Data esdeveniment
        'start': '2024-06-05',
        'className': 'calendar-event',
        'display': 'block',
        // Codi de color
        'cercle': 'blue',
        // Número de sessió
        'session_num': '2',
        // Total de sessions del pack
        'session_total': '3',
        // Url de la pàgina de la sessió. Important que aquesta
        // variable no es digui 'url' perquè necessitem saltar-nos
        // el comportament default del calendari per mostrar el 
        // modal, però encara necessito saber la url per després
        'url_page': '',
        
        // Però també necessito la resta de la info, perquè al fer click
        // al calendari s'obre un modal amb tota la fitxa
        // el format d'això dona igual, però necessito aquests camps
        'id': '1234', //li diu 'publicId'
        'cercle_title': 'Ecofeminismes',
        'description': 'Un programa formatiu i d’acompanyament que neix amb la voluntat d’augmentar i enfortir les iniciatives cooperatives, i de l’ESS, que treballen en pro de la transició ecològica en el context urbà.',
        // Adreçat a:
        'target': 'Persones i equips que volen crear o consolidar projectes socioeconòmics que situen el seu àmbit d’acció en sectors estratègics per la transició ecològica i/o que incorporen la sostenibilitat ambiental en la intencionalitat del projecte.',
        'tags': ['tag 1', 'tag2', 'Presencial'],
        'sessions': [
          // Per cada sessió
          {
            'date': '2302-12-12',
            'start_time': '12:00',
            'end_time': '14:00',
            'title': "Sessió de formació en FFCC"
          },
          {
            'date': '2302-12-14',
            'start_time': '12:00',
            'end_time': '14:00',
            'title': "Sessió de formació en FFCC"
          },
          {
            'date': '2302-12-16',
            'start_time': '12:00',
            'end_time': '14:00',
            'title': "Sessió de formació en FFCC"
          },
        ],
      },
      {
        // Per cada event necessito aquests camps amb aquests noms
        // Per fer-los servir amb el Fullcalendar
        // Títol de l'esdeveniment
        'title': 'Event 3 hardcodejat de prova',
        // Data esdeveniment
        'start': '2023-11-04',
        'className': 'calendar-event',
        'display': 'block',
        // Codi de color
        'cercle': 'red',
        // Número de sessió
        'session_num': '3',
        // Total de sessions del pack
        'session_total': '3',
        // Url de la pàgina de la sessió. Important que aquesta
        // variable no es digui 'url' perquè necessitem saltar-nos
        // el comportament default del calendari per mostrar el 
        // modal, però encara necessito saber la url per després
        'url_page': '',
        
        // Però també necessito la resta de la info, perquè al fer click
        // al calendari s'obre un modal amb tota la fitxa
        // el format d'això dona igual, però necessito aquests camps
        'id': '123456', //li diu 'publicId'
        'cercle_title': 'Ecofeminismes',
        'description': 'Un programa formatiu i d’acompanyament que neix amb la voluntat d’augmentar i enfortir les iniciatives cooperatives, i de l’ESS, que treballen en pro de la transició ecològica en el context urbà.',
        // Adreçat a:
        'target': 'Persones i equips que volen crear o consolidar projectes socioeconòmics que situen el seu àmbit d’acció en sectors estratègics per la transició ecològica i/o que incorporen la sostenibilitat ambiental en la intencionalitat del projecte.',
        'tags': ['tag 1', 'tag2', 'Presencial'],
        'sessions': [
          // Per cada sessió
          {
            'date': '2302-12-12',
            'start_time': '12:00',
            'end_time': '14:00',
            'title': "Sessió de formació en FFCC"
          },
          {
            'date': '2302-12-14',
            'start_time': '12:00',
            'end_time': '14:00',
            'title': "Sessió de formació en FFCC"
          },
          {
            'date': '2302-12-16',
            'start_time': '12:00',
            'end_time': '14:00',
            'title': "Sessió de formació en FFCC"
          },
        ],
      },
    ],
    // events: {
    // // url: '/reservations/ajax/calendar/',
    //   error: function() {
    //       alert("No s'han pogut carregar les reserves. Recarrega la pàgina i si d'aquí uns minuts segueix fallant, si us plau avisa'ns.");
    //   }
    // },
    eventDidMount: function(info) {
      let pill = document.createElement("div");
      let session_num = info.event._def.extendedProps['session_num'];
      let session_total = info.event._def.extendedProps['session_total'];
      let color = info.event._def.extendedProps['cercle'];

      if (session_num && session_total) {
        pill.classList.add("calendar-event__top", "text-xsm")
        pill.style.borderTop = `2px ${color} solid`
        pill.style.color = color
        pill.innerText = `${session_num}/${session_total}`;
        let fctitle = info.el.querySelector('.fc-event-title-container');
        fctitle.append(pill)
      }
    },
    eventClick: function(info) {
      // console.log("info click", info)
      if (info.event._def.publicId) {
        let thisModal = document.getElementById(`${info.event._def.publicId}`)
        thisModal.classList.remove("is-hidden")

        window.scrollTo(0,0)
      }
    },
  });

  calendar.render();
});