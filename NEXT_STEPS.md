# Next Steps

## Live Counters And Milestone Countdown

Status:

- The standalone YouTube subscriber badge was removed to avoid duplication.
- YouTube milestone badge is implemented through `images/youtube-countdown.svg`; it shows the current subscriber count against the 100K goal.
- The countdown refreshes daily through `.github/workflows/update-youtube-countdown.yml`.
- Profile views are already live through Komarev.
- GitHub follower count is live through Shields.io.

Assessment:

- A real "YouTube to 100K" badge is now implemented through the scheduled GitHub Action. Without a `YOUTUBE_API_KEY` secret it uses Shields.io's JSON response, which is rounded and therefore approximate. With `YOUTUBE_API_KEY`, the same script switches to exact YouTube Data API statistics.
- X follower counts are possible with API-backed automation only. X's user lookup endpoint requires bearer-token authorization and exposes counts through `user.fields=public_metrics`; the public Shields X followers badge returns an empty value for `Whats_AI`, so there is no reliable no-token badge to add. Whether it is free depends on whether the current X developer plan grants user lookup access for your app; if it does, the repo only needs an `X_BEARER_TOKEN` secret.
- LinkedIn follower counts are possible for organization pages through official LinkedIn APIs, but not as a public no-token badge. Organization follower statistics require `rw_organization_admin`; Microsoft also notes total follower count should be retrieved via the `networkSizes` API under Organization Lookup. This can be free in the sense that there is no repo-side hosting cost, but it requires LinkedIn developer access, an app, an access token, an organization URN, and approved permissions. For a personal LinkedIn profile, there is no clean official public follower-count badge.
- Newsletter/Substack counters need either a reliable private export/API source or a manually maintained badge. I did not find a stable official public subscriber-count endpoint suitable for a GitHub README automation.
- YouTube is the cleanest first version and is implemented. X and LinkedIn are technically feasible after adding credentials as repo secrets, but they are not guaranteed to be free because access depends on each platform's current developer/API permissions. Substack/newsletter is feasible only if we choose a trusted source for the count.

Recommended implementation:

- Optional: add `YOUTUBE_API_KEY` as a GitHub repo secret for exact subscriber counts instead of rounded Shields.io counts.
- Optional: run the `Update YouTube Countdown` workflow manually after adding the secret.
- Optional: add `X_BEARER_TOKEN` to generate an X follower badge through the official X API.
- Optional: add `LINKEDIN_ACCESS_TOKEN` and `LINKEDIN_ORGANIZATION_URN` to generate an organization follower badge through LinkedIn's official API.
- Optional: add a newsletter count source, such as a private export committed by automation, before adding a newsletter milestone badge.

Suggested order:

- X follower badge after `X_BEARER_TOKEN` is available.
- LinkedIn organization follower badge after `LINKEDIN_ACCESS_TOKEN` and `LINKEDIN_ORGANIZATION_URN` are available.
- Newsletter/Substack milestone after a reliable export or API source is available.

## Profile Maintenance

- Keep pinned repositories managed directly in the GitHub profile settings.
