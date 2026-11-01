import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('update_cask', Path(__file__).with_name('update-maccurrent-cask.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class ManifestTests(unittest.TestCase):
    def manifest(self):
        return {'channel': 'direct', 'version': '1.2.0.68', 'betaExpiresAt': None,
                'artifacts': {'dmg': {'url': 'https://downloads.maccurrent.com/releases/direct/1.2.0.68/macCurrent-1.2.0.68.dmg', 'sha256': 'a' * 64}}}

    def test_exact_published_version_and_checksum(self):
        result = module.update(self.manifest(), '  version "1.0.0"\n  sha256 "old"\n')
        self.assertIn('version "1.2.0.68"', result)
        self.assertIn('sha256 "' + 'a' * 64 + '"', result)

    def test_rejects_mutable_url_foreign_host_and_invalid_checksum(self):
        for field, value in [('url', 'https://downloads.maccurrent.com/releases/direct/latest/macCurrent.dmg'), ('url', 'https://example.com/app.dmg'), ('sha256', ':no_check')]:
            with self.subTest(field=field, value=value):
                manifest = self.manifest()
                manifest['artifacts']['dmg'][field] = value
                with self.assertRaises(ValueError): module.update(manifest, '  version "1"\n  sha256 "x"\n')

    def test_rejects_expiring_or_unpublished_channels(self):
        for field, value in [('channel', 'beta'), ('betaExpiresAt', '2026-12-01'), ('version', '../latest')]:
            manifest = self.manifest(); manifest[field] = value
            with self.assertRaises(ValueError): module.update(manifest, '')

if __name__ == '__main__': unittest.main()
