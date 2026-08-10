import React, { useState } from 'react';
import Header from './components/Header';
import TimerRing from './components/TimerRing';
import TimerControls from './components/TimerControls';
import ActiveTaskBadge from './components/ActiveTaskBadge';
import AmbientSoundBar from './components/AmbientSoundBar';
import TaskManager from './components/TaskManager';
import StatsGrid from './components/StatsGrid';
import SettingsModal from './components/SettingsModal';

export default function App() {
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);

  return (
    <div className="container">
      <Header onOpenSettings={() => setIsSettingsOpen(true)} />

      <main className="main-grid">
        {/* Left Column: Pomodoro Timer & Ambient Soundscape */}
        <section className="glass-card timer-container">
          <TimerRing />
          <TimerControls />
          <ActiveTaskBadge />
          <AmbientSoundBar />
        </section>

        {/* Right Column: Task Manager & Productivity Stats */}
        <section style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          <TaskManager />
          <StatsGrid />
        </section>
      </main>

      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
      />
    </div>
  );
}
