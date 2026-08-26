# Class 02C work area

These utilities observe the golden agent application without editing its source.

| File | Purpose |
|---|---|
| `start_api_server.sh` | Starts the golden agents with native Google Cloud OpenTelemetry export |
| `run_and_record.sh` | Creates a session, runs two messages, and records session events to JSONL |
| `show_events.sh` | Displays a concise event table |
| `play_events.sh` | Plays the recorded event sequence at a chosen speed |
| `replay_events.py` | Reconstructs the JSONL recording as a new Google Cloud trace |
| `verify_golden_source.sh` | Verifies the golden source and configuration against the supplied manifest |

Generated files such as `sessions.db`, `events.jsonl`, `session.json`, and
`run-*.json` are written here and are ignored by Git.
