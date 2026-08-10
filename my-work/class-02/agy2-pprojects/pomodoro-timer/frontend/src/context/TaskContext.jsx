import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import * as api from '../services/api';

const TaskContext = createContext();

export function TaskProvider({ children }) {
  const [tasks, setTasks] = useState([]);
  const [stats, setStats] = useState({ total_focus_minutes: 0, total_sessions: 0, completed_tasks: 0 });
  const [activeTask, setActiveTask] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadTasks = useCallback(async () => {
    try {
      const data = await api.fetchTasks();
      setTasks(data);
      const active = data.find(t => t.is_active) || data[0] || null;
      setActiveTask(active);
    } catch (err) {
      console.error('Error fetching tasks:', err);
    }
  }, []);

  const loadStats = useCallback(async () => {
    try {
      const data = await api.fetchStats();
      setStats(data);
    } catch (err) {
      console.error('Error fetching stats:', err);
    }
  }, []);

  useEffect(() => {
    Promise.all([loadTasks(), loadStats()]).finally(() => setLoading(false));
  }, [loadTasks, loadStats]);

  const addTask = async (title, category, estPomodoros) => {
    try {
      await api.createTask(title, category, estPomodoros);
      await loadTasks();
    } catch (err) {
      console.error('Error adding task:', err);
    }
  };

  const toggleTaskCompleted = async (taskId, completed) => {
    try {
      await api.updateTask(taskId, { completed });
      await Promise.all([loadTasks(), loadStats()]);
    } catch (err) {
      console.error('Error toggling task:', err);
    }
  };

  const selectActiveTask = async (taskId) => {
    try {
      await api.updateTask(taskId, { is_active: true });
      await loadTasks();
    } catch (err) {
      console.error('Error selecting active task:', err);
    }
  };

  const removeTask = async (taskId) => {
    try {
      await api.deleteTask(taskId);
      await loadTasks();
    } catch (err) {
      console.error('Error removing task:', err);
    }
  };

  return (
    <TaskContext.Provider
      value={{
        tasks,
        stats,
        activeTask,
        loading,
        addTask,
        toggleTaskCompleted,
        selectActiveTask,
        removeTask,
        refreshTasksAndStats: () => Promise.all([loadTasks(), loadStats()])
      }}
    >
      {children}
    </TaskContext.Provider>
  );
}

export function useTasks() {
  return useContext(TaskContext);
}
