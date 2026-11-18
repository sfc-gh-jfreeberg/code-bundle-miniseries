---
name: propagate-episode-change
description: Carry a change made in one episode directory forward into every later episode in the miniseries, then verify with scripts/check_episodes.py. Use when the user edits an episode's code and wants later episodes kept in sync.
---

# Propagate an episode change

The repo has one full snapshot per episode, ordered by `chain` in `scripts/episodes.toml`.
Each episode builds on the previous one. A change to an earlier episode
(for example, a new query in `episode-0-intro/job.py`) must show up in every
later episode, adapted to that episode's own changes.

## Steps

1. **Find the change.** Run `git diff` (and `git status` for new files) to see
   what changed. Identify the source episode, which is the earliest episode in
   `chain` with changes. If changes span several episodes, ask which one is the
   source.
2. **Classify the change.** Is it shared logic (it should flow forward
   unchanged), or is it specific to that episode's step (for example, the
   Snowpark session swap in episode 1, which later episodes already have)?
   Only shared logic is propagated.
3. **Apply it forward.** For each later episode in order:
   - Apply the same semantic change, not a blind text patch. Later episodes may
     have rewritten the surrounding lines. Examples: a new query in episode 0
     uses `cursor.execute`, but it must use `session.sql(...)` from episode 1
     on; from episode 3 on it must sit inside the error-logging wrapper.
   - Keep each episode's own deltas intact.
   - Stop and ask if the change conflicts with what a later episode
     demonstrates (for example, it touches the business rule episode 4 changes).
4. **Verify.** Run `python scripts/check_episodes.py` and fix any violations.
   If the change needs a file that isn't in an episode's `allowed` list, update
   `scripts/episodes.toml` only if the user agrees the change belongs to that step.
5. **Flag narrative impact.** List anything that may no longer match the
   videos or blogs, such as quoted snippets, line numbers, or on-screen diffs
   in the episode READMEs.

## Report

Summarize, per episode: what changed, any adaptations, the check result, and
narrative items to review.
