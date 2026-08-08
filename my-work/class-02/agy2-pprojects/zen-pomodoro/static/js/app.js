/**
 * Zen Pomodoro — Main Application State Machine & Task Manager
 */

document.addEventListener('DOMContentLoaded', () => {
  // --- Timer State ---
  let state = {
    mode: 'focus', // 'focus', 'shortBreak', 'longBreak'
    minutes: 25,
    seconds: 0,
    totalSeconds: 25 * 60,
    remainingSeconds: 25 * 60,
    isRunning: false,
    intervalId: null,
    activeTaskId: null,
    completedCycles: 0,
    settings: {
      focus_duration: 25,
      short_break_duration: 5,
      long_break_duration: 15,
      long_break_interval: 4,
      auto_start_breaks: false,
      theme: 'serene-forest'
    }
  };

  // --- DOM Elements ---
  const timerDigits = document.getElementById('timerDigits');
  const timerStateLabel = document.getElementById('timerStateLabel');
  const playPauseBtn = document.getElementById('playPauseBtn');
  const playPauseIcon = document.getElementById('playPauseIcon');
  const resetBtn = document.getElementById('resetBtn');
  const skipBtn = document.getElementById('skipBtn');
  const progressCircle = document.querySelector('.progress-ring-circle');
  const modeBtns = document.querySelectorAll('.mode-btn');
  const activeTaskTitle = document.getElementById('activeTaskTitle');

  // Task Elements
  const taskForm = document.getElementById('taskForm');
  const taskInput = document.getElementById('taskInput');
  const taskCategorySelect = document.getElementById('taskCategorySelect');
  const taskEstSelect = document.getElementById('taskEstSelect');
  const taskList = document.getElementById('taskList');

  // Stats Elements
  const statFocusMinutes = document.getElementById('statFocusMinutes');
  const statSessions = document.getElementById('statSessions');
  const statCompletedTasks = document.getElementById('statCompletedTasks');

  // Ambient Buttons
  const ambientBtns = document.querySelectorAll('.ambient-btn');

  // Modal Elements
  const settingsBtn = document.getElementById('settingsBtn');
  const settingsModal = document.getElementById('settingsModal');
  const modalCloseBtn = document.getElementById('modalCloseBtn');
  const settingsForm = document.getElementById('settingsForm');
  const themeOptions = document.querySelectorAll('.theme-option');

  // Circle Perimeter
  const CIRCLE_RADIUS = 130;
  const CIRCLE_PERIMETER = 2 * Math.PI * CIRCLE_RADIUS; // ~816

  if (progressCircle) {
    progressCircle.style.strokeDasharray = `${CIRCLE_PERIMETER} ${CIRCLE_PERIMETER}`;
    progressCircle.style.strokeDashoffset = '0';
  }

  // Fetch initial data
  initApp();

  function initApp() {
    fetch('/api/settings')
      .then(res => res.json())
      .then(settings => {
        state.settings = settings;
        applyTheme(settings.theme || 'serene-forest');
        setMode('focus');
      });

    loadTasks();
    loadStats();
  }

  // --- Timer Operations ---

  function setMode(mode) {
    state.mode = mode;
    state.isRunning = false;
    clearInterval(state.intervalId);

    // Set duration based on settings
    let durationMins = state.settings.focus_duration;
    let label = 'Focus Session';

    if (mode === 'shortBreak') {
      durationMins = state.settings.short_break_duration;
      label = 'Short Break';
    } else if (mode === 'longBreak') {
      durationMins = state.settings.long_break_duration;
      label = 'Long Break';
    }

    state.minutes = durationMins;
    state.seconds = 0;
    state.totalSeconds = durationMins * 60;
    state.remainingSeconds = durationMins * 60;

    // Update Mode Buttons UI
    modeBtns.forEach(btn => {
      if (btn.getAttribute('data-mode') === mode) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });

    if (timerStateLabel) timerStateLabel.textContent = label;
    updateTimerDisplay();
    updatePlayPauseIcon();
  }

  function toggleTimer() {
    window.zenAudio.init(); // Resume Web Audio context

    if (state.isRunning) {
      pauseTimer();
    } else {
      startTimer();
    }
  }

  function startTimer() {
    state.isRunning = true;
    updatePlayPauseIcon();

    state.intervalId = setInterval(() => {
      if (state.remainingSeconds > 0) {
        state.remainingSeconds--;
        updateTimerDisplay();
      } else {
        onTimerComplete();
      }
    }, 1000);
  }

  function pauseTimer() {
    state.isRunning = false;
    clearInterval(state.intervalId);
    updatePlayPauseIcon();
  }

  function resetTimer() {
    pauseTimer();
    state.remainingSeconds = state.totalSeconds;
    updateTimerDisplay();
  }

  function skipTimer() {
    pauseTimer();
    if (state.mode === 'focus') {
      state.completedCycles++;
      if (state.completedCycles % state.settings.long_break_interval === 0) {
        setMode('longBreak');
      } else {
        setMode('shortBreak');
      }
    } else {
      setMode('focus');
    }
  }

  function updateTimerDisplay() {
    const mins = Math.floor(state.remainingSeconds / 60);
    const secs = state.remainingSeconds % 60;
    const formatted = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;

    if (timerDigits) timerDigits.textContent = formatted;

    // Update Document Title
    const icon = state.mode === 'focus' ? '🧘' : '☕';
    document.title = `${formatted} ${icon} Zen Pomodoro`;

    // Update SVG Progress Ring
    if (progressCircle && state.totalSeconds > 0) {
      const progressFraction = state.remainingSeconds / state.totalSeconds;
      const offset = CIRCLE_PERIMETER * (1 - progressFraction);
      progressCircle.style.strokeDashoffset = offset;
    }
  }

  function updatePlayPauseIcon() {
    if (playPauseIcon) {
      if (state.isRunning) {
        playPauseIcon.className = 'fa-solid fa-pause';
      } else {
        playPauseIcon.className = 'fa-solid fa-play';
      }
    }
  }

  function onTimerComplete() {
    pauseTimer();
    
    // Play soothing Zen bowl chime sound
    if (window.zenAudio) {
      window.zenAudio.playCompletionChime();
    }

    // Send session completion log to server
    const payload = {
      task_id: state.activeTaskId,
      duration_minutes: Math.round(state.totalSeconds / 60),
      type: state.mode
    };

    fetch('/api/sessions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
      .then(res => res.json())
      .then(data => {
        updateStatsUI(data.stats);
        renderTaskList(data.tasks);
      })
      .catch(err => console.error("Error recording session:", err));

    // Handle transition to next mode
    if (state.mode === 'focus') {
      state.completedCycles++;
      if (state.completedCycles % state.settings.long_break_interval === 0) {
        setMode('longBreak');
      } else {
        setMode('shortBreak');
      }
    } else {
      setMode('focus');
    }

    // Auto start if enabled
    if (state.settings.auto_start_breaks && state.mode !== 'focus') {
      startTimer();
    }
  }

  // --- Task Operations ---

  function loadTasks() {
    fetch('/api/tasks')
      .then(res => res.json())
      .then(tasks => renderTaskList(tasks));
  }

  function renderTaskList(tasks) {
    if (!taskList) return;

    if (!tasks || tasks.length === 0) {
      taskList.innerHTML = `
        <div style="text-align:center; padding:24px; color:var(--text-dim);">
          <p>No tasks added yet. Add a task above to begin focusing!</p>
        </div>
      `;
      if (activeTaskTitle) activeTaskTitle.textContent = "Select a task to focus on";
      return;
    }

    let activeTask = tasks.find(t => t.is_active) || tasks[0];
    if (activeTask) {
      state.activeTaskId = activeTask.id;
      if (activeTaskTitle) {
        activeTaskTitle.innerHTML = `
          <strong>Active Task:</strong> ${escapeHtml(activeTask.title)} 
          <span style="opacity:0.8; margin-left:6px;">(${activeTask.completed_pomodoros} / ${activeTask.est_pomodoros} 🍅)</span>
        `;
      }
    }

    taskList.innerHTML = tasks.map(task => `
      <div class="task-item ${task.completed ? 'completed' : ''} ${task.id === state.activeTaskId ? 'active' : ''}" data-id="${task.id}">
        <input type="checkbox" class="task-checkbox" ${task.completed ? 'checked' : ''} data-id="${task.id}">
        
        <div class="task-details" style="cursor:pointer;" data-id="${task.id}">
          <div class="task-title">${escapeHtml(task.title)}</div>
          <div class="task-meta">
            <span class="task-tag">${escapeHtml(task.category)}</span>
            <span>🍅 ${task.completed_pomodoros} / ${task.est_pomodoros}</span>
          </div>
        </div>

        <button class="task-action-btn delete-task-btn" data-id="${task.id}" title="Delete Task">
          <i class="fa-solid fa-trash-can"></i>
        </button>
      </div>
    `).join('');
  }

  if (taskForm) {
    taskForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const title = taskInput.value.trim();
      if (!title) return;

      const category = taskCategorySelect ? taskCategorySelect.value : 'Work';
      const est_pomodoros = taskEstSelect ? parseInt(taskEstSelect.value) : 1;

      fetch('/api/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, category, est_pomodoros })
      })
        .then(res => res.json())
        .then(newTask => {
          taskInput.value = '';
          loadTasks();
        });
    });
  }

  // Delegate task clicks (check, select active, delete)
  if (taskList) {
    taskList.addEventListener('click', (e) => {
      const target = e.target;
      const taskId = target.getAttribute('data-id') || target.closest('[data-id]')?.getAttribute('data-id');

      if (!taskId) return;

      if (target.classList.contains('task-checkbox')) {
        // Toggle completed
        const isChecked = target.checked;
        fetch(`/api/tasks/${taskId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ completed: isChecked })
        })
          .then(res => res.json())
          .then(() => {
            loadTasks();
            loadStats();
          });
      } else if (target.closest('.delete-task-btn')) {
        // Delete task
        fetch(`/api/tasks/${taskId}`, { method: 'DELETE' })
          .then(res => res.json())
          .then(() => loadTasks());
      } else {
        // Select active task
        fetch(`/api/tasks/${taskId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ is_active: true })
        })
          .then(res => res.json())
          .then(() => loadTasks());
      }
    });
  }

  // --- Productivity Stats ---

  function loadStats() {
    fetch('/api/stats')
      .then(res => res.json())
      .then(stats => updateStatsUI(stats));
  }

  function updateStatsUI(stats) {
    if (statFocusMinutes) statFocusMinutes.textContent = stats.total_focus_minutes || 0;
    if (statSessions) statSessions.textContent = stats.total_sessions || 0;
    if (statCompletedTasks) statCompletedTasks.textContent = stats.completed_tasks || 0;
  }

  // --- Ambient Sound Controller ---

  ambientBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const type = btn.getAttribute('data-sound');
      const isPlaying = window.zenAudio.toggleAmbience(type);

      ambientBtns.forEach(b => b.classList.remove('active'));
      if (isPlaying) {
        btn.classList.add('active');
      }
    });
  });

  // --- Mode Button Event Handlers ---
  modeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const mode = btn.getAttribute('data-mode');
      setMode(mode);
    });
  });

  if (playPauseBtn) playPauseBtn.addEventListener('click', toggleTimer);
  if (resetBtn) resetBtn.addEventListener('click', resetTimer);
  if (skipBtn) skipBtn.addEventListener('click', skipTimer);

  // --- Settings & Theme Modal ---

  if (settingsBtn) {
    settingsBtn.addEventListener('click', () => {
      settingsModal.classList.add('open');
      // Populate form
      document.getElementById('focusMinsInput').value = state.settings.focus_duration;
      document.getElementById('shortBreakMinsInput').value = state.settings.short_break_duration;
      document.getElementById('longBreakMinsInput').value = state.settings.long_break_duration;
    });
  }

  if (modalCloseBtn) {
    modalCloseBtn.addEventListener('click', () => settingsModal.classList.remove('open'));
  }

  themeOptions.forEach(opt => {
    opt.addEventListener('click', () => {
      themeOptions.forEach(o => o.classList.remove('active'));
      opt.classList.add('active');
      const theme = opt.getAttribute('data-theme');
      applyTheme(theme);
    });
  });

  if (settingsForm) {
    settingsForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const focus_duration = parseInt(document.getElementById('focusMinsInput').value);
      const short_break_duration = parseInt(document.getElementById('shortBreakMinsInput').value);
      const long_break_duration = parseInt(document.getElementById('longBreakMinsInput').value);
      const activeThemeOpt = document.querySelector('.theme-option.active');
      const theme = activeThemeOpt ? activeThemeOpt.getAttribute('data-theme') : state.settings.theme;

      const newSettings = {
        focus_duration,
        short_break_duration,
        long_break_duration,
        theme
      };

      fetch('/api/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newSettings)
      })
        .then(res => res.json())
        .then(settings => {
          state.settings = settings;
          setMode(state.mode);
          settingsModal.classList.remove('open');
        });
    });
  }

  function applyTheme(theme) {
    document.body.setAttribute('data-theme', theme);
    themeOptions.forEach(opt => {
      if (opt.getAttribute('data-theme') === theme) {
        opt.classList.add('active');
      } else {
        opt.classList.remove('active');
      }
    });
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
});
