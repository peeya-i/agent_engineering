import React from 'react';
import { useTimer } from '../context/TimerContext';

const CIRCLE_RADIUS = 130;
const CIRCLE_PERIMETER = 2 * Math.PI * CIRCLE_RADIUS; // ~816

export default function TimerRing() {
  const { mode, remainingSeconds, totalSeconds, switchMode } = useTimer();

  const mins = Math.floor(remainingSeconds / 60);
  const secs = remainingSeconds % 60;
  const formattedDigits = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;

  const progressFraction = totalSeconds > 0 ? remainingSeconds / totalSeconds : 1;
  const strokeOffset = CIRCLE_PERIMETER * (1 - progressFraction);

  const getLabel = () => {
    if (mode === 'shortBreak') return 'Short Break';
    if (mode === 'longBreak') return 'Long Break';
    return 'Focus Session';
  };

  return (
    <>
      {/* Session Mode Selector Pills */}
      <div className="mode-pills">
        <button
          className={`mode-btn ${mode === 'focus' ? 'active' : ''}`}
          onClick={() => switchMode('focus')}
        >
          🧘 Focus
        </button>
        <button
          className={`mode-btn ${mode === 'shortBreak' ? 'active' : ''}`}
          onClick={() => switchMode('shortBreak')}
        >
          ☕ Short Break
        </button>
        <button
          className={`mode-btn ${mode === 'longBreak' ? 'active' : ''}`}
          onClick={() => switchMode('longBreak')}
        >
          🌿 Long Break
        </button>
      </div>

      {/* SVG Circular Timer Display */}
      <div className="timer-display-wrapper">
        <svg className="progress-ring" width="280" height="280">
          <circle className="progress-ring-circle-bg" cx="140" cy="140" r={CIRCLE_RADIUS}></circle>
          <circle
            className="progress-ring-circle"
            cx="140"
            cy="140"
            r={CIRCLE_RADIUS}
            style={{
              strokeDasharray: `${CIRCLE_PERIMETER} ${CIRCLE_PERIMETER}`,
              strokeDashoffset: `${strokeOffset}`
            }}
          ></circle>
        </svg>

        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', zIndex: 2 }}>
          <div className="timer-digits">{formattedDigits}</div>
          <div className="timer-state-label">{getLabel()}</div>
        </div>
      </div>
    </>
  );
}
