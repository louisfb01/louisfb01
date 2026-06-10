# Next Steps

## Live Counters And Milestone Countdown

Status:

- YouTube subscriber count is already live in `README.md` through the Shields.io YouTube badge.
- Profile views are already live through Komarev.
- GitHub follower count is shown as a stable static badge. The live Shields.io GitHub follower endpoint returns data, but it rendered inconsistently on the profile.

Assessment:

- A real "countdown to 100K YouTube subscribers" is possible, but not as plain Markdown. GitHub README files do not run JavaScript or arithmetic, so the countdown needs an external SVG/badge endpoint or a scheduled GitHub Action that updates generated text/images.
- LinkedIn and X follower counters are possible only with API-backed automation. Unauthenticated public scraping is brittle and likely to break.
- YouTube is the cleanest first version because the YouTube Data API exposes channel statistics. X can expose user `public_metrics` through its API, but it requires a bearer token. LinkedIn follower stats usually require a LinkedIn app and approved permissions, so it is the highest-friction option.

Recommended implementation:

- Create a small generated badge, for example: `YouTube: 29,812 until 100K`.
- Use a scheduled GitHub Action to refresh it once per day.
- Store API credentials as GitHub repo secrets, starting with `YOUTUBE_API_KEY`.
- Generate either `images/youtube-countdown.svg` or a tiny `metrics.json` consumed by a Shields.io dynamic badge.
- Add the countdown badge beside the current YouTube subscriber badge once the script is stable.

Suggested order:

- YouTube milestone countdown to 100K subscribers.
- Newsletter/substack milestone if a reliable export or API source is available.
- X follower count if an API bearer token is available.
- LinkedIn follower count only if the official API permissions are already available.

## Profile Maintenance

- Keep pinned repositories managed directly in the GitHub profile settings.
