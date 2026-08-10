import React, { useState, useEffect } from 'react';
import { useTimer } from '../context/TimerContext';

export default function SettingsModal({ isOpen, onClose }) {
  const { settings, saveSettings, applyTheme } = useTimer();

  const [focusMins, setFocusMins] = useState(25);
  const [shortBreakMins, setShortBreakMins] = useState(5);
  const [longBreakMins, setLongBreakMins] = useState(15);
  const [selectedTheme, setSelectedTheme] = useState('serene-forest');

  useEffect(() => {
    if (settings) {
      setFocusMins(settings.focus_duration || 25);
      setShortBreakMins(settings.short_break_duration || 5);
      setLongBreakMins(settings.long_break_duration || 15);
      setSelectedTheme(settings.theme || 'serene-forest');
    }
  }, [settings, isOpen]);

  if (!isOpen) return null;

  const handleThemeSelect = (themeName) => {
    setSelectedTheme(themeName);
    applyTheme(themeName);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    saveSettings({
      focus_duration: parseInt(focusMins),
      short_break_duration: parseInt(shortBreakMins),
      long_break_duration: parseInt(longBreakMins),
      theme: selectedTheme
    });
    onClose();
  };

  return (
    <div className="modal-overlay open">
      <div className="modal-box">
        <button className="modal-close" onClick={onClose}>
          <i className="fa-solid fa-xmark"></i>
        </button>

        <h2 style={{ fontSize: '1.3rem', fontWeight: 700, marginBottom: '20px' }}>
          <i className="fa-solid fa-sliders" style={{ color: 'var(--accent-primary)', marginRight: '8px' }}></i>
          App Settings & Themes
        </h2>

        <form onSubmit={handleSubmit}>
          {/* Timer Durations */}
          <div className="setting-group">
            <label className="setting-label">Timer Durations (Minutes)</label>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '10px' }}>
              <div>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Focus</span>
                <input
                  type="number"
                  className="task-input"
                  min="1"
                  max="120"
                  value={focusMins}
                  onChange={(e) => setFocusMins(e.target.value)}
                />
              </div>
              <div>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Short Break</span>
                <input
                  type="number"
                  className="task-input"
                  min="1"
                  max="30"
                  value={shortBreakMins}
                  onChange={(e) => setShortBreakMins(e.target.value)}
                />
              </div>
              <div>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Long Break</span>
                <input
                  type="number"
                  className="task-input"
                  min="1"
                  max="60"
                  value={longBreakMins}
                  onChange={(e) => setLongBreakMins(e.target.value)}
                />
              </div>
            </div>
          </div>

          {/* Theme Palette Chooser */}
          <div className="setting-group">
            <label className="setting-label">Aesthetic Color Themes</label>
            <div className="theme-grid">
              <div
                className={`theme-option ${selectedTheme === 'serene-forest' ? 'active' : ''}`}
                onClick={() => handleThemeSelect('serene-forest')}
              >
                <span style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#5EEAD4' }}></span>
                Serene Forest
              </div>

              <div
                className={`theme-option ${selectedTheme === 'nordic-fog' ? 'active' : ''}`}
                onClick={() => handleThemeSelect('nordic-fog')}
              >
                <span style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#38BDF8' }}></span>
                Nordic Fog
              </div>

              <div
                className={`theme-option ${selectedTheme === 'sunset-calm' ? 'active' : ''}`}
                onClick={() => handleThemeSelect('sunset-calm')}
              >
                <span style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#F472B6' }}></span>
                Sunset Calm
              </div>

              <div
                className={`theme-option ${selectedTheme === 'cherry-blossom' ? 'active' : ''}`}
                onClick={() => handleThemeSelect('cherry-blossom')}
              >
                <span style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#FB7185' }}></span>
                Cherry Blossom
              </div>

              <div
                className={`theme-option ${selectedTheme === 'midnight-obsidian' ? 'active' : ''}`}
                style={{ gridColumn: 'span 2' }}
                onClick={() => handleThemeSelect('midnight-obsidian')}
              >
                <span style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#A855F7' }}></span>
                Midnight Obsidian
              </div>
            </div>
          </div>

          <button
            type="submit"
            className="add-task-btn"
            style={{ width: '100%', padding: '12px', marginTop: '10px', borderRadius: 'var(--radius-md)' }}
          >
            Save Preferences
          </button>
        </form>
      </div>
    </div>
  );
}
