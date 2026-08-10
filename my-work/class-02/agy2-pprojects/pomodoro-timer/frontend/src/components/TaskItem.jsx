import React from 'react';
import { useTasks } from '../context/TaskContext';

export default function TaskItem({ task }) {
  const { activeTask, toggleTaskCompleted, selectActiveTask, removeTask } = useTasks();

  const isActive = activeTask && activeTask.id === task.id;

  return (
    <div
      className={`task-item ${task.completed ? 'completed' : ''} ${isActive ? 'active' : ''}`}
    >
      <input
        type="checkbox"
        className="task-checkbox"
        checked={!!task.completed}
        onChange={(e) => toggleTaskCompleted(task.id, e.target.checked)}
      />

      <div
        className="task-details"
        style={{ cursor: 'pointer' }}
        onClick={() => selectActiveTask(task.id)}
      >
        <div className="task-title">{task.title}</div>
        <div className="task-meta">
          <span className="task-tag">{task.category || 'Work'}</span>
          <span>🍅 {task.completed_pomodoros || 0} / {task.est_pomodoros || 1}</span>
        </div>
      </div>

      <button
        className="task-action-btn delete-task-btn"
        title="Delete Task"
        onClick={(e) => {
          e.stopPropagation();
          removeTask(task.id);
        }}
      >
        <i className="fa-solid fa-trash-can"></i>
      </button>
    </div>
  );
}
