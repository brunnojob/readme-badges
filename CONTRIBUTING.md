# Contributing

Add or correct badges in `badges.json`, then run `python scripts/build.py`. Keep labels unique and colors as six hexadecimal characters. Use official Simple Icons slugs when available; text-only badges are welcome for field protocols and project states.

Run `python -m unittest discover -s tests` and `python scripts/build.py --check` before opening a pull request. Include the category, the reason for the change and the rendered badge URL. Do not add claims of certification, affiliation or endorsements without evidence.

Please keep generated catalog changes in the same pull request as the data changes. Do not edit sponsor identities manually; that section is synchronized from public GitHub sponsorships.
