# Bring Your Python Jobs to Snowflake: Code Bundles Miniseries

Sample code for the miniseries. Each episode directory is a complete,
runnable snapshot of the job at that point in the story.

| Episode | Directory | Retires | Replaced by |
| --- | --- | --- | --- |
| 0 | [episode-0-intro](episode-0-intro) | n/a: starting point | n/a |
| 1 | [episode-1-code-bundle](episode-1-code-bundle) | Python on a VM, stored credentials | Warehouse Code Bundle with an injected session |
| 2 | [episode-2-task](episode-2-task) | Cron on the host | Snowflake Task |
| 3 | [episode-3-observability](episode-3-observability) | Host log files | Code Bundle/Task history, event-table logs |
| 4 | [episode-4-dcm](episode-4-dcm) | Manual deploy to the box | DCM PLAN/DEPLOY |

`shared/fixtures/` holds synthetic input data and expected output used to
compare episodes.

## Keeping episodes in sync

`scripts/episodes.toml` defines the episode order and which files each episode may
change relative to the previous one. To check for drift:

```bash
python scripts/check_episodes.py
```

To carry a change in an earlier episode forward, use the
`propagate-episode-change` skill (`.cortex/skills/`).
