import html
import json
import os
import re
import urllib.request
from pathlib import Path


CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID", "UCUzGQrN-lyyc0BWTYoJM_Sg")
GOAL = int(os.getenv("YOUTUBE_SUBSCRIBER_GOAL", "100000"))
OUTPUT = Path("images/youtube-countdown.svg")


def fetch_json(url: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "louisfb01-profile-readme/1.0"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def parse_compact_count(value: str) -> int:
    cleaned = value.strip().replace(",", "").replace("+", "").lower()
    match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)([km]?)", cleaned)
    if not match:
        raise ValueError(f"Cannot parse subscriber count: {value!r}")

    number = float(match.group(1))
    suffix = match.group(2)
    multiplier = {"": 1, "k": 1_000, "m": 1_000_000}[suffix]
    return int(number * multiplier)


def fetch_subscribers() -> tuple[int, str]:
    api_key = os.getenv("YOUTUBE_API_KEY")
    if api_key:
        url = (
            "https://www.googleapis.com/youtube/v3/channels"
            f"?part=statistics&id={CHANNEL_ID}&key={api_key}"
        )
        data = fetch_json(url)
        items = data.get("items", [])
        if not items:
            raise RuntimeError("YouTube API returned no channel items.")

        count = int(items[0]["statistics"]["subscriberCount"])
        return count, "YouTube API"

    url = (
        "https://img.shields.io/youtube/channel/subscribers/"
        f"{CHANNEL_ID}.json?label=YouTube%20subscribers"
    )
    data = fetch_json(url)
    return parse_compact_count(data["message"]), "Shields.io"


def format_count(value: int) -> str:
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M".replace(".0M", "M")
    if value >= 1_000:
        return f"{value / 1_000:.1f}K".replace(".0K", "K")
    return str(value)


def text_width(text: str, char_width: int = 7, padding: int = 22) -> int:
    return max(40, len(text) * char_width + padding)


def build_svg(subscribers: int, source: str) -> str:
    label = f"YouTube to {format_count(GOAL)}"
    message = format_count(subscribers)

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


def main() -> None:
    subscribers, source = fetch_subscribers()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(build_svg(subscribers, source), encoding="utf-8")
    print(f"Generated {OUTPUT} from {source}: {subscribers} subscribers.")


if __name__ == "__main__":
    main()
