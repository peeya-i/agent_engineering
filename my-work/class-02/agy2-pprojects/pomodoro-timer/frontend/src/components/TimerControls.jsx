import React from 'react';
import { useTimer } from '../context/TimerContext';

export default function TimerControls() {
  const { isRunning, toggleTimer, resetTimer, skipTimer } = useTimer();

  return (
    <div className="timer-controls">
      <button
        className="control-btn control-btn-secondary"
        title="Reset Timer"
        onClick={resetTimer}
      >
        <i className="fa-solid fa-rotate-left"></i>
      </button>

      <button
        className="control-btn control-btn-main"
        title={isRunning ? "Pause Session" : "Start Focus Session"}
        onClick={toggleTimer}
      >
        <i className={`fa-solid ${isRunning ? 'fa-pause' : 'fa-play'}`}></i>
      </button>

      <button
        className="control-btn control-btn-secondary"
        title="Skip Session"
        onClick={skipTimer}
      >
        <i className="fa-solid fa-forward-step"></i>
      </button>
    </div>
  );
}
