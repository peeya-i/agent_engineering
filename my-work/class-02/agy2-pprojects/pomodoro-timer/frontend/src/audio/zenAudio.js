/**
 * Zen Audio Engine — Procedural Web Audio API Soundscapes & Chimes
 * Generates Rain, Wind, Ocean, and Zen Bowl Chimes dynamically without external file dependencies.
 */

class ZenAudioEngine {
  constructor() {
    this.ctx = null;
    this.activeAmbience = null;
    this.ambientType = null;
    this.gainNode = null;
    this.volume = 0.5;
  }

  init() {
    if (!this.ctx) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      this.ctx = new AudioCtx();
    }
    if (this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  setVolume(vol) {
    this.volume = Math.max(0, Math.min(1, vol));
    if (this.gainNode && this.ctx) {
      this.gainNode.gain.setValueAtTime(this.volume * 0.3, this.ctx.currentTime);
    }
  }

  toggleAmbience(type) {
    this.init();

    if (this.ambientType === type) {
      this.stopAmbience();
      return false; // Stopped
    }

    this.stopAmbience();
    this.ambientType = type;

    this.gainNode = this.ctx.createGain();
    this.gainNode.gain.setValueAtTime(this.volume * 0.25, this.ctx.currentTime);
    this.gainNode.connect(this.ctx.destination);

    if (type === 'rain') {
      this.createRainSound();
    } else if (type === 'wind') {
      this.createWindSound();
    } else if (type === 'ocean') {
      this.createOceanWaves();
    } else if (type === 'binaural') {
      this.createBinauralBeats();
    }

    return true; // Playing
  }

  stopAmbience() {
    if (this.activeAmbience) {
      try {
        if (Array.isArray(this.activeAmbience)) {
          this.activeAmbience.forEach(node => {
            if (node.stop) node.stop();
            if (node.disconnect) node.disconnect();
          });
        } else if (this.activeAmbience.stop) {
          this.activeAmbience.stop();
        }
      } catch (e) {
        console.warn("Audio node cleanup:", e);
      }
    }
    this.activeAmbience = null;
    this.ambientType = null;
  }

  // --- Rain Generator (Filtered White Noise) ---
  createRainSound() {
    const bufferSize = 2 * this.ctx.sampleRate;
    const noiseBuffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const output = noiseBuffer.getChannelData(0);
    
    for (let i = 0; i < bufferSize; i++) {
      output[i] = Math.random() * 2 - 1;
    }

    const whiteNoise = this.ctx.createBufferSource();
    whiteNoise.buffer = noiseBuffer;
    whiteNoise.loop = true;

    const filter = this.ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(1000, this.ctx.currentTime);

    whiteNoise.connect(filter);
    filter.connect(this.gainNode);
    whiteNoise.start();

    this.activeAmbience = [whiteNoise, filter];
  }

  // --- Gentle Wind Generator ---
  createWindSound() {
    const bufferSize = 2 * this.ctx.sampleRate;
    const noiseBuffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const output = noiseBuffer.getChannelData(0);
    
    for (let i = 0; i < bufferSize; i++) {
      output[i] = Math.random() * 2 - 1;
    }

    const noise = this.ctx.createBufferSource();
    noise.buffer = noiseBuffer;
    noise.loop = true;

    const filter = this.ctx.createBiquadFilter();
    filter.type = 'bandpass';
    filter.frequency.setValueAtTime(400, this.ctx.currentTime);
    filter.Q.setValueAtTime(3.0, this.ctx.currentTime);

    // LFO to modulate wind frequency
    const lfo = this.ctx.createOscillator();
    lfo.frequency.setValueAtTime(0.2, this.ctx.currentTime);
    
    const lfoGain = this.ctx.createGain();
    lfoGain.gain.setValueAtTime(200, this.ctx.currentTime);

    lfo.connect(lfoGain);
    lfoGain.connect(filter.frequency);

    noise.connect(filter);
    filter.connect(this.gainNode);

    lfo.start();
    noise.start();

    this.activeAmbience = [noise, filter, lfo, lfoGain];
  }

  // --- Ocean Waves Generator ---
  createOceanWaves() {
    const bufferSize = 2 * this.ctx.sampleRate;
    const noiseBuffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const output = noiseBuffer.getChannelData(0);
    
    for (let i = 0; i < bufferSize; i++) {
      output[i] = Math.random() * 2 - 1;
    }

    const noise = this.ctx.createBufferSource();
    noise.buffer = noiseBuffer;
    noise.loop = true;

    const filter = this.ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(300, this.ctx.currentTime);

    // Slow wave swell gain modulation
    const swellGain = this.ctx.createGain();
    const lfo = this.ctx.createOscillator();
    lfo.frequency.setValueAtTime(0.1, this.ctx.currentTime); // 10s wave cycle

    const lfoGain = this.ctx.createGain();
    lfoGain.gain.setValueAtTime(0.15, this.ctx.currentTime);

    lfo.connect(lfoGain);
    lfoGain.connect(swellGain.gain);

    noise.connect(filter);
    filter.connect(swellGain);
    swellGain.connect(this.gainNode);

    lfo.start();
    noise.start();

    this.activeAmbience = [noise, filter, swellGain, lfo, lfoGain];
  }

  // --- Binaural Beta Focus Beats (Alpha 10Hz difference) ---
  createBinauralBeats() {
    const oscLeft = this.ctx.createOscillator();
    const oscRight = this.ctx.createOscillator();
    const merger = this.ctx.createChannelMerger(2);

    oscLeft.frequency.setValueAtTime(200, this.ctx.currentTime);
    oscRight.frequency.setValueAtTime(210, this.ctx.currentTime); // 10Hz difference

    oscLeft.connect(merger, 0, 0);
    oscRight.connect(merger, 0, 1);
    merger.connect(this.gainNode);

    oscLeft.start();
    oscRight.start();

    this.activeAmbience = [oscLeft, oscRight, merger];
  }

  // --- Soothing Zen Bowl Completion Chime ---
  playCompletionChime() {
    this.init();

    const now = this.ctx.currentTime;
    const osc1 = this.ctx.createOscillator();
    const osc2 = this.ctx.createOscillator();
    const gain = this.ctx.createGain();

    osc1.type = 'sine';
    osc1.frequency.setValueAtTime(432, now); // A = 432 Hz Zen tuning

    osc2.type = 'sine';
    osc2.frequency.setValueAtTime(864, now); // Harmonic overtone

    gain.gain.setValueAtTime(0, now);
    gain.gain.linearRampToValueAtTime(0.4, now + 0.1);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 4.5); // 4.5s soft decay

    osc1.connect(gain);
    osc2.connect(gain);
    gain.connect(this.ctx.destination);

    osc1.start(now);
    osc2.start(now);

    osc1.stop(now + 4.5);
    osc2.stop(now + 4.5);
  }
}

export const zenAudio = new ZenAudioEngine();
