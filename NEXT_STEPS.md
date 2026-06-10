# Next Steps

## Live Counters And Milestone Countdown

Status:

- The standalone YouTube subscriber badge was removed to avoid duplication.
- YouTube milestone badge is implemented through `images/youtube-countdown.svg`; it shows the current subscriber count against the 100K goal.
- The countdown refreshes daily through `.github/workflows/update-youtube-countdown.yml`.
- Profile views are already live through Komarev.
- GitHub follower count is live through Shields.io.

## Free Exact YouTube Count

`YOUTUBE_API_KEY` should be free for this use case under the normal YouTube Data API quota.
I removed the X, LinkedIn, and newsletter counter ideas from this file because the reliable versions require platform credentials, approved API access, or unclear paid/gated developer plans.

Why:

- The badge uses `channels.list`, which costs 1 quota unit per request.
- Google gives YouTube Data API projects 10,000 quota units per day for most endpoints.
- The GitHub Action runs once per day, so exact counts should use about 1 quota unit per day.
- That leaves roughly 9,999 unused quota units per day for this project if this badge is the only thing using the API.

What to do:

- Open the [Google API Console credentials page](https://console.cloud.google.com/apis/credentials).
- Create or select a Google Cloud project.
- Enable the YouTube Data API v3.
- Create an API key.
- Restrict the key to the YouTube Data API v3 if Google offers that option.
- In GitHub, open `louisfb01/louisfb01` -> Settings -> Secrets and variables -> Actions.
- Add a repository secret named `YOUTUBE_API_KEY`.
- Paste the API key as the value.
- Go to Actions -> `Update YouTube Countdown` -> `Run workflow`.

References:

- [YouTube Data API quota costs](https://developers.google.com/youtube/v3/determine_quota_cost)
- [YouTube Data API credential setup](https://developers.google.com/youtube/registering_an_application)

## Profile Maintenance

- Keep pinned repositories managed directly in the GitHub profile settings.
