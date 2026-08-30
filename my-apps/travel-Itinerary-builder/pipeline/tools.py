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


def save_itinerary_schedule(
    tool_context: ToolContext,
    schedule: List[Dict[str, Any]],
    total_estimated_cost: float
) -> str:
    """Saves the structured multi-day itinerary and total estimated cost into central state."""
    itinerary = {
        "total_estimated_cost": float(total_estimated_cost),
        "schedule": schedule
    }
    tool_context.state["current_itinerary"] = itinerary
    msg = f"Successfully saved itinerary for {len(schedule)} days with total cost ${total_estimated_cost:.2f}."
    append_event_to_json({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "tool_execution",
        "agent": "Scheduler",
        "tool": "save_itinerary_schedule",
        "days_count": len(schedule),
        "total_estimated_cost": float(total_estimated_cost),
        "schedule": schedule,
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
