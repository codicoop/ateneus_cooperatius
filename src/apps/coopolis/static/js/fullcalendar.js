
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
          'title': 'Event 1 hardcodejat de prova',
          'start': '2023-11-01',
          'url': 'hola',
          'className': 'calendar-event',
          'display': 'block',
          'cercle': 'red',
          'session_num': '1',
          'session_total': '3',
      },
      {
          'title': 'Event 2 hardcodejat de prova',
          'start': '2023-11-09',
          'url': 'hola',
          'className': 'calendar-event',
          'display': 'block',
          'cercle': 'violet',
          'session_num': '1',
          'session_total': '3',
      },
      {
          'title': 'Event 3 hardcodejat de prova',
          'start': '2023-11-09',
          'url': 'hola',
          'className': 'calendar-event',
          'display': 'block',
          'cercle': 'blue',
          'session_num': '3',
          'session_total': '3',
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
      let eventObj = info.event;
      if (eventObj.url) {
        window.open(eventObj.url);
        info.jsEvent.preventDefault(); // prevents browser from following link in current tab.
      }
    },

  });

  let eventsArray = calendar.getEvents()
  // console.log("events inici", eventsArray)

  // eventsArray.map(el => {
  //   let eventTag = el
  //   console.log("this event", eventTag);
  // })
  // console.log("events final", eventsArray)

  calendar.render();
});