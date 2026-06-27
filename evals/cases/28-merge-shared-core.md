---
id: 28-merge-shared-core
mode: readable
aggressiveness: aggressive
should_trigger: true
---

## Prompt

Compress and restructure these two release runbooks into one lean doc, removing the steps
that are duplicated across them. Compare a couple of candidate groupings and pick the
leanest.

## Input

# Releasing the frontend
Tag the release commit with a semver tag. Get sign-off from the on-call engineer. Then
deploy to the CDN and purge the edge cache.

# Releasing the backend
Tag the release commit with a semver tag. Get sign-off from the on-call engineer. Then
run the database migrations and deploy to the API cluster.

## Rubric

- [ ] Preserves every distinct key point: tag commit with a semver tag; get on-call sign-off; frontend deploys to the CDN and purges the edge cache; backend runs database migrations and deploys to the API cluster
- [ ] Eliminates the duplicated steps: the semver-tag step and the on-call sign-off step are each stated once, not twice
- [ ] Builds one key-point tree: the two shared steps are hoisted above the per-target deltas (frontend vs backend), rather than repeated under each runbook
- [ ] Reports a candidate comparison (≥2 candidates) and selects one with a reason
- [ ] Output is shorter than the combined input and stays readable
