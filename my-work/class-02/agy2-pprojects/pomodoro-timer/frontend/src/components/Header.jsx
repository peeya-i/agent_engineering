import React from 'react';

export default function Header({ onOpenSettings }) {
  return (
    <header className="header">
      <div className="brand">
        <div className="brand-icon">
          <i className="fa-solid fa-spa"></i>
        </div>
        <div className="brand-title">
          Zen <span>Pomodoro</span>
        </div>
      </div>

      <div className="top-actions">
        <button
          className="icon-btn"
          title="Timer Settings & Themes"
          onClick={onOpenSettings}
        >
          <i className="fa-solid fa-sliders"></i>
        </button>
      </div>
    </header>
  );
}
