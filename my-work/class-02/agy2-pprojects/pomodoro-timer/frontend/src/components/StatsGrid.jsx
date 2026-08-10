import React from 'react';
import { useTasks } from '../context/TaskContext';

export default function StatsGrid() {
  const { stats } = useTasks();

  return (
    <div className="stats-grid">
      <div className="stat-card">
        <div className="stat-value">{stats?.total_focus_minutes || 0}</div>
        <div className="stat-label">Focus Mins</div>
      </div>

      <div className="stat-card">
        <div className="stat-value">{stats?.total_sessions || 0}</div>
        <div className="stat-label">Sessions</div>
      </div>

      <div className="stat-card">
        <div className="stat-value">{stats?.completed_tasks || 0}</div>
        <div className="stat-label">Finished</div>
      </div>
    </div>
  );
}
