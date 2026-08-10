import React, { useState } from 'react';
import { useTasks } from '../context/TaskContext';
import TaskItem from './TaskItem';

export default function TaskManager() {
  const { tasks, addTask, loading } = useTasks();
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState('Work');
  const [estPomodoros, setEstPomodoros] = useState('1');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!title.trim()) return;
    addTask(title.trim(), category, parseInt(estPomodoros));
    setTitle('');
  };

  return (
    <div className="glass-card">
      <div className="panel-title">
        <span>
          <i className="fa-solid fa-list-check" style={{ color: 'var(--accent-primary)', marginRight: '8px' }}></i>
          Focus Tasks
        </span>
      </div>

      {/* Add Task Form */}
      <form onSubmit={handleSubmit} className="task-form">
        <input
          type="text"
          className="task-input"
          placeholder="What are you working on?"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />

        <select
          className="task-select"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        >
          <option value="Work">Work</option>
          <option value="Study">Study</option>
          <option value="Design">Design</option>
          <option value="Personal">Personal</option>
        </select>

        <select
          className="task-select"
          title="Target Pomodoro Cycles"
          value={estPomodoros}
          onChange={(e) => setEstPomodoros(e.target.value)}
        >
          <option value="1">1 🍅</option>
          <option value="2">2 🍅</option>
          <option value="3">3 🍅</option>
          <option value="4">4 🍅</option>
          <option value="5">5 🍅</option>
        </select>

        <button type="submit" className="add-task-btn" title="Add Task">
          +
        </button>
      </form>

      {/* Task Items List */}
      <div className="task-list">
        {loading ? (
          <div style={{ textAlign: 'center', padding: '24px', color: 'var(--text-muted)' }}>
            Loading tasks...
          </div>
        ) : tasks.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '24px', color: 'var(--text-muted)' }}>
            No tasks added yet. Add a task above to begin focusing!
          </div>
        ) : (
          tasks.map((task) => <TaskItem key={task.id} task={task} />)
        )}
      </div>
    </div>
  );
}
