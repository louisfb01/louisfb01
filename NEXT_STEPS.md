# Next Steps

## Live Counters And Milestone Countdown

Status:

- YouTube subscriber count is already live in `README.md` through the Shields.io YouTube badge.
- YouTube milestone countdown is implemented through `images/youtube-countdown.svg`.
- The countdown refreshes daily through `.github/workflows/update-youtube-countdown.yml`.
- Profile views are already live through Komarev.
- GitHub follower count is live through Shields.io.

Assessment:

- A real "countdown to 100K YouTube subscribers" is now possible through the scheduled GitHub Action. Without a `YOUTUBE_API_KEY` secret it uses Shields.io's JSON response, which is rounded and therefore approximate. With `YOUTUBE_API_KEY`, the same script switches to exact YouTube Data API statistics.
- LinkedIn and X follower counters are possible only with API-backed automation. Unauthenticated public scraping is brittle and likely to break.
- YouTube is the cleanest first version and is now implemented. X can expose user `public_metrics` through its API, but it requires a bearer token. LinkedIn follower stats usually require a LinkedIn app and approved permissions, so it is the highest-friction option.

Recommended implementation:

- Optional: add `YOUTUBE_API_KEY` as a GitHub repo secret for exact subscriber counts instead of rounded Shields.io counts.
- Optional: run the `Update YouTube Countdown` workflow manually after adding the secret.

Suggested order:

- Newsletter/Substack milestone if a reliable export or API source is available.
- X follower count if an API bearer token is available.
- LinkedIn follower count only if the official API permissions are already available.

## Profile Maintenance

- Keep pinned repositories managed directly in the GitHub profile settings.
