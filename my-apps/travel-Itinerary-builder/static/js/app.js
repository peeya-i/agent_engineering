/**
 * Travel Itinerary Builder - Frontend Orchestration & UI Controller
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const form = document.getElementById('itineraryForm');
    const originInput = document.getElementById('originInput');
    const destinationInput = document.getElementById('destinationInput');
    const departureDateInput = document.getElementById('departureDateInput');
    const budgetInput = document.getElementById('budgetInput');
    const daysInput = document.getElementById('daysInput');
    const customInterestInput = document.getElementById('customInterestInput');
    const addInterestBtn = document.getElementById('addInterestBtn');
    const interestTagsContainer = document.getElementById('interestTags');
    const interestsListText = document.getElementById('interestsListText');
    const submitBtn = document.getElementById('submitBtn');

    // Errors
    const originError = document.getElementById('originError');
    const destinationError = document.getElementById('destinationError');
    const departureDateError = document.getElementById('departureDateError');
    const budgetError = document.getElementById('budgetError');
    const daysError = document.getElementById('daysError');

    // Architecture Indicators
    const phaseFlight = document.getElementById('phaseFlight');
    const flightStatus = document.getElementById('flightStatus');
    const discoveryStatus = document.getElementById('discoveryStatus');
    const loopStatus = document.getElementById('loopStatus');
    const agentFlight = document.getElementById('agentFlight');
    const agentHotel = document.getElementById('agentHotel');
    const agentActivity = document.getElementById('agentActivity');
    const agentScheduler = document.getElementById('agentScheduler');
    const agentBudget = document.getElementById('agentBudget');
    const phaseDiscovery = document.getElementById('phaseDiscovery');
    const phaseLoop = document.getElementById('phaseLoop');
    const logsTerminal = document.getElementById('logsTerminal');

    // Results Elements
    const resultsSection = document.getElementById('resultsSection');
    const resDestination = document.getElementById('resDestination');
    const resTripTitle = document.getElementById('resTripTitle');
    const resTotalCost = document.getElementById('resTotalCost');
    const resBudget = document.getElementById('resBudget');
    const resVariance = document.getElementById('resVariance');
    const resApprovalBadge = document.getElementById('resApprovalBadge');
    const resFeedbackText = document.getElementById('resFeedbackText');
    const scheduleContainer = document.getElementById('scheduleContainer');
    const flightsList = document.getElementById('flightsList');
    const hotelsList = document.getElementById('hotelsList');
    const activitiesList = document.getElementById('activitiesList');
    const budgetTable = document.getElementById('budgetTable');
    const copyJsonBtn = document.getElementById('copyJsonBtn');

    let currentJsonState = null;

    // --------------------------------------------------------------------------
    // Interest Tags Management
    // --------------------------------------------------------------------------
    function getSelectedInterests() {
        const activeChips = interestTagsContainer.querySelectorAll('.tag-chip.active');
        return Array.from(activeChips).map(chip => chip.getAttribute('data-tag'));
    }

    function updateInterestsPreview() {
        const selected = getSelectedInterests();
        interestsListText.textContent = selected.length > 0 ? selected.join(', ') : 'None selected (defaults will apply)';
    }

    interestTagsContainer.addEventListener('click', (e) => {
        if (e.target.classList.contains('tag-chip')) {
            e.target.classList.toggle('active');
            updateInterestsPreview();
        }
    });

    function addCustomInterest() {
        const val = customInterestInput.value.trim();
        if (val) {
            // Check duplicate
            const existing = Array.from(interestTagsContainer.querySelectorAll('.tag-chip'))
                .find(c => c.getAttribute('data-tag').toLowerCase() === val.toLowerCase());
            
            if (!existing) {
                const newChip = document.createElement('button');
                newChip.type = 'button';
                newChip.className = 'tag-chip active';
                newChip.setAttribute('data-tag', val);
                newChip.textContent = val;
                interestTagsContainer.appendChild(newChip);
            } else {
                existing.classList.add('active');
            }
            customInterestInput.value = '';
            updateInterestsPreview();
        }
    }

    addInterestBtn.addEventListener('click', addCustomInterest);
    customInterestInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            addCustomInterest();
        }
    });

    // --------------------------------------------------------------------------
    // Logging Terminal
    // --------------------------------------------------------------------------
    function addLog(message, isHighlight = false) {
        const line = document.createElement('div');
        line.className = `log-line ${isHighlight ? 'highlight' : ''}`;
        const time = new Date().toLocaleTimeString();
        line.textContent = `[${time}] ${message}`;
        logsTerminal.appendChild(line);
        logsTerminal.scrollTop = logsTerminal.scrollHeight;
    }

    function clearLogs() {
        logsTerminal.innerHTML = '';
    }

    // --------------------------------------------------------------------------
    // Form Validation
    // --------------------------------------------------------------------------
    function clearErrors() {
        if (destinationError) { destinationError.style.display = 'none'; destinationError.textContent = ''; }
        if (budgetError) { budgetError.style.display = 'none'; budgetError.textContent = ''; }
        if (daysError) { daysError.style.display = 'none'; daysError.textContent = ''; }
    }

    function validateForm() {
        clearErrors();
        let isValid = true;

        const dest = destinationInput.value.trim();
        const budget = parseFloat(budgetInput.value);
        const days = parseInt(daysInput.value, 10);

        if (!dest) {
            destinationError.textContent = 'Please provide a destination (e.g. Kyoto, Japan).';
            destinationError.style.display = 'block';
            isValid = false;
        }

        if (isNaN(budget) || budget <= 0) {
            budgetError.textContent = 'Please enter a valid budget greater than $0.';
            budgetError.style.display = 'block';
            isValid = false;
        }

        if (isNaN(days) || days < 1 || days > 30) {
            daysError.textContent = 'Please enter trip duration between 1 and 30 days.';
            daysError.style.display = 'block';
            isValid = false;
        }

        return isValid;
    }

    // --------------------------------------------------------------------------
    // UI Animation for Pipeline Execution
    // --------------------------------------------------------------------------
    function setPipelineRunning(isRunning) {
        if (isRunning) {
            submitBtn.disabled = true;
            submitBtn.querySelector('.btn-text').style.display = 'none';
            submitBtn.querySelector('.btn-loader').style.display = 'inline-flex';

            // Reset visual states
            if (phaseFlight) phaseFlight.classList.add('active');
            if (phaseDiscovery) phaseDiscovery.classList.remove('active');
            if (phaseLoop) phaseLoop.classList.remove('active');

            if (flightStatus) { flightStatus.textContent = 'Running'; flightStatus.className = 'phase-status running'; }
            if (discoveryStatus) { discoveryStatus.textContent = 'Waiting'; discoveryStatus.className = 'phase-status'; }
            if (loopStatus) { loopStatus.textContent = 'Waiting'; loopStatus.className = 'phase-status'; }

            if (agentFlight) agentFlight.classList.add('active');
            if (agentHotel) agentHotel.classList.remove('active');
            if (agentActivity) agentActivity.classList.remove('active');
            if (agentScheduler) agentScheduler.classList.remove('active');
            if (agentBudget) agentBudget.classList.remove('active');
        } else {
            submitBtn.disabled = false;
            submitBtn.querySelector('.btn-text').style.display = 'inline-flex';
            submitBtn.querySelector('.btn-loader').style.display = 'none';

            if (flightStatus) { flightStatus.textContent = 'Completed'; flightStatus.className = 'phase-status done'; }
            if (discoveryStatus) { discoveryStatus.textContent = 'Completed'; discoveryStatus.className = 'phase-status done'; }
            if (loopStatus) { loopStatus.textContent = 'Completed'; loopStatus.className = 'phase-status done'; }

            if (agentFlight) agentFlight.classList.remove('active');
            if (agentHotel) agentHotel.classList.remove('active');
            if (agentActivity) agentActivity.classList.remove('active');
            if (agentScheduler) agentScheduler.classList.remove('active');
            if (agentBudget) agentBudget.classList.remove('active');

            if (phaseFlight) phaseFlight.classList.remove('active');
            if (phaseDiscovery) phaseDiscovery.classList.remove('active');
            if (phaseLoop) phaseLoop.classList.remove('active');
        }
    }

    // --------------------------------------------------------------------------
    // Form Submission & API Invocation
    // --------------------------------------------------------------------------
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (!validateForm()) {
            addLog('Validation failed: Missing required fields.');
            return;
        }

        const payload = {
            city_of_origin: originInput ? originInput.value.trim() : '',
            destination: destinationInput.value.trim(),
            departure_date: departureDateInput ? departureDateInput.value : '',
            budget: parseFloat(budgetInput.value),
            days: parseInt(daysInput.value, 10),
            interests: getSelectedInterests()
        };

        clearLogs();
        const originTxt = payload.city_of_origin ? ` from ${payload.city_of_origin}` : '';
        addLog(`Initiating trip pipeline for ${payload.destination}${originTxt} (${payload.days} days, budget: $${payload.budget.toFixed(2)})`);
        setPipelineRunning(true);

        try {
            // Stage 1: Flight Researcher
            setTimeout(() => {
                addLog('Phase 1: FlightResearcher locating transit options and schedules...');
            }, 400);

            // Stage 2: Parallel Discovery Team
            setTimeout(() => {
                if (phaseFlight) phaseFlight.classList.remove('active');
                if (flightStatus) { flightStatus.textContent = 'Done'; flightStatus.className = 'phase-status done'; }
                if (phaseDiscovery) phaseDiscovery.classList.add('active');
                if (discoveryStatus) { discoveryStatus.textContent = 'Running'; discoveryStatus.className = 'phase-status running'; }
                if (agentHotel) agentHotel.classList.add('active');
                if (agentActivity) agentActivity.classList.add('active');
                addLog('Phase 2: Parallel Discovery Team researching lodging and attractions concurrently...');
            }, 1200);

            // Stage 3: Optimization Room
            setTimeout(() => {
                if (phaseDiscovery) phaseDiscovery.classList.remove('active');
                if (discoveryStatus) { discoveryStatus.textContent = 'Done'; discoveryStatus.className = 'phase-status done'; }
                if (phaseLoop) phaseLoop.classList.add('active');
                if (loopStatus) { loopStatus.textContent = 'Running'; loopStatus.className = 'phase-status running'; }
                if (agentScheduler) agentScheduler.classList.add('active');
                if (agentBudget) agentBudget.classList.add('active');
                addLog('Phase 3: Optimization Room (Scheduler & BudgetEnforcer) synthesizing and refining schedule...');
            }, 2200);

            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const result = await response.json();

            if (!response.ok || !result.success) {
                const errorMsg = result.error || 'Failed to generate itinerary.';
                addLog(`Error: ${errorMsg}`);
                alert(`Error: ${errorMsg}`);
                setPipelineRunning(false);
                return;
            }

            // Success: render pipeline results
            currentJsonState = result.data;
            if (result.data.logs) {
                result.data.logs.forEach(msg => addLog(msg));
            }
            addLog('Itinerary generation complete! Rendering schedule and metrics.', true);

            renderResults(result.data);
            setPipelineRunning(false);

            // Smooth scroll to results
            resultsSection.scrollIntoView({ behavior: 'smooth' });

        } catch (err) {
            console.error('Request failed:', err);
            addLog(`Network or execution error: ${err.message}`);
            alert(`An unexpected error occurred: ${err.message}`);
            setPipelineRunning(false);
        }
    });

    // --------------------------------------------------------------------------
    // Results Rendering
    // --------------------------------------------------------------------------
    function renderResults(state) {
        const userInput = state.user_input || {};
        const research = state.raw_research || {};
        const itinerary = state.current_itinerary || {};
        const schedule = itinerary.schedule || [];
        const totalCost = itinerary.total_estimated_cost || 0.0;
        const budget = userInput.budget || 0.0;
        const isApproved = state.budget_approved;
        const feedback = state.critic_feedback || 'Itinerary optimized.';

        // Header Metrics
        resDestination.textContent = userInput.destination;
        resTripTitle.textContent = `${userInput.days}-Day Vacation Plan`;
        resTotalCost.textContent = `$${totalCost.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        resBudget.textContent = `$${budget.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

        const variance = budget - totalCost;
        if (variance >= 0) {
            resVariance.textContent = `+$${variance.toFixed(2)} (Under Budget)`;
            resVariance.style.color = 'var(--accent-emerald)';
        } else {
            resVariance.textContent = `-$${Math.abs(variance).toFixed(2)} (Over Budget)`;
            resVariance.style.color = 'var(--accent-rose)';
        }

        if (isApproved) {
            resApprovalBadge.textContent = 'Approved';
            resApprovalBadge.className = 'metric-badge approved';
        } else {
            resApprovalBadge.textContent = 'Exceeds Budget';
            resApprovalBadge.className = 'metric-badge over-budget';
        }

        resFeedbackText.textContent = feedback;

        // 1. Render Daily Schedule
        scheduleContainer.innerHTML = '';

        // Normalize schedule if needed
        let normalizedSchedule = [];
        if (Array.isArray(schedule) && schedule.length > 0) {
            const hasNestedEvents = schedule.every(item => item && Array.isArray(item.events));
            if (hasNestedEvents) {
                normalizedSchedule = schedule;
            } else {
                // Flat list of events
                const totalDays = parseInt(userInput.days, 10) || 1;
                const eventsPerDay = Math.max(1, Math.ceil(schedule.length / totalDays));
                for (let d = 1; d <= totalDays; d++) {
                    const dayEvents = schedule.slice((d - 1) * eventsPerDay, d * eventsPerDay);
                    normalizedSchedule.push({
                        day: d,
                        events: dayEvents.length > 0 ? dayEvents : [{
                            time: '10:00 AM',
                            title: `Day ${d} Local Exploration`,
                            category: 'sightseeing',
                            estimated_cost: 0.0,
                            description: 'Explore local sights, cafes, and neighborhoods.'
                        }]
                    });
                }
            }
        }

        if (normalizedSchedule.length === 0) {
            scheduleContainer.innerHTML = '<div class="day-card"><p class="text-muted">No schedule items generated.</p></div>';
        } else {
            normalizedSchedule.forEach((dayPlan, index) => {
                const dayCard = document.createElement('div');
                dayCard.className = 'day-card';
                const dayNum = dayPlan.day !== undefined ? dayPlan.day : (index + 1);

                const dayEvents = Array.isArray(dayPlan.events) ? dayPlan.events : [];
                const dayCost = dayEvents.reduce((acc, ev) => acc + (parseFloat(ev.estimated_cost) || 0), 0);

                let eventsHtml = dayEvents.map(ev => {
                    const categoryClass = (ev.category || 'landmark').toLowerCase().replace(/\s+/g, '-');
                    const costVal = parseFloat(ev.estimated_cost) || 0;
                    const costDisplay = costVal === 0 ? 'Free' : `$${costVal.toFixed(2)}`;

                    return `
                        <div class="event-item">
                            <div class="event-time">
                                <i class="fa-regular fa-clock"></i> ${escapeHtml(ev.time || 'All Day')}
                            </div>
                            <div class="event-content">
                                <h5>${escapeHtml(ev.title || 'Activity')}</h5>
                                <p>${escapeHtml(ev.description || '')}</p>
                                <span class="event-badge ${categoryClass}">${escapeHtml(ev.category || 'Activity')}</span>
                            </div>
                            <div class="event-cost">${costDisplay}</div>
                        </div>
                    `;
                }).join('');

                dayCard.innerHTML = `
                    <div class="day-header">
                        <div class="day-title"><i class="fa-solid fa-calendar-day"></i> Day ${dayNum}</div>
                        <div class="day-total">Daily Estimated: $${dayCost.toFixed(2)}</div>
                    </div>
                    <div class="events-list">
                        ${eventsHtml || '<p class="text-muted" style="padding: 1rem;">No events scheduled for this day.</p>'}
                    </div>
                `;
                scheduleContainer.appendChild(dayCard);
            });
        }

        // 2. Render Raw Research
        // Flights
        flightsList.innerHTML = '';
        (research.flights || []).forEach(fl => {
            const item = document.createElement('div');
            item.className = 'research-item-box';
            item.innerHTML = `
                <div class="research-item-header">
                    <span>${escapeHtml(fl.flight_name || 'Flight')} (${escapeHtml(fl.airline || 'Carrier')})</span>
                    <span class="research-item-price">$${parseFloat(fl.estimated_cost || 0).toFixed(2)}</span>
                </div>
                <div class="research-item-sub">Time: ${escapeHtml(fl.travel_time || 'N/A')} | ${escapeHtml(fl.notes || '')}</div>
            `;
            flightsList.appendChild(item);
        });

        // Hotels
        hotelsList.innerHTML = '';
        (research.hotels || []).forEach(ht => {
            const item = document.createElement('div');
            item.className = 'research-item-box';
            item.innerHTML = `
                <div class="research-item-header">
                    <span>${escapeHtml(ht.hotel_name || 'Hotel')} [${escapeHtml(ht.tier || 'mid-range')}]</span>
                    <span class="research-item-price">$${parseFloat(ht.price_per_night || 0).toFixed(2)}/nt</span>
                </div>
                <div class="research-item-sub">${escapeHtml(ht.safety_rating || '')} | ${escapeHtml(ht.location_notes || '')}</div>
            `;
            hotelsList.appendChild(item);
        });

        // Activities
        activitiesList.innerHTML = '';
        (research.activities || []).forEach(act => {
            const item = document.createElement('div');
            item.className = 'research-item-box';
            const cost = parseFloat(act.estimated_cost || 0);
            item.innerHTML = `
                <div class="research-item-header">
                    <span>${escapeHtml(act.activity_name || 'Activity')}</span>
                    <span class="research-item-price">${cost === 0 ? 'Free' : '$' + cost.toFixed(2)}</span>
                </div>
                <div class="research-item-sub">${escapeHtml(act.category || '')} (${act.duration_hours || 2}h) - ${escapeHtml(act.description || '')}</div>
            `;
            activitiesList.appendChild(item);
        });

        // 3. Render Budget Breakdown Table
        let totalFlights = 0;
        if (research.flights && research.flights.length > 0) {
            totalFlights = parseFloat(research.flights[0].estimated_cost) || 0;
        }

        let totalLodging = 0;
        if (research.hotels && research.hotels.length > 0) {
            const perNight = parseFloat(research.hotels[0].price_per_night) || 0;
            totalLodging = perNight * (userInput.days || 1);
        }

        const totalActivitiesCost = normalizedSchedule.reduce((sum, day) => {
            return sum + (day.events || []).reduce((dSum, ev) => dSum + (parseFloat(ev.estimated_cost) || 0), 0);
        }, 0);

        budgetTable.innerHTML = `
            <div class="budget-row">
                <span><i class="fa-solid fa-plane"></i> Estimated Roundtrip Transit</span>
                <span>$${totalFlights.toFixed(2)}</span>
            </div>
            <div class="budget-row">
                <span><i class="fa-solid fa-hotel"></i> Lodging (${userInput.days} nights)</span>
                <span>$${totalLodging.toFixed(2)}</span>
            </div>
            <div class="budget-row">
                <span><i class="fa-solid fa-utensils"></i> Activities, Dining & Attractions</span>
                <span>$${totalActivitiesCost.toFixed(2)}</span>
            </div>
            <div class="budget-row total">
                <span>Total Estimated Cost</span>
                <span>$${totalCost.toFixed(2)}</span>
            </div>
        `;

        resultsSection.style.display = 'block';
    }

    // --------------------------------------------------------------------------
    // Tab Navigation
    // --------------------------------------------------------------------------
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));

            btn.classList.add('active');
            const targetId = btn.getAttribute('data-tab');
            const pane = document.getElementById(targetId);
            if (pane) pane.classList.add('active');
        });
    });

    // --------------------------------------------------------------------------
    // Copy JSON State
    // --------------------------------------------------------------------------
    copyJsonBtn.addEventListener('click', () => {
        if (!currentJsonState) return;
        navigator.clipboard.writeText(JSON.stringify(currentJsonState, null, 2))
            .then(() => {
                const originalText = copyJsonBtn.innerHTML;
                copyJsonBtn.innerHTML = '<i class="fa-solid fa-check"></i> Copied!';
                setTimeout(() => {
                    copyJsonBtn.innerHTML = originalText;
                }, 2000);
            })
            .catch(err => {
                alert('Could not copy to clipboard: ' + err);
            });
    });

    // Utility: HTML Escaping
    function escapeHtml(str) {
        if (!str) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }
});
