import React, { useState } from 'react';
import { zenAudio } from '../audio/zenAudio';

export default function AmbientSoundBar() {
  const [activeSound, setActiveSound] = useState(null);

  const handleToggle = (type) => {
    const isPlaying = zenAudio.toggleAmbience(type);
    setActiveSound(isPlaying ? type : null);
  };

  return (
    <div className="ambient-bar">
      <button
        className={`ambient-btn ${activeSound === 'rain' ? 'active' : ''}`}
        onClick={() => handleToggle('rain')}
      >
        <i className="fa-solid fa-cloud-rain"></i> Gentle Rain
      </button>

      <button
        className={`ambient-btn ${activeSound === 'wind' ? 'active' : ''}`}
        onClick={() => handleToggle('wind')}
      >
        <i className="fa-solid fa-wind"></i> Soft Wind
      </button>

      <button
        className={`ambient-btn ${activeSound === 'ocean' ? 'active' : ''}`}
        onClick={() => handleToggle('ocean')}
      >
        <i className="fa-solid fa-water"></i> Ocean Waves
      </button>

      <button
        className={`ambient-btn ${activeSound === 'binaural' ? 'active' : ''}`}
        onClick={() => handleToggle('binaural')}
      >
        <i className="fa-solid fa-brain"></i> Alpha Beats
      </button>
    </div>
  );
}
