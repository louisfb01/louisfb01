# Next Steps

## Current Status

- YouTube is the only custom live milestone counter in the README.
- The duplicate standalone YouTube subscribers badge was removed.
- The README now uses `images/youtube-countdown.svg`, labeled `YouTube to 100K`.
- `YOUTUBE_API_KEY` is configured in GitHub Actions.
- The workflow successfully reaches the YouTube Data API and reads the exact subscriber count.
- Profile views and GitHub followers are live through public badges.

## YouTube Automation

- Workflow: `.github/workflows/update-youtube-countdown.yml`
- Script: `scripts/update_youtube_countdown.py`
- Output: `images/youtube-countdown.svg`
- Schedule: daily at 08:17 UTC, plus manual runs through GitHub Actions.
- API usage: about 1 YouTube Data API quota unit per run through `channels.list`.

## Maintenance

- Keep pinned repositories managed directly in the GitHub profile settings.
- Re-run `Update YouTube Countdown` manually if you want the badge refreshed immediately after a visible subscriber milestone.
