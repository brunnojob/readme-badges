import argparse
import json
import re
from pathlib import Path
from urllib.parse import quote, urlencode

ROOT = Path(__file__).resolve().parents[1]


def badge_url(badge, style="for-the-badge"):
    label = badge["label"].replace("-", "--").replace("_", "__")
    query = {"style": style}
    if badge.get("logo"):
        query.update(logo=badge["logo"], logoColor="white")
    return "https://img.shields.io/badge/" + quote(label, safe="") + "-" + badge["color"] + "?" + urlencode(query)


def catalog(data):
    seen = set()
    parts = ["# Badge catalog", "", "Copy the Markdown next to a preview. These are labels for your README, not verified credentials or GitHub achievements.", ""]
    for group in data:
        parts.extend(["## " + group["category"], "", "| Preview | Copy Markdown |", "| --- | --- |"])
        for badge in group["badges"]:
            if badge["label"] in seen or not re.fullmatch(r"[A-Fa-f0-9]{6}", badge["color"]):
                raise ValueError("Duplicate badge or invalid color: " + badge["label"])
            seen.add(badge["label"])
            markdown = f'![{badge["label"]}]({badge_url(badge)})'
            parts.append(f"| {markdown} | `{markdown}` |")
        parts.append("")
    return "\n".join(parts) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Build the Markdown badge catalog from badges.json")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output = catalog(json.loads((ROOT / "badges.json").read_text()))
    target = ROOT / "CATALOG.md"
    if args.check:
        if not target.exists() or target.read_text() != output:
            raise SystemExit("CATALOG.md is out of date. Run python scripts/build.py")
        print("Catalog is up to date.")
    else:
        target.write_text(output)
        print("Built CATALOG.md")


if __name__ == "__main__":
    main()
