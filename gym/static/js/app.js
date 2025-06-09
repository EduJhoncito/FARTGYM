// FartGym Admin Interface JavaScript

// Global state management
const AppState = {
  currentUser: null,
  classes: [],          // Array to store all classes
  currentClassId: null  // ID of class for modal
};

// Utility functions
function showMessage(message, type = 'success') {
  document.querySelectorAll('.message').forEach(m => m.remove());
  const div = document.createElement('div');
  div.className = `message ${type}`;
  div.textContent = message;
  const form = document.querySelector('main .add-class-section form, main .auth-form form');
  if (form) {
    form.parentNode.insertBefore(div, form);
    setTimeout(() => div.remove(), 5000);
  }
}

function formatTime(time) {
  const [h] = time.split(':').map(Number);
  if (h === 12) return '12:00 PM';
  if (h === 0) return '12:00 AM';
  return `${h % 12 || 12}:00 ${h < 12 ? 'AM' : 'PM'}`;
}

function getCookie(name) {
  const match = document.cookie.split(';').find(c => c.trim().startsWith(name + '='));
  return match ? match.split('=')[1] : '';
}

// Calendar setup & render
function initializeCalendar() {
  const calendarBody = document.getElementById('calendarBody');
  if (!calendarBody) return;

  const timeSlots = [
    '06:00','07:00','08:00','09:00','10:00','11:00',
    '12:00','13:00','14:00','15:00','16:00','17:00',
    '18:00','19:00','20:00'
  ];
  const days = 6; // Mon-Sat

  calendarBody.innerHTML = '';

  timeSlots.forEach(time => {
    const tr = document.createElement('tr');
    const th = document.createElement('th');
    th.className = 'time-cell';
    th.textContent = formatTime(time);
    tr.appendChild(th);

    for (let day = 1; day <= days; day++) {
      const td = document.createElement('td');
      td.dataset.day = day;
      td.dataset.time = time;
      td.className = 'day-cell';
      tr.appendChild(td);
    }

    calendarBody.appendChild(tr);
  });

  // load sessions
  fetch('/api/sessions/')
    .then(r => r.json())
    .then(data => {
      AppState.classes = data.sessions.map(s => ({
        id: s.id,
        day: s.day,
        time: s.time,
        name: s.name
      }));
      renderClasses();
    })
    .catch(console.error);
}

function renderClasses() {
  document.querySelectorAll('.class-square').forEach(el => el.remove());

  AppState.classes.forEach(cls => {
    const selector = `[data-day="${cls.day}"][data-time="${cls.time}"]`;
    const cell = document.querySelector(selector);
    if (!cell) return;
    const div = document.createElement('div');
    div.className = 'class-square';
    div.textContent = cls.name;
    div.addEventListener('click', () => openClassModal(cls.id));
    cell.appendChild(div);
  });
}

// Add class
function handleAddClass(e) {
  e.preventDefault();
  const day   = document.getElementById('classDay')?.value;
  const time  = document.getElementById('classTime')?.value;
  const name  = document.getElementById('className')?.value;
  if (!day || !time || !name) return;
  if (AppState.classes.some(c => c.day == day && c.time == time)) {
    return showMessage('Slot occupied', 'error');
  }

  fetch('/api/sessions/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({ day, time, name })
  })
  .then(r => r.json())
  .then(sess => {
    AppState.classes.push({ ...sess });
    renderClasses();
    document.getElementById('addClassForm').reset();
    showMessage('Class added', 'success');
  })
  .catch(() => showMessage('Failed to add class', 'error'));
}

function openClassModal(id) {
  // Navega a /class-detail/5/ por ejemplo
  window.location.href = `/class-detail/${id}/`;
}

// Event binding
document.addEventListener('DOMContentLoaded', () => {
  // Bind add class
  document.getElementById('addClassForm')?.addEventListener('submit', handleAddClass);
  // Initialize calendar on dashboard
  if (window.location.pathname.startsWith('/dashboard')) {
    initializeCalendar();
  }
});

// expose for debugging
window.AppState = AppState;