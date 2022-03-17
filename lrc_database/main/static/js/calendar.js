document.addEventListener('DOMContentLoaded', function () {
  let calendarEl = document.getElementById('calendar');
  let calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    themeSystem: 'bootstrap5',
    events: events,
  });
  calendar.render();
});
