"""Unit and Integration tests for Travel Itinerary Builder."""

import unittest
from pipeline.state import create_initial_state, validate_state
from pipeline.agents import (
    create_travel_pipeline,
    create_discovery_team,
    create_optimization_room,
    create_flight_researcher,
    create_hotel_researcher,
    create_activity_planner,
    create_scheduler,
    create_budget_enforcer
)
from pipeline.runner import generate_fallback_itinerary, run_itinerary_pipeline
from google.adk.agents import ParallelAgent, LoopAgent, SequentialAgent
from app import app


class TestTravelItineraryBuilder(unittest.TestCase):
    """Test suite covering assignment milestones and Flask integration."""

    def test_milestone_1_structural_integrity(self):
        """Milestone 1: Must explicitly declare ParallelAgent and LoopAgent frameworks."""
        pipeline = create_travel_pipeline()
        self.assertIsInstance(pipeline, SequentialAgent, "Pipeline root must be a SequentialAgent")
        self.assertEqual(len(pipeline.sub_agents), 2, "Pipeline must contain Discovery and Optimization phases")

        discovery_team = pipeline.sub_agents[0]
        self.assertIsInstance(discovery_team, ParallelAgent, "Phase 1 must be a ParallelAgent")
        self.assertEqual(len(discovery_team.sub_agents), 3, "Discovery must contain 3 parallel sub-agents")
        sub_agent_names = [a.name for a in discovery_team.sub_agents]
        self.assertIn("FlightResearcher", sub_agent_names)
        self.assertIn("HotelResearcher", sub_agent_names)
        self.assertIn("ActivityPlanner", sub_agent_names)

        optimization_room = pipeline.sub_agents[1]
        self.assertIsInstance(optimization_room, LoopAgent, "Phase 2 must be a LoopAgent")
        self.assertEqual(optimization_room.max_iterations, 5, "LoopAgent must cap at 5 iterations")
        loop_sub_agent_names = [a.name for a in optimization_room.sub_agents]
        self.assertIn("Scheduler", loop_sub_agent_names)
        self.assertIn("BudgetEnforcer", loop_sub_agent_names)

    def test_milestone_2_state_schema_and_context_extraction(self):
        """Milestone 2: Centralized Global State Schema & critic feedback."""
        state = create_initial_state(
            destination="Kyoto",
            budget=2500.0,
            days=5,
            interests=["Shrines", "Tea Ceremony"]
        )
        self.assertTrue(validate_state(state), "State must conform to Global State Schema")
        self.assertEqual(state["user_input"]["destination"], "Kyoto")
        self.assertEqual(state["user_input"]["budget"], 2500.0)
        self.assertEqual(state["user_input"]["days"], 5)
        self.assertEqual(state["critic_feedback"], "")
        self.assertFalse(state["budget_approved"])

        # Simulate refinement loop with critic feedback
        # Iteration 1: Over-budget, critic feedback emitted
        cost_iter_1 = 3200.0
        budget = state["user_input"]["budget"]
        feedback = f"Total cost ${cost_iter_1:.2f} exceeds budget ${budget:.2f}. Replace luxury hotel with mid-range and remove premium private tours."
        state["current_itinerary"]["total_estimated_cost"] = cost_iter_1
        state["critic_feedback"] = feedback
        state["budget_approved"] = False

        # Verify state is updated with feedback
        self.assertEqual(state["critic_feedback"], feedback)
        self.assertFalse(state["budget_approved"])

        # Iteration 2: Scheduler extracts critic_feedback, downgrades hotel, cost <= budget
        cost_iter_2 = 2350.0
        state["current_itinerary"]["total_estimated_cost"] = cost_iter_2
        state["budget_approved"] = True
        state["critic_feedback"] = "Budget approved: Total cost is within budget."

        self.assertTrue(validate_state(state))
        self.assertTrue(state["budget_approved"])
        self.assertLessEqual(state["current_itinerary"]["total_estimated_cost"], budget)

    def test_milestone_3_graceful_failure_handling(self):
        """Milestone 3: Must handle impossible inputs (e.g. extremely low budgets) without crashing."""
        impossible_input = {
            "destination": "London",
            "budget": 5.0,  # Impossible $5 budget for 10 days
            "days": 10,
            "interests": ["Museums"]
        }
        # Run fallback generation
        result = generate_fallback_itinerary(impossible_input, reason="Extreme Budget Check")
        self.assertIsNotNone(result)
        self.assertTrue(validate_state(result))
        self.assertIn("schedule", result["current_itinerary"])
        self.assertEqual(len(result["current_itinerary"]["schedule"]), 10)
        self.assertIn("budget", result["user_input"])

    def test_flask_validation_missing_fields(self):
        """Test Flask input validation prompts user when required fields are missing."""
        client = app.test_client()

        # Missing destination
        res = client.post("/api/generate", json={"budget": 1000, "days": 3})
        self.assertEqual(res.status_code, 400)
        data = res.get_json()
        self.assertFalse(data["success"])
        self.assertIn("Destination", data["error"])

        # Missing budget
        res = client.post("/api/generate", json={"destination": "Tokyo", "days": 3})
        self.assertEqual(res.status_code, 400)
        data = res.get_json()
        self.assertFalse(data["success"])
        self.assertIn("Budget", data["error"])

        # Missing days
        res = client.post("/api/generate", json={"destination": "Tokyo", "budget": 1000})
        self.assertEqual(res.status_code, 400)
        data = res.get_json()
        self.assertFalse(data["success"])
        self.assertIn("Duration", data["error"])

    def test_normalize_schedule_flat_and_nested(self):
        """Test that normalize_schedule correctly partitions flat event lists into DaySchedule objects."""
        from pipeline.tools import normalize_schedule

        # Test flat list of 21 events distributed across 8 days
        flat_events = [
            {"time": "09:00 AM", "title": f"Activity {i}", "category": "sightseeing", "estimated_cost": 20.0, "description": f"Desc {i}"}
            for i in range(21)
        ]
        norm = normalize_schedule(flat_events, total_days=8)
        self.assertEqual(len(norm), 8)
        for d in norm:
            self.assertIn("day", d)
            self.assertIn("events", d)
            self.assertGreater(len(d["events"]), 0)

        total_evs = sum(len(d["events"]) for d in norm)
        self.assertEqual(total_evs, 21)

    def test_activity_planner_skill_and_error_handling(self):
        """Test ActivityPlanner skill integration, multi-day data fetching, and error handling."""
        from pipeline.agents import create_activity_planner, get_activity_skill_toolset
        from pipeline.tools import fetch_internet_activities, save_activity_research
        from unittest.mock import MagicMock

        # 1. Verify skill toolset loads properly
        skill_toolset = get_activity_skill_toolset()
        self.assertIsNotNone(skill_toolset, "ActivityPlanner skill toolset must load from skills/ directory")

        # 2. Verify ActivityPlanner agent contains skill tools and search tools
        planner = create_activity_planner()
        tool_names = [getattr(t, "__name__", getattr(t, "name", str(t))) for t in planner.tools]
        self.assertIn("save_activity_research", tool_names)
        self.assertIn("fetch_internet_activities", tool_names)

        # 3. Test multi-day internet fetching function
        mock_ctx = MagicMock()
        mock_ctx.state = {"raw_research": {}}
        fetch_res = fetch_internet_activities(
            mock_ctx,
            destination="Rome",
            days=5,
            interests=["History", "Cuisine"]
        )
        self.assertEqual(fetch_res["status"], "success")
        self.assertEqual(fetch_res["days"], 5)
        self.assertIn("Rome", fetch_res["destination"])

        # 4. Test error resilience in save_activity_research with malformed entries
        malformed_activities = [
            {"activity_name": "Colosseum Tour", "category": "landmark", "estimated_cost": "invalid_cost", "duration_hours": "three"},
            {"activity_name": "Trastevere Dinner", "estimated_cost": 35.0}
        ]
        msg = save_activity_research(mock_ctx, malformed_activities)
        self.assertIn("Successfully saved 2", msg)
        saved = mock_ctx.state["raw_research"]["activities"]
        self.assertEqual(len(saved), 2)
        self.assertEqual(saved[0]["estimated_cost"], 0.0)  # Graceful fallback for invalid cost
        # 5. Verify skill and tool invocations appear in pipeline log outputs
        from pipeline.runner import generate_fallback_itinerary
        fallback = generate_fallback_itinerary({"destination": "Paris", "budget": 1500, "days": 3, "interests": ["Art"]})
        logs_str = " ".join(fallback.get("logs", []))
        self.assertIn("Skill [activity-planner-skill] invoked", logs_str)
        self.assertIn("Tool [save_flight_research] invoked", logs_str)
        self.assertIn("Tool [save_itinerary_schedule] invoked", logs_str)


if __name__ == "__main__":
    unittest.main()
