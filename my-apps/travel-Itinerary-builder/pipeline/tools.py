from datetime import datetime, timezone
import json
from typing import Any, Dict, List, Optional
from google.adk.tools import ToolContext, exit_loop
from .event_logger import append_event_to_json


def save_flight_research(
    tool_context: ToolContext,
    flights: List[Dict[str, Any]]
) -> str:
    """Saves discovered flight and transport options into the central state."""
    raw_research = dict(tool_context.state.get("raw_research", {}))
    raw_research["flights"] = flights
    tool_context.state["raw_research"] = raw_research
    msg = f"Successfully saved {len(flights)} flight options to raw_research."
    append_event_to_json({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "tool_execution",
        "agent": "FlightResearcher",
        "tool": "save_flight_research",
        "saved_flights_count": len(flights),
        "flights": flights,
        "result": msg
    })
    return msg


def save_hotel_research(
    tool_context: ToolContext,
    hotels: List[Dict[str, Any]]
) -> str:
    """Saves lodging and hotel options into the central state."""
    raw_research = dict(tool_context.state.get("raw_research", {}))
    raw_research["hotels"] = hotels
    tool_context.state["raw_research"] = raw_research
    msg = f"Successfully saved {len(hotels)} hotel options to raw_research."
    append_event_to_json({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "tool_execution",
        "agent": "HotelResearcher",
        "tool": "save_hotel_research",
        "saved_hotels_count": len(hotels),
        "hotels": hotels,
        "result": msg
    })
    return msg


def save_activity_research(
    tool_context: ToolContext,
    activities: List[Dict[str, Any]]
) -> str:
    """Saves landmark, restaurant, and tour options into the central state."""
    raw_research = dict(tool_context.state.get("raw_research", {}))
    raw_research["activities"] = activities
    tool_context.state["raw_research"] = raw_research
    msg = f"Successfully saved {len(activities)} activity options to raw_research."
    append_event_to_json({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "tool_execution",
        "agent": "ActivityPlanner",
        "tool": "save_activity_research",
        "saved_activities_count": len(activities),
        "activities": activities,
        "result": msg
    })
    return msg


import re


def normalize_schedule(schedule: Any, total_days: int = 1) -> List[Dict[str, Any]]:
    """Normalizes any schedule structure into standard List[DaySchedule]:
    [{"day": 1, "events": [...]}, {"day": 2, "events": [...]}, ...]
    """
    num_days = max(1, total_days)
    if not isinstance(schedule, list) or not schedule:
        return [{"day": d, "events": []} for d in range(1, num_days + 1)]

    # Check if already in standard [{"day": 1, "events": [...]}, ...] format
    is_standard = True
    for item in schedule:
        if not isinstance(item, dict) or "events" not in item or not isinstance(item["events"], list):
            is_standard = False
            break
    if is_standard and len(schedule) > 0:
        normalized = []
        for idx, item in enumerate(schedule):
            day_num = item.get("day", idx + 1)
            try:
                day_num = int(day_num)
            except (ValueError, TypeError):
                day_num = idx + 1
            normalized.append({
                "day": day_num,
                "events": item.get("events", [])
            })
        return normalized

    # Extract all flat events or detect day numbers
    flat_events: List[Dict[str, Any]] = []
    explicit_day_groups: Dict[int, List[Dict[str, Any]]] = {}

    for idx, item in enumerate(schedule):
        if not isinstance(item, dict):
            continue

        # If it has an events list inside
        if "events" in item and isinstance(item["events"], list):
            d = item.get("day", idx + 1)
            try:
                d = int(d)
            except (ValueError, TypeError):
                d = idx + 1
            explicit_day_groups.setdefault(d, []).extend(item["events"])
            continue

        # If it has day field
        if "day" in item:
            try:
                d = int(item["day"])
                explicit_day_groups.setdefault(d, []).append(item)
                continue
            except (ValueError, TypeError):
                pass

        # Check title for "Day X"
        title = item.get("title", "")
        day_match = re.search(r'\bDay\s*(\d+)\b', title, re.IGNORECASE)
        if day_match:
            d = int(day_match.group(1))
            explicit_day_groups.setdefault(d, []).append(item)
            continue

        flat_events.append(item)

    if explicit_day_groups and not flat_events:
        return [{"day": d, "events": explicit_day_groups[d]} for d in sorted(explicit_day_groups.keys())]

    result_days: Dict[int, List[Dict[str, Any]]] = {d: [] for d in range(1, num_days + 1)}

    for d, evs in explicit_day_groups.items():
        if d in result_days:
            result_days[d].extend(evs)
        else:
            result_days[d] = evs

    if flat_events:
        total_evs = len(flat_events)
        base_count = total_evs // num_days
        remainder = total_evs % num_days
        idx = 0
        for d in range(1, num_days + 1):
            count = base_count + (1 if d <= remainder else 0)
            day_slice = flat_events[idx : idx + count]
            idx += count
            if not day_slice and not result_days[d]:
                day_slice = [{
                    "time": "10:00 AM",
                    "title": f"Day {d} Local Exploration",
                    "category": "sightseeing",
                    "estimated_cost": 0.0,
                    "description": "Explore local neighborhood sights and culture."
                }]
            result_days[d].extend(day_slice)

    return [{"day": d, "events": result_days[d]} for d in sorted(result_days.keys())]


def save_itinerary_schedule(
    tool_context: ToolContext,
    schedule: List[Dict[str, Any]],
    total_estimated_cost: float
) -> str:
    """Saves the structured multi-day itinerary and total estimated cost into central state.
    
    Parameters:
        schedule: A list of day objects with Day numbers and events list, e.g.
                  [{"day": 1, "events": [{"time": "09:00 AM", "title": "...", "category": "...", "estimated_cost": 20.0, "description": "..."}]}]
        total_estimated_cost: Total cost in USD (flights + hotel * days + all activity costs).
    """
    user_input = tool_context.state.get("user_input", {})
    days = int(user_input.get("days", 1))
    normalized_schedule = normalize_schedule(schedule, total_days=days)

    itinerary = {
        "total_estimated_cost": float(total_estimated_cost),
        "schedule": normalized_schedule
    }
    tool_context.state["current_itinerary"] = itinerary
    msg = f"Successfully saved itinerary for {len(normalized_schedule)} days with total cost ${total_estimated_cost:.2f}."
    append_event_to_json({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "tool_execution",
        "agent": "Scheduler",
        "tool": "save_itinerary_schedule",
        "days_count": len(normalized_schedule),
        "total_estimated_cost": float(total_estimated_cost),
        "schedule": normalized_schedule,
        "result": msg
    })
    return msg


def evaluate_budget_and_finalize(
    tool_context: ToolContext,
    approved: bool,
    critic_feedback: str = ""
) -> str:
    """Validates whether current itinerary satisfies user budget and terminates loop or requests refinement."""
    user_input = tool_context.state.get("user_input", {})
    budget = float(user_input.get("budget", 0.0))
    current_itinerary = tool_context.state.get("current_itinerary", {})
    cost = float(current_itinerary.get("total_estimated_cost", 0.0))

    if cost <= budget or approved:
        tool_context.state["budget_approved"] = True
        tool_context.state["critic_feedback"] = "Budget approved: Total cost is within budget."
        # Escalate / exit the LoopAgent
        exit_loop(tool_context)
        msg = f"BUDGET APPROVED: Total cost (${cost:.2f}) is within budget (${budget:.2f}). Exiting optimization loop."
        append_event_to_json({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": "tool_execution",
            "agent": "BudgetEnforcer",
            "tool": "evaluate_budget_and_finalize",
            "approved": True,
            "total_estimated_cost": cost,
            "budget": budget,
            "action": "exit_loop",
            "result": msg
        })
        return msg
    else:
        tool_context.state["budget_approved"] = False
        feedback_msg = critic_feedback or f"Total cost (${cost:.2f}) exceeds budget (${budget:.2f}) by ${cost - budget:.2f}. Replace luxury items with budget alternatives."
        tool_context.state["critic_feedback"] = feedback_msg
        msg = f"BUDGET REJECTED: {feedback_msg}. Optimization loop will trigger Scheduler for revision."
        append_event_to_json({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": "tool_execution",
            "agent": "BudgetEnforcer",
            "tool": "evaluate_budget_and_finalize",
            "approved": False,
            "total_estimated_cost": cost,
            "budget": budget,
            "critic_feedback": feedback_msg,
            "action": "continue_loop",
            "result": msg
        })
        return msg
