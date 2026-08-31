---
name: activity-planner-skill
description: Gemini skill for fetching travel activities, landmarks, dining, and tours from the internet with multi-day support and robust error handling.
---

# Activity Planner Skill for Gemini

## Overview
This skill instructs Gemini to research, fetch, and curate real-time travel activity data from the internet for any destination across single or multi-day trip durations. It enforces structured formatting and robust error handling.

## Core Capabilities

### 1. Fetching Data from the Internet
- Query the internet or search engines for up-to-date travel attractions, cultural landmarks, local food spots, walking routes, and guided tours based on:
  - Destination (city, region, or country)
  - Duration (number of days)
  - User interests (e.g. History, Food & Dining, Nature & Hiking, Shopping, Art)

### 2. Multi-Day Itinerary Support
- Scale recommendations according to trip duration (1 to 30 days).
- Ensure sufficient diverse activities to populate morning, afternoon, and evening slots for all days.
- Include a balanced mix of:
  - Primary landmarks and top-rated cultural highlights
  - Local eateries and signature dining spots (cheap eats and quality dining)
  - Free/low-cost activities (parks, public viewpoints, historic districts)
  - Day trips, nature excursions, and guided tours

### 3. Structured Data Formatting
All discovered activities must conform to the following schema:
- `activity_name`: String (name of the landmark, restaurant, or tour)
- `category`: String (one of `"landmark"`, `"restaurant"`, `"tour"`, `"culture"`, `"nature"`, `"shopping"`)
- `estimated_cost`: Float in USD (0.0 for free activities)
- `duration_hours`: Float (e.g. 1.5, 2.0, 3.5)
- `description`: String (highlighting key features, why it matches user interests, and practical tips)

### 4. Error Handling and Resilience
- **Connectivity / Search Failures**: If search queries fail, timeout, or return incomplete results, gracefully synthesize verified local landmarks and popular dining staples for the destination.
- **Malformed Data**: Ensure all fields have valid fallback defaults (e.g. default `estimated_cost = 0.0`, `duration_hours = 2.0`).
- **Error Messages**: If critical issues occur, log informative messages and return valid fallback items so the pipeline never breaks.
- Always execute `save_activity_research(activities=[...])` with the resulting structured list.
