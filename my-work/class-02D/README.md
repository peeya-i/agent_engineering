# Class 02D — Deploying to Agent Platform (planning notes)

> **Status: planning, not a student-facing lab.** Nothing here has been built or
> tested. This file records the scope, the decisions already taken, and the
> obstacles found while testing Class 02C on 2026-09-01, so none of it has to be
> rediscovered.

---

## Why this is a separate class

Class 02C runs ADK on the student's own machine and exports OpenTelemetry spans
to Cloud Trace. That is deliberate and it stays that way. But it means the whole
Agent Platform console — Agent Registry, Sessions services, Deployments, Memory
Bank, Evaluation — is empty for a 02C student, because every one of those pages
lists resources *deployed to* Agent Platform.

That console is where the industry conversation is, and students ask about it. It
deserves its own class rather than three tasks bolted onto a lab that already has
twelve.

---

## What 02D teaches

1. Deploy the Class 02C golden application to Agent Engine.
2. Read the same agent's telemetry from the **Agent Registry → Traces** tab
   (Session / Trace / Span views) rather than from Trace Explorer.
3. Use the managed **Sessions service** instead of a local SQLite file.
4. Compare local-versus-deployed observability: what each surface shows, what it
   hides, and which questions each one can answer.
5. **Diagnose a failed invocation from its spans alone** — see below.

The entry point is a single command:

```bash
adk deploy agent_engine \
  --project=<project> \
  --region=<region> \
  --display_name=<name> \
  --otel_to_cloud \
  <agent>
```

`--staging_bucket` is deprecated in ADK 2.6.0, so the old GCS setup step is gone.
`--session_service_uri agentengine://<id>` is what populates the managed Sessions
page.

---

## The failure-diagnosis exercise

This is the strongest exercise idea to come out of testing 02C, and it belongs
here rather than in 02C's Task 7.

**The idea.** Students spend the whole of 02C reading healthy traces. Reading a
*failed* trace is a different and more useful skill: find the invocation that
went wrong, follow the span tree to the failing leaf, and explain the failure
from the spans without reading application logs.

**Where it came from.** During 02C testing, one run died on a Wikipedia HTTP 429
and left five `Error`-status spans sitting beside two successful invocations in
the same project. Reading that trace against the healthy ones was more
instructive than any exercise in the lab.

**The problem to solve first.** That failure is no longer reproducible. 02C's
Wikipedia tool was hardened to catch the exception and return
`{"status": "unavailable", ...}`, so the tool now degrades gracefully and the
span carries **no error status at all**. The very fix that made 02C reliable
removed the failure this exercise depends on. Any induced failure must therefore
be deliberate and separate from the hardened tool.

**Candidate ways to induce a failure**, in order of preference:

| Method | How | Why it is good or bad |
|---|---|---|
| Invalid model name | `MODEL=gemini-does-not-exist` | One env var, no source edit, reversible, fails fast at `call_llm`. Best candidate. |
| Region without the model | `GOOGLE_CLOUD_LOCATION=<region lacking the model>` | Also one env var; produces a `NOT_FOUND` on the model call. Needs a region confirmed not to serve the model. |
| Revoked permission | remove `roles/aiplatform.user` | Realistic, but needs admin rights a student will not have in a lab project. |
| A deliberately failing tool | add a tool that raises | Fully reliable, but requires editing the golden source, which the course promises not to do. |

Both preferred methods work through `.env` or a single-run override, which fits
how 02C already teaches `MODEL`. Whichever is chosen must be verified to produce
a genuine `Error` span status, not a silently handled result.

**Questions the exercise should ask.** Which span failed, and which succeeded
before it? What did the parent do when the child failed? How far up did the
failure propagate? What can you tell about the cause from the span alone, and
what needs the logs? Why did the agents that ran before the failure still leave
successful spans?

---

## Known obstacles

Recorded while testing 02C. None of these is solved.

1. **`file_writer` writes to the local filesystem.** The golden application's
   final step writes `movie_pitches/<title>.txt`. On Agent Engine that lands in
   an ephemeral container and disappears, so the lab's tangible artifact is lost.
   Either the agent moves to the artifact service
   (`--artifact_service_uri gs://<bucket>`) or the deployed version has no
   visible output. **This is a design change, not a flag, and it gates whether a
   deployed agent is demonstrable at all.** Solve it before building anything
   else.

2. **Qwiklabs permissions are unverified.** Creating a `reasoningEngines`
   resource may be outside a student account's rights, and a deployment is a
   billable resource that keeps running. Test this early — if it fails, the whole
   class needs a different project model.

3. **Region.** Now handled: both 02C `.env` templates ship
   `GOOGLE_CLOUD_LOCATION=us-central1` as of 2026-09-01, because Agent Engine
   requires a real region and rejects `global`.

---

## Carried over from 02C

Fixes made in 02C that this class inherits and must not regress:

- `wikipedia.set_user_agent(...)` — the package default is rate-limited to HTTP
  429 by Wikimedia, which surfaces as a bare `JSONDecodeError`.
- `service.instance.id` in `OTEL_RESOURCE_ATTRIBUTES` — without it,
  `telemetry.googleapis.com` rejects every metrics batch with
  "prometheus_target resource type must have an instance specified".
- `get_gcp_resource(project_id)` must be passed explicitly when setting up OTel
  providers by hand; setting `GOOGLE_CLOUD_PROJECT` is not enough.
- `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS` defaults **on** and is a separate knob
  from `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT`. 02C leaves it on
  deliberately and teaches it. Decide whether a deployed agent should do the
  same — the exposure is larger when the agent is not on a student's laptop.
