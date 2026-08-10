import React from 'react';
import { useTasks } from '../context/TaskContext';

export default function ActiveTaskBadge() {
  const { activeTask } = useTasks();

  return (
    <div className="active-task-banner">
      <span className="active-task-dot"></span>
      {activeTask ? (
        <span>
          <strong>Active Task:</strong> {activeTask.title}{' '}
          <span style={{ opacity: 0.8, marginLeft: '6px' }}>
            ({activeTask.completed_pomodoros} / {activeTask.est_pomodoros} 🍅)
          </span>
        </span>
      ) : (
        <span>Select a task below to focus on</span>
      )}
    </div>
  );
}
