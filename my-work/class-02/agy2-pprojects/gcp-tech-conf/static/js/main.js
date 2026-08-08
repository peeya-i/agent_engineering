/**
 * CloudCon 2026 - Interactive Schedule & Search Controller
 */

document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const searchInput = document.getElementById('searchInput');
  const categorySelect = document.getElementById('categorySelect');
  const speakerSelect = document.getElementById('speakerSelect');
  const categoryPills = document.querySelectorAll('.pill-btn');
  const viewBtns = document.querySelectorAll('.view-btn');
  const scheduleContainer = document.getElementById('scheduleContainer');
  const sessionCountEl = document.getElementById('sessionCount');
  const resetFiltersBtn = document.getElementById('resetFiltersBtn');
  
  // Modal Elements
  const modalOverlay = document.getElementById('talkModal');
  const modalCloseBtn = document.getElementById('modalClose');
  const modalTitle = document.getElementById('modalTitle');
  const modalTime = document.getElementById('modalTime');
  const modalRoom = document.getElementById('modalRoom');
  const modalBadge = document.getElementById('modalBadge');
  const modalDesc = document.getElementById('modalDesc');
  const modalSpeakers = document.getElementById('modalSpeakers');

  let currentCategory = 'all';
  let currentSpeaker = 'all';
  let searchQuery = '';

  // Initialize Event Listeners
  if (searchInput) {
    searchInput.addEventListener('input', debounce((e) => {
      searchQuery = e.target.value.toLowerCase().trim();
      applyFilters();
    }, 200));
  }

  if (categorySelect) {
    categorySelect.addEventListener('change', (e) => {
      currentCategory = e.target.value;
      updatePillsUI(currentCategory);
      applyFilters();
    });
  }

  if (speakerSelect) {
    speakerSelect.addEventListener('change', (e) => {
      currentSpeaker = e.target.value;
      applyFilters();
    });
  }

  // Pill click handlers
  categoryPills.forEach(pill => {
    pill.addEventListener('click', () => {
      const cat = pill.getAttribute('data-category');
      currentCategory = cat;
      if (categorySelect) categorySelect.value = cat;
      updatePillsUI(cat);
      applyFilters();
    });
  });

  // View Mode Switcher (Timeline vs Grid)
  viewBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      viewBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const viewMode = btn.getAttribute('data-view');
      
      if (viewMode === 'grid') {
        scheduleContainer.classList.remove('timeline-view');
        scheduleContainer.classList.add('grid-view');
      } else {
        scheduleContainer.classList.remove('grid-view');
        scheduleContainer.classList.add('timeline-view');
      }
    });
  });

  if (resetFiltersBtn) {
    resetFiltersBtn.addEventListener('click', () => {
      searchQuery = '';
      currentCategory = 'all';
      currentSpeaker = 'all';
      if (searchInput) searchInput.value = '';
      if (categorySelect) categorySelect.value = 'all';
      if (speakerSelect) speakerSelect.value = 'all';
      updatePillsUI('all');
      applyFilters();
    });
  }

  // Talk Detail Modal Click Handler
  document.addEventListener('click', (e) => {
    const talkCard = e.target.closest('.talk-card');
    const isLinkedin = e.target.closest('.linkedin-icon-link') || e.target.closest('.linkedin-btn');
    
    // Open modal if clicked inside talk card but not directly on LinkedIn link
    if (talkCard && !isLinkedin) {
      const talkId = talkCard.getAttribute('data-talk-id');
      if (talkId) {
        openTalkModal(talkId);
      }
    }
  });

  if (modalCloseBtn) {
    modalCloseBtn.addEventListener('click', closeModal);
  }

  if (modalOverlay) {
    modalOverlay.addEventListener('click', (e) => {
      if (e.target === modalOverlay) closeModal();
    });
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeModal();
  });

  // Function to update pill button state
  function updatePillsUI(selectedCategory) {
    categoryPills.forEach(p => {
      if (p.getAttribute('data-category') === selectedCategory) {
        p.classList.add('active');
      } else {
        p.classList.remove('active');
      }
    });
  }

  // Filter application logic
  function applyFilters() {
    const talkCards = document.querySelectorAll('.talk-card');
    let visibleCount = 0;

    talkCards.forEach(card => {
      const title = (card.getAttribute('data-title') || '').toLowerCase();
      const category = (card.getAttribute('data-category-id') || '').toLowerCase();
      const categoryName = (card.getAttribute('data-category-name') || '').toLowerCase();
      const description = (card.getAttribute('data-desc') || '').toLowerCase();
      const speakersText = (card.getAttribute('data-speakers') || '').toLowerCase();
      const roomText = (card.getAttribute('data-room') || '').toLowerCase();

      // Check Category match
      let matchCat = (currentCategory === 'all') || (category === currentCategory) || (categoryName.includes(currentCategory));

      // Check Speaker match
      let matchSpeaker = (currentSpeaker === 'all') || (speakersText.includes(currentSpeaker.toLowerCase()));

      // Check Search query match
      let matchQuery = !searchQuery || (
        title.includes(searchQuery) ||
        description.includes(searchQuery) ||
        speakersText.includes(searchQuery) ||
        categoryName.includes(searchQuery) ||
        roomText.includes(searchQuery)
      );

      if (matchCat && matchSpeaker && matchQuery) {
        card.style.display = 'grid';
        visibleCount++;
      } else {
        card.style.display = 'none';
      }
    });

    if (sessionCountEl) {
      sessionCountEl.textContent = `Showing ${visibleCount} of ${talkCards.length} technical talks`;
    }

    // Toggle empty state notice if no results
    let noResultsEl = document.getElementById('noResultsNotice');
    if (visibleCount === 0) {
      if (!noResultsEl) {
        noResultsEl = document.createElement('div');
        noResultsEl.id = 'noResultsNotice';
        noResultsEl.className = 'meta-card';
        noResultsEl.style.justifyContent = 'center';
        noResultsEl.style.padding = '40px';
        noResultsEl.style.textAlign = 'center';
        noResultsEl.innerHTML = `
          <div>
            <h3 style="margin-bottom:8px;">🔍 No talks match your filter criteria</h3>
            <p style="color:var(--text-muted); margin-bottom:16px;">Try adjusting your keywords, speaker, or category selections.</p>
            <button id="clearFiltersInlineBtn" class="pill-btn active">Reset All Filters</button>
          </div>
        `;
        scheduleContainer.appendChild(noResultsEl);
        document.getElementById('clearFiltersInlineBtn').addEventListener('click', () => {
          if (resetFiltersBtn) resetFiltersBtn.click();
        });
      }
      noResultsEl.style.display = 'flex';
    } else if (noResultsEl) {
      noResultsEl.style.display = 'none';
    }
  }

  // Open modal with talk details
  function openTalkModal(talkId) {
    fetch(`/api/talk/${talkId}`)
      .then(res => res.json())
      .then(talk => {
        if (talk.error) return;

        modalTitle.textContent = talk.title;
        modalTime.textContent = `🕒 ${talk.time}`;
        modalRoom.textContent = `📍 ${talk.room}`;
        modalBadge.textContent = talk.category;
        modalBadge.className = `badge badge-${talk.category_id}`;
        modalDesc.textContent = talk.description;

        // Render Speakers
        modalSpeakers.innerHTML = talk.speakers.map(sp => `
          <div class="speaker-card" style="padding:16px; margin-bottom:12px; text-align:left; display:flex; align-items:center; gap:16px;">
            <div class="speaker-card-avatar" style="margin:0; width:50px; height:50px; font-size:1.1rem;">
              ${sp.avatar_initials}
            </div>
            <div style="flex:1;">
              <div style="font-weight:700; color:var(--text-main); font-size:1.05rem;">${sp.first_name} ${sp.last_name}</div>
              <div style="font-size:0.85rem; color:var(--gcp-cyan);">${sp.role} • ${sp.company}</div>
              <p style="font-size:0.8rem; color:var(--text-muted); margin-top:4px;">${sp.bio}</p>
            </div>
            <a href="${sp.linkedin_url}" target="_blank" rel="noopener noreferrer" class="linkedin-btn" style="padding:6px 12px; font-size:0.8rem;">
              LinkedIn ↗
            </a>
          </div>
        `).join('');

        modalOverlay.classList.add('open');
        document.body.style.overflow = 'hidden';
      })
      .catch(err => console.error("Error fetching talk details:", err));
  }

  function closeModal() {
    if (modalOverlay) modalOverlay.classList.remove('open');
    document.body.style.overflow = '';
  }

  // Utility Debounce
  function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }
});
