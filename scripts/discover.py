#!/usr/bin/env python3
import json, os, urllib.request
from datetime import datetime, timezone

repos = [
    'awesome-selfhosted/awesome-selfhosted',
    'jellyfin/jellyfin',
    'immich-app/immich',
    'syncthing/syncthing',
    'dani-garcia/vaultwarden',
]
items = []
for repo in repos:
    req = urllib.request.Request(f'https://api.github.com/repos/{repo}/releases/latest', headers={'Accept':'application/vnd.github+json','User-Agent':'isoul-watchlist'})
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            release = json.load(response)
        items.append({'repository': repo, 'release': release.get('tag_name'), 'released': release.get('published_at'), 'url': release.get('html_url'), 'status': 'review'})
    except Exception as exc:
        items.append({'repository': repo, 'status': 'check failed', 'error': str(exc)})

os.makedirs('data', exist_ok=True)
with open('data/candidates.json', 'w', encoding='utf-8') as output:
    json.dump({'generated': datetime.now(timezone.utc).isoformat(), 'items': items}, output, indent=2)
    output.write('\n')
