import html
import json
import os
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path


CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID", "UCUzGQrN-lyyc0BWTYoJM_Sg")
CHANNEL_TITLE = os.getenv("YOUTUBE_CHANNEL_TITLE", "What's AI")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "louisfb01")
GOAL = int(os.getenv("YOUTUBE_SUBSCRIBER_GOAL", "100000"))
COUNTDOWN_OUTPUT = Path("images/youtube-countdown.svg")
BUTTON_OUTPUT = Path("images/youtube.svg")
GITHUB_FOLLOWERS_OUTPUT = Path("images/github-followers.svg")
README = Path("README.md")
LATEST_VIDEO_START = "<!-- LATEST_YOUTUBE_VIDEO:START -->"
LATEST_VIDEO_END = "<!-- LATEST_YOUTUBE_VIDEO:END -->"


@dataclass(frozen=True)
class ChannelStats:
    subscribers: int
    source: str
    exact: bool
    uploads_playlist_id: str | None = None


@dataclass(frozen=True)
class LatestVideo:
    title: str
    video_id: str
    url: str
    thumbnail_url: str
    published_at: str | None = None


def fetch_json(url: str, headers: dict[str, str] | None = None) -> dict:
    request_headers = {"User-Agent": "louisfb01-profile-readme/1.0"}
    if headers:
        request_headers.update(headers)

    request = urllib.request.Request(
        url,
        headers=request_headers,
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def build_url(base_url: str, params: dict[str, str | int]) -> str:
    return f"{base_url}?{urllib.parse.urlencode(params)}"


def parse_compact_count(value: str) -> int:
    cleaned = value.strip().replace(",", "").replace("+", "").lower()
    match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)([km]?)", cleaned)
    if not match:
        raise ValueError(f"Cannot parse subscriber count: {value!r}")

    number = float(match.group(1))
    suffix = match.group(2)
    multiplier = {"": 1, "k": 1_000, "m": 1_000_000}[suffix]
    return int(number * multiplier)


def fetch_channel_stats() -> ChannelStats:
    api_key = os.getenv("YOUTUBE_API_KEY")
    if api_key:
        url = build_url(
            "https://www.googleapis.com/youtube/v3/channels",
            {
                "part": "statistics,contentDetails",
                "id": CHANNEL_ID,
                "key": api_key,
            },
        )
        data = fetch_json(url)
        items = data.get("items", [])
        if not items:
            raise RuntimeError("YouTube API returned no channel items.")

        channel = items[0]
        count = int(channel["statistics"]["subscriberCount"])
        uploads_playlist_id = channel.get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads")
        return ChannelStats(count, "YouTube API", True, uploads_playlist_id)

    url = build_url(
        f"https://img.shields.io/youtube/channel/subscribers/{CHANNEL_ID}.json",
        {"label": "YouTube subscribers"},
    )
    data = fetch_json(url)
    return ChannelStats(parse_compact_count(data["message"]), "Shields.io", False)


def best_thumbnail(thumbnails: dict) -> str | None:
    for key in ("maxres", "standard", "high", "medium", "default"):
        thumbnail = thumbnails.get(key)
        if thumbnail and thumbnail.get("url"):
            return thumbnail["url"]
    return None


def fetch_latest_video_from_api(api_key: str, uploads_playlist_id: str) -> LatestVideo:
    url = build_url(
        "https://www.googleapis.com/youtube/v3/playlistItems",
        {
            "part": "snippet,contentDetails",
            "playlistId": uploads_playlist_id,
            "maxResults": 1,
            "key": api_key,
        },
    )
    data = fetch_json(url)
    items = data.get("items", [])
    if not items:
        raise RuntimeError("YouTube API returned no playlist items.")

    item = items[0]
    snippet = item["snippet"]
    video_id = (
        snippet.get("resourceId", {}).get("videoId")
        or item.get("contentDetails", {}).get("videoId")
    )
    if not video_id:
        raise RuntimeError("YouTube API returned a playlist item without a video ID.")

    thumbnail_url = best_thumbnail(snippet.get("thumbnails", {}))
    if not thumbnail_url:
        thumbnail_url = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"

    return LatestVideo(
        title=snippet["title"],
        video_id=video_id,
        url=f"https://www.youtube.com/watch?v={video_id}",
        thumbnail_url=thumbnail_url,
        published_at=snippet.get("publishedAt"),
    )


def fetch_latest_video_from_rss() -> LatestVideo:
    url = build_url(
        "https://www.youtube.com/feeds/videos.xml",
        {"channel_id": CHANNEL_ID},
    )
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "louisfb01-profile-readme/1.0"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        root = ET.fromstring(response.read())

    namespaces = {
        "atom": "http://www.w3.org/2005/Atom",
        "yt": "http://www.youtube.com/xml/schemas/2015",
        "media": "http://search.yahoo.com/mrss/",
    }
    entry = root.find("atom:entry", namespaces)
    if entry is None:
        raise RuntimeError("YouTube RSS feed returned no entries.")

    title = entry.findtext("atom:title", default="", namespaces=namespaces)
    video_id = entry.findtext("yt:videoId", default="", namespaces=namespaces)
    published_at = entry.findtext("atom:published", default="", namespaces=namespaces) or None
    link = entry.find("atom:link", namespaces)
    media_group = entry.find("media:group", namespaces)
    thumbnail = media_group.find("media:thumbnail", namespaces) if media_group is not None else None
    thumbnail_url = thumbnail.attrib.get("url") if thumbnail is not None else None

    if not video_id:
        raise RuntimeError("YouTube RSS feed returned an entry without a video ID.")

    return LatestVideo(
        title=title,
        video_id=video_id,
        url=link.attrib.get("href", f"https://www.youtube.com/watch?v={video_id}") if link is not None else f"https://www.youtube.com/watch?v={video_id}",
        thumbnail_url=thumbnail_url or f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
        published_at=published_at,
    )


def fetch_latest_video(stats: ChannelStats) -> LatestVideo:
    api_key = os.getenv("YOUTUBE_API_KEY")
    if api_key and stats.uploads_playlist_id:
        return fetch_latest_video_from_api(api_key, stats.uploads_playlist_id)

    return fetch_latest_video_from_rss()


def fetch_github_followers() -> int:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    username = urllib.parse.quote(GITHUB_USERNAME, safe="")
    data = fetch_json(f"https://api.github.com/users/{username}", headers=headers)
    return int(data["followers"])


def format_count(value: int) -> str:
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M".replace(".0M", "M")
    if value >= 1_000:
        return f"{value / 1_000:.1f}K".replace(".0K", "K")
    return str(value)


def text_width(text: str, char_width: int = 7, padding: int = 22) -> int:
    return max(40, len(text) * char_width + padding)


def build_countdown_svg(subscribers: int, source: str, exact: bool) -> str:
    label = f"YouTube to {format_count(GOAL)}"
    message = f"{subscribers:,}" if exact else format_count(subscribers)

    left_width = text_width(label)
    right_width = text_width(message)
    width = left_width + right_width
    label_x = left_width / 2
    message_x = left_width + right_width / 2
    title = f"{label}: {message} subscribers (source: {source})"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="20" role="img" aria-label="{html.escape(title)}">
  <title>{html.escape(title)}</title>
  <g shape-rendering="crispEdges">
    <rect width="{left_width}" height="20" fill="#555"/>
    <rect x="{left_width}" width="{right_width}" height="20" fill="#ff0000"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" text-rendering="geometricPrecision" font-size="110">
    <text x="{label_x * 10:.0f}" y="140" transform="scale(.1)" textLength="{(left_width - 16) * 10}">{html.escape(label)}</text>
    <text x="{message_x * 10:.0f}" y="140" transform="scale(.1)" textLength="{(right_width - 16) * 10}">{html.escape(message)}</text>
  </g>
</svg>
"""


def build_badge_svg(label: str, message: str, color: str, source: str) -> str:
    left_width = text_width(label)
    right_width = text_width(message)
    width = left_width + right_width
    label_x = left_width / 2
    message_x = left_width + right_width / 2
    title = f"{label}: {message} (source: {source})"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="20" role="img" aria-label="{html.escape(title)}">
  <title>{html.escape(title)}</title>
  <g shape-rendering="crispEdges">
    <rect width="{left_width}" height="20" fill="#555"/>
    <rect x="{left_width}" width="{right_width}" height="20" fill="{html.escape(color)}"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" text-rendering="geometricPrecision" font-size="110">
    <text x="{label_x * 10:.0f}" y="140" transform="scale(.1)" textLength="{(left_width - 16) * 10}">{html.escape(label)}</text>
    <text x="{message_x * 10:.0f}" y="140" transform="scale(.1)" textLength="{(right_width - 16) * 10}">{html.escape(message)}</text>
  </g>
</svg>
"""


def build_button_svg(subscribers: int, source: str, exact: bool) -> str:
    count = f"{subscribers:,}" if exact else format_count(subscribers)
    subtitle = f"{count} subscribers"
    title = f"YouTube - {CHANNEL_TITLE}: {subtitle} (source: {source})"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="188" height="34" viewBox="0 0 188 34" role="img" aria-label="{html.escape(title)}">
  <title>{html.escape(title)}</title>
  <rect width="188" height="34" rx="7" fill="#0f172a"/>
  <rect x="8" y="7" width="31" height="20" rx="6" fill="#ff0000"/>
  <path d="M21 12v10l9-5z" fill="#ffffff"/>
  <text x="49" y="15" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="11" font-weight="700">{html.escape(f"YouTube: {CHANNEL_TITLE}")}</text>
  <text x="49" y="26" fill="#cbd5e1" font-family="Arial, Helvetica, sans-serif" font-size="9">{html.escape(subtitle)}</text>
</svg>
"""


def build_latest_video_block(video: LatestVideo) -> str:
    title = html.escape(video.title)
    alt = html.escape(f"Latest {CHANNEL_TITLE} video: {video.title}", quote=True)
    image_src = html.escape(video.thumbnail_url, quote=True)
    video_url = html.escape(video.url, quote=True)

    return f"""{LATEST_VIDEO_START}
### What I'm Up To?

<p align="center">
  <strong>Watch my most recent video:</strong> <a href="{video_url}">{title}</a>
</p>

<p align="center">
  <a href="{video_url}">
    <img src="{image_src}" alt="{alt}" width="560">
  </a>
</p>

<p align="center">
  <a href="{video_url}"><strong>Watch on YouTube</strong></a>
</p>
{LATEST_VIDEO_END}"""


def update_latest_video_block(video: LatestVideo) -> None:
    readme = README.read_text(encoding="utf-8")
    block = build_latest_video_block(video)

    if LATEST_VIDEO_START in readme and LATEST_VIDEO_END in readme:
        pattern = re.compile(
            rf"{re.escape(LATEST_VIDEO_START)}.*?{re.escape(LATEST_VIDEO_END)}",
            re.DOTALL,
        )
        updated = pattern.sub(block, readme, count=1)
    else:
        heading = "## Education & Towards AI"
        updated = readme.replace(heading, f"{heading}\n\n{block}", 1)

    README.write_text(updated, encoding="utf-8")


def main() -> None:
    stats = fetch_channel_stats()
    latest_video = fetch_latest_video(stats)
    github_followers = fetch_github_followers()
    COUNTDOWN_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    COUNTDOWN_OUTPUT.write_text(
        build_countdown_svg(stats.subscribers, stats.source, stats.exact),
        encoding="utf-8",
    )
    BUTTON_OUTPUT.write_text(
        build_button_svg(stats.subscribers, stats.source, stats.exact),
        encoding="utf-8",
    )
    GITHUB_FOLLOWERS_OUTPUT.write_text(
        build_badge_svg("GitHub followers", f"{github_followers:,}", "#0A7FDB", "GitHub API"),
        encoding="utf-8",
    )
    update_latest_video_block(latest_video)
    print(
        f"Generated YouTube README assets from {stats.source}: "
        f"{stats.subscribers} subscribers, latest video {latest_video.video_id}; "
        f"GitHub followers: {github_followers}."
    )


if __name__ == "__main__":
    main()
