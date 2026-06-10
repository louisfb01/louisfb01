# Next Steps

## Current Status

- YouTube is the only custom live milestone counter in the README.
- X and LinkedIn counters are intentionally not included because the reliable versions require platform credentials, approved API access, or unclear paid/gated developer plans.
- The duplicate standalone YouTube subscribers badge was removed.
- The top YouTube button is generated from the YouTube API and shows the subscriber count exposed by YouTube.
- The `YouTube to 100K` badge is generated from the same API call.
- `YOUTUBE_API_KEY` is configured in GitHub Actions and has been tested successfully.
- The workflow successfully read `72,400` subscribers from the YouTube Data API.
- Profile views and GitHub followers are live through public badges.

## YouTube Automation

- Workflow: `.github/workflows/update-youtube-countdown.yml`
- Script: `scripts/update_youtube_countdown.py`
- Outputs: `images/youtube.svg` and `images/youtube-countdown.svg`
- Schedule: every 5 minutes, plus manual runs through GitHub Actions.
- GitHub Actions schedule limit: 5 minutes is the shortest supported interval.
- GitHub may delay or drop scheduled jobs during high-load periods, so this is the fastest practical free refresh, not guaranteed true real time.
- API usage: about 1 YouTube Data API quota unit per run through `channels.list`.
- Daily usage at this cadence: about 288 quota units per day.
- Default YouTube Data API quota for most endpoints: 10,000 quota units per day.
- Remaining headroom if this workflow is the only API user: about 9,712 quota units per day.
- The workflow commits only when a generated SVG changes.

## Maintenance

- Keep pinned repositories managed directly in the GitHub profile settings.
- Re-run `Update YouTube Countdown` manually if you want the badge refreshed immediately after a visible subscriber milestone.
- If the README looks stale, wait a few minutes or hard-refresh the browser; GitHub can cache rendered README images briefly.
