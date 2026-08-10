import React, { createContext, useContext, useState, useEffect, useRef, useCallback } from 'react';
import * as api from '../services/api';
import { zenAudio } from '../audio/zenAudio';
import { useTasks } from './TaskContext';

const TimerContext = createContext();

export function TimerProvider({ children }) {
  const { activeTask, refreshTasksAndStats } = useTasks();

  const [settings, setSettings] = useState({
    focus_duration: 25,
    short_break_duration: 5,
    long_break_duration: 15,
    long_break_interval: 4,
    auto_start_breaks: false,
    theme: 'serene-forest'
  });

  const [mode, setModeState] = useState('focus'); // 'focus' | 'shortBreak' | 'longBreak'
  const [remainingSeconds, setRemainingSeconds] = useState(25 * 60);
  const [totalSeconds, setTotalSeconds] = useState(25 * 60);
  const [isRunning, setIsRunning] = useState(false);
  const [completedCycles, setCompletedCycles] = useState(0);

  const timerRef = useRef(null);

  // Apply theme to document element
  const applyTheme = useCallback((themeName) => {
    document.body.setAttribute('data-theme', themeName || 'serene-forest');
  }, []);

  // Fetch initial settings from server
  useEffect(() => {
    api.fetchSettings().then(data => {
      if (data) {
        setSettings(data);
        applyTheme(data.theme);
        const focusSecs = (data.focus_duration || 25) * 60;
        setRemainingSeconds(focusSecs);
        setTotalSeconds(focusSecs);
      }
    }).catch(err => console.error("Error loading settings:", err));
  }, [applyTheme]);

  // Mode switching helper
  const switchMode = useCallback((newMode, currentSettings = settings) => {
    setIsRunning(false);
    if (timerRef.current) clearInterval(timerRef.current);

    setModeState(newMode);
    let mins = currentSettings.focus_duration || 25;
    if (newMode === 'shortBreak') mins = currentSettings.short_break_duration || 5;
    if (newMode === 'longBreak') mins = currentSettings.long_break_duration || 15;

    const secs = mins * 60;
    setRemainingSeconds(secs);
    setTotalSeconds(secs);
  }, [settings]);

  // Timer complete handler
  const handleTimerComplete = useCallback(async () => {
    setIsRunning(false);
    if (timerRef.current) clearInterval(timerRef.current);

    // Play Zen bowl chime
    zenAudio.playCompletionChime();

    // Record session to backend API
    try {
      const durationMins = Math.round(totalSeconds / 60);
      await api.recordSession(activeTask?.id || null, durationMins, mode);
      await refreshTasksAndStats();
    } catch (err) {
      console.error("Error recording session:", err);
    }

    // Determine next mode
    if (mode === 'focus') {
      const nextCycle = completedCycles + 1;
      setCompletedCycles(nextCycle);
      const nextMode = (nextCycle % (settings.long_break_interval || 4) === 0) ? 'longBreak' : 'shortBreak';
      switchMode(nextMode);
      if (settings.auto_start_breaks) {
        setIsRunning(true);
      }
    } else {
      switchMode('focus');
    }
  }, [mode, totalSeconds, activeTask, completedCycles, settings, switchMode, refreshTasksAndStats]);

  // Timer tick interval effect
  useEffect(() => {
    if (isRunning) {
      timerRef.current = setInterval(() => {
        setRemainingSeconds(prev => {
          if (prev <= 1) {
            handleTimerComplete();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    } else {
      if (timerRef.current) clearInterval(timerRef.current);
    }

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [isRunning, handleTimerComplete]);

  // Update document title with timer countdown
  useEffect(() => {
    const mins = Math.floor(remainingSeconds / 60);
    const secs = remainingSeconds % 60;
    const formatted = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    const icon = mode === 'focus' ? '🧘' : '☕';
    document.title = `${formatted} ${icon} Zen Pomodoro`;
  }, [remainingSeconds, mode]);

  const toggleTimer = () => {
    zenAudio.init(); // Initialize audio context on user interaction
    setIsRunning(prev => !prev);
  };

  const resetTimer = () => {
    setIsRunning(false);
    if (timerRef.current) clearInterval(timerRef.current);
    setRemainingSeconds(totalSeconds);
  };

  const skipTimer = () => {
    setIsRunning(false);
    if (timerRef.current) clearInterval(timerRef.current);

    if (mode === 'focus') {
      const nextCycle = completedCycles + 1;
      setCompletedCycles(nextCycle);
      const nextMode = (nextCycle % (settings.long_break_interval || 4) === 0) ? 'longBreak' : 'shortBreak';
      switchMode(nextMode);
    } else {
      switchMode('focus');
    }
  };

  const saveSettings = async (newSettings) => {
    try {
      const updated = await api.updateSettings(newSettings);
      setSettings(updated);
      applyTheme(updated.theme);
      switchMode(mode, updated);
    } catch (err) {
      console.error("Error saving settings:", err);
    }
  };

  return (
    <TimerContext.Provider
      value={{
        mode,
        remainingSeconds,
        totalSeconds,
        isRunning,
        settings,
        switchMode,
        toggleTimer,
        resetTimer,
        skipTimer,
        saveSettings,
        applyTheme
      }}
    >
      {children}
    </TimerContext.Provider>
  );
}

export function useTimer() {
  return useContext(TimerContext);
}
