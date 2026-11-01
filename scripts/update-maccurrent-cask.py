"""Update the cask from a verified, published direct-release manifest.

Fetch with curl --fail https://downloads.maccurrent.com/releases/direct/latest.json,
then pass the saved manifest path. This never builds or republishes an artifact.
"""
import json
from pathlib import Path
import re
import sys


def update(manifest, cask):
    version = manifest['version']
    if manifest.get('channel') != 'direct' or not re.fullmatch(r'\d+(?:\.\d+){2,3}', version):
        raise ValueError('Expected a published direct release with a numeric version')
    artifact = manifest['artifacts']['dmg']
    expected = f'https://downloads.maccurrent.com/releases/direct/{version}/macCurrent-{version}.dmg'
    if artifact['url'] != expected or not re.fullmatch(r'[a-f0-9]{64}', artifact['sha256']):
        raise ValueError('Expected a versioned official artifact and exact SHA-256')
    if manifest.get('betaExpiresAt') is not None:
        raise ValueError('Expiring releases require manual review')
    text, count = re.subn(r'^  version "[^"]+"$', f'  version "{version}"', cask, count=1, flags=re.M)
    if count != 1:
        raise ValueError('Missing cask version')
    text, count = re.subn(r'^  sha256 "[^"]+"$', f'  sha256 "{artifact["sha256"]}"', text, count=1, flags=re.M)
    if count != 1:
        raise ValueError('Missing cask checksum')
    return text


if __name__ == '__main__':
    path = Path(__file__).resolve().parents[1] / 'Casks/maccurrent.rb'
    path.write_text(update(json.loads(Path(sys.argv[1]).read_text()), path.read_text()))
