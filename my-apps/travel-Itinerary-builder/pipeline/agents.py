import logging
import os
from pathlib import Path
from typing import Optional
from google.adk.agents import Agent, ParallelAgent, LoopAgent, SequentialAgent
from google.adk.skills import load_skill_from_dir
from google.adk.tools.skill_toolset import SkillToolset
from google.adk.tools import google_search
from .tools import (
    save_flight_research,
    save_hotel_research,
    save_activity_research,
    fetch_internet_activities,
    save_itinerary_schedule,
    evaluate_budget_and_finalize,
)

logger = logging.getLogger(__name__)


def get_gemini_model() -> str:
    """Retrieves the Gemini model from environment or defaults to gemini-2.0-flash."""
    return os.getenv("GEMINI_MODEL", "gemini-2.0-flash")


def get_activity_skill_toolset() -> Optional[SkillToolset]:
    """Loads the activity planner skill toolset from the skills directory."""
    skill_dir = Path(__file__).resolve().parent.parent / "skills" / "activity-planner-skill"
    if skill_dir.exists() and (skill_dir / "SKILL.md").exists():
        try:
            skill = load_skill_from_dir(skill_dir)
            return SkillToolset(skills=[skill])
        except Exception as e:
            logger.warning("Could not load activity planner skill from %s: %s", skill_dir, e)
    return None


def create_flight_researcher(model: Optional[str] = None) -> Agent:
    """Agent responsible for researching transportation options and costs."""
    model_name = model or get_gemini_model()
    instruction = """You are the FlightResearcher agent.
Your responsibility is to research and locate flight and transit options for the user's destination.
Look at the user's destination, duration, and budget in the session state `user_input`.

Provide 3 distinct flight/transit options (e.g. Economy Direct, Budget Airline, Premium/Flexible) with:
- flight_name (e.g., "Economy Non-Stop")
- airline (e.g., "United Airlines" or "Delta")
- travel_time (e.g., "6h 30m")
- estimated_cost (realistic roundtrip total in USD as a float)
- notes (baggage allowance, transfer details)

Call `save_flight_research(flights=[...])` with your options to update the state.
Always execute the tool call."""
    return Agent(
        name="FlightResearcher",
        model=model_name,
        instruction=instruction,
        tools=[save_flight_research]
    )


def create_hotel_researcher(model: Optional[str] = None) -> Agent:
    """Agent responsible for finding lodging matching user preferences and safety."""
    model_name = model or get_gemini_model()
    instruction = """You are the HotelResearcher agent.
Your responsibility is to find accommodation options for the user's destination that align with their interests and budget.
Look at the destination, days, budget, and interests in `user_input`.

Provide 3 diverse lodging options representing different tiers:
1. "luxury": High-end boutique or 5-star hotel with top amenities.
2. "mid-range": Comfortable 3-4 star hotel in a prime/safe neighborhood.
3. "budget": Highly-rated budget hotel, capsule hotel, or boutique hostel.

For each hotel include:
- hotel_name
- tier ("luxury", "mid-range", or "budget")
- price_per_night (float in USD)
- safety_rating (e.g., "Excellent - 9.2/10 in safe downtown district")
- location_notes (proximity to transit and main attractions)

Call `save_hotel_research(hotels=[...])` with your options to update the state.
Always execute the tool call."""
    return Agent(
        name="HotelResearcher",
        model=model_name,
        instruction=instruction,
        tools=[save_hotel_research]
    )


def create_activity_planner(model: Optional[str] = None) -> Agent:
    """Agent responsible for compiling landmarks, restaurants, and tours using Gemini skills."""
    model_name = model or get_gemini_model()
    skill_toolset = get_activity_skill_toolset()
    tools = [save_activity_research, fetch_internet_activities, google_search]
    if skill_toolset:
        tools.append(skill_toolset)

    instruction = """You are the ActivityPlanner agent utilizing the Gemini `activity-planner-skill`.
Your responsibility is to fetch real-time data from the internet and compile structured activity, landmark, dining, and tour recommendations matching the user's destination, days, and interests.
Check `user_input` in session state for destination, duration (days), and interests.

Skills & Guidelines:
1. Research and fetch data from the internet for the requested destination, duration (multi-day support), and user interests.
2. Provide a rich, curated list of at least 6-12 diverse activities scaled to the trip duration:
   - Key cultural landmarks and signature highlights matching user interests
   - Popular local food spots and restaurants (cheap eats and quality dining)
   - Free or low-cost activities (parks, public markets, historic walks)
   - Guided tours, excursions, or nature walks
3. Structure each activity with:
   - activity_name (string)
   - category ("landmark", "restaurant", "tour", "culture", "nature", "shopping")
   - estimated_cost (float in USD, 0.0 for free activities)
   - duration_hours (float, e.g. 2.0)
   - description (highlighting why it matches user interests and location context)
4. Robust Error Handling:
   - If internet search queries encounter errors, network timeouts, or missing details, handle them gracefully by returning verified regional highlights and appropriate error recovery details without breaking.
   - Ensure all output fields have valid default values.
5. Call `save_activity_research(activities=[...])` with your structured recommendations to update state.
Always execute the tool call."""
    return Agent(
        name="ActivityPlanner",
        model=model_name,
        instruction=instruction,
        tools=tools
    )


def create_scheduler(model: Optional[str] = None) -> Agent:
    """Agent that builds day-by-day sequence and refines based on critic feedback."""
    model_name = model or get_gemini_model()
    instruction = """You are the Scheduler agent in the Optimization Room.
Your goal is to build a realistic, day-by-day travel schedule covering all days from Day 1 to Day N and calculate total estimated costs.

Read the central state:
- `user_input`: destination, days, budget, interests
- `raw_research`: flights, hotels, activities
- `critic_feedback`: CRITICAL! Read any feedback from previous iterations.

If `critic_feedback` is present (e.g., "cost exceeds budget by $X, replace 5-star hotel with 3-star, pick free walking tours"):
- You MUST adapt the plan! Downgrade the chosen hotel tier (e.g. choose mid-range or budget from raw_research), select free or cheaper activity alternatives, or reduce dining costs to satisfy the budget constraint.
- Explicitly address the feedback in your schedule choices.

Calculate `total_estimated_cost`:
- Selected Roundtrip Flight cost
- Selected Lodging cost = (chosen hotel price_per_night * days)
- Selected Activities & Dining cost = sum of event costs across all days

Construct a detailed day-by-day schedule:
- Must contain an entry for each day from Day 1 to Day N (where N = user_input.days).
- The `schedule` parameter MUST be a list of day objects with `day` (integer) and `events` (list of event objects):
  [
    {
      "day": 1,
      "events": [
        {
          "time": "09:00 AM",
          "title": "Morning: Arrival & City Exploration",
          "category": "sightseeing",
          "estimated_cost": 25.0,
          "description": "Visit historic downtown landmarks"
        },
        {
          "time": "01:00 PM",
          "title": "Lunch: Regional Cuisine",
          "category": "dining",
          "estimated_cost": 20.0,
          "description": "Authentic local specialty lunch"
        }
      ]
    },
    {
      "day": 2,
      "events": [...]
    }
  ]

Call `save_itinerary_schedule(schedule=[...], total_estimated_cost=...)` to update state.
Always execute the tool call."""
    return Agent(
        name="Scheduler",
        model=model_name,
        instruction=instruction,
        tools=[save_itinerary_schedule]
    )


def create_budget_enforcer(model: Optional[str] = None) -> Agent:
    """Agent that validates costs against budget and signals loop termination or critique."""
    model_name = model or get_gemini_model()
    instruction = """You are the BudgetEnforcer agent in the Optimization Room.
Your role is to strictly validate the current itinerary against the user's budget.

Examine the session state:
- `user_input.budget`: The target maximum spending limit.
- `current_itinerary.total_estimated_cost`: The total calculated cost.
- `current_itinerary.schedule`: The current proposed plan.

Rules:
1. If `total_estimated_cost <= budget`:
   - Set approved = True.
   - Call `evaluate_budget_and_finalize(approved=True, critic_feedback="Budget approved: Itinerary is within budget.")`.
2. If `total_estimated_cost > budget`:
   - Set approved = False.
   - Calculate the overage: overage = total_estimated_cost - budget.
   - Provide concrete, actionable `critic_feedback` for the Scheduler (e.g. "Total cost $3200 exceeds budget $2500 by $700. Action required: Switch hotel from Luxury ($350/night) to Budget/Mid-range ($120/night), replace paid private tour with self-guided walk, and adjust daily dining estimate to $40/day.").
   - Call `evaluate_budget_and_finalize(approved=False, critic_feedback=...)`.

Always execute the tool call."""
    return Agent(
        name="BudgetEnforcer",
        model=model_name,
        instruction=instruction,
        tools=[evaluate_budget_and_finalize]
    )


def create_discovery_team(model: Optional[str] = None) -> ParallelAgent:
    """Creates the Parallel Discovery Team subagents."""
    return ParallelAgent(
        name="DiscoveryTeam",
        sub_agents=[
            create_flight_researcher(model),
            create_hotel_researcher(model),
            create_activity_planner(model),
        ]
    )


def create_optimization_room(model: Optional[str] = None, max_iterations: int = 5) -> LoopAgent:
    """Creates the Loop Optimization Room with Scheduler and BudgetEnforcer."""
    return LoopAgent(
        name="OptimizationRoom",
        sub_agents=[
            create_scheduler(model),
            create_budget_enforcer(model),
        ],
        max_iterations=max_iterations
    )


def create_travel_pipeline(model: Optional[str] = None, max_iterations: int = 5) -> SequentialAgent:
    """Creates the complete Sequential Pipeline orchestrating Parallel Discovery and Loop Optimization.

    Explicitly implements the architecture from SPECIFICATIONS.md:
    Sequential Pipeline:
      -> ParallelAgent (Discovery Team: FlightResearcher, HotelResearcher, ActivityPlanner)
      -> LoopAgent (Optimization Room: Scheduler, BudgetEnforcer, max_iterations=5)
    """
    discovery = create_discovery_team(model)
    optimization = create_optimization_room(model, max_iterations=max_iterations)
    
    return SequentialAgent(
        name="TravelItineraryPipeline",
        sub_agents=[discovery, optimization]
    )
