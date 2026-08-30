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

    def test_flask_successful_generation(self):
        """Test Flask successful generation endpoint."""
        client = app.test_client()
        res = client.post("/api/generate", json={
            "destination": "Barcelona",
            "budget": 1800,
            "days": 4,
            "interests": ["Architecture", "Tapas"]
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertTrue(data["is_valid_schema"])
        state = data["data"]
        self.assertEqual(state["user_input"]["destination"], "Barcelona")
        self.assertEqual(len(state["current_itinerary"]["schedule"]), 4)


if __name__ == "__main__":
    unittest.main()
