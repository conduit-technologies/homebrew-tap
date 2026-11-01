"""Explicit live qualification using genuine published macCurrent artifacts.

The regular macCurrent application must be stopped before starting. This runner
never launches either release into the customer's database. The native Sparkle
CLI installs into an isolated app directory; its SU/SPU preferences are restored.
"""
import argparse, hashlib, json, os, pathlib, platform, plistlib, re, shutil, subprocess, time

parser = argparse.ArgumentParser()
parser.add_argument('--brew', required=True)
parser.add_argument('--sparkle', required=True)
parser.add_argument('--preferences-helper', required=True)
parser.add_argument('--output', required=True)
parser.add_argument('--older-version', default='1.2.0.65')
parser.add_argument('--target-version', default='1.2.0.68')
args = parser.parse_args()
root = pathlib.Path(args.output).resolve()
root.mkdir(parents=True, exist_ok=False)
appdir = root / 'Applications'; appdir.mkdir()
app = appdir / 'macCurrent.app'
env = dict(os.environ, HOMEBREW_NO_AUTO_UPDATE='1', HOMEBREW_NO_ANALYTICS='1', HOMEBREW_NO_INSTALL_CLEANUP='1', HOMEBREW_NO_ENV_HINTS='1')
token = 'conduit-technologies/tap/maccurrent'
evidence = {'architecture': platform.machine(), 'osVersion': platform.mac_ver()[0], 'phases': [], 'result': 'failed'}

def run(argv, check=True, timeout=600):
    result = subprocess.run(list(map(str,argv)), env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    with (root/'commands.log').open('a') as log:
        log.write('$ '+ ' '.join(map(str,argv))+'\n'+result.stdout+result.stderr+'\n')
    if check and result.returncode:
        raise RuntimeError(f'{argv[0]} failed with {result.returncode}: {(result.stdout+result.stderr)[-1800:]}')
    return result

def brew(*arguments, check=True):
    return run([args.brew, *arguments], check=check)

def manifest(version):
    if not re.fullmatch(r'\d+(?:\.\d+){2,3}', version): raise ValueError('Invalid release version')
    destination=root/(version+'.json')
    run(['/usr/bin/curl','--fail','--silent','--show-error','--location','--proto','=https',
         f'https://downloads.maccurrent.com/releases/direct/{version}/latest.json','-o',destination])
    data=json.loads(destination.read_text())
    assert data['version']==version and data['channel']=='direct'
    artifact=data['artifacts']['dmg']
    assert artifact['url']==f'https://downloads.maccurrent.com/releases/direct/{version}/macCurrent-{version}.dmg'
    assert re.fullmatch('[a-f0-9]{64}',artifact['sha256'])
    return data

def identity(expected):
    info=plistlib.loads((app/'Contents/Info.plist').read_bytes())
    assert info['CFBundleIdentifier']=='com.conduit-technologies.macCurrent'
    assert info['CFBundleShortVersionString']==expected, (info['CFBundleShortVersionString'],expected)
    assert info['LSMinimumSystemVersion']=='15.0'
    run(['/usr/bin/codesign','--verify','--deep','--strict',app])
    signed=run(['/usr/bin/codesign','-dv','--verbose=4',app])
    signature=signed.stdout+signed.stderr
    assert 'TeamIdentifier=D3B973F339' in signature
    run(['/usr/sbin/spctl','--assess','--type','execute',app])
    run(['/usr/bin/lipo',app/'Contents/MacOS/macCurrent','-verify_arch',platform.machine()])
    return {'version':info['CFBundleShortVersionString'],'build':info['CFBundleVersion'],
            'binarySHA256':hashlib.sha256((app/'Contents/MacOS/macCurrent').read_bytes()).hexdigest()}

def record(name, version):
    evidence['phases'].append({'name':name,'result':'passed',**identity(version)})
    (root/'evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')

processes=run(['/bin/ps','-axo','comm']).stdout.splitlines()
for process in processes:
    process=process.strip()
    if not process.endswith('/macCurrent.app/Contents/MacOS/macCurrent'): continue
    info=pathlib.Path(process).parents[1]/'Info.plist'
    if info.exists() and plistlib.loads(info.read_bytes()).get('CFBundleIdentifier')=='com.conduit-technologies.macCurrent':
        raise RuntimeError('Quit the regular macCurrent app normally before qualification')
repo=pathlib.Path(brew('--repo','conduit-technologies/tap').stdout.strip())
recipe=repo/'Casks/maccurrent.rb'; original=recipe.read_text()
assert not json.loads(brew('info','--json=v2','--cask',token).stdout)['casks'][0].get('installed'), 'Use a prefix without an installed macCurrent cask'
older=manifest(args.older_version); target=manifest(args.target_version)
assert re.search(r'  version "'+re.escape(args.target_version)+'"',original)
assert target['artifacts']['dmg']['sha256'] in original

def select(data):
    text=re.sub(r'^  version "[^"]+"$', '  version "'+data['version']+'"',original,flags=re.M)
    text=re.sub(r'^  sha256 "[^"]+"$', '  sha256 "'+data['artifacts']['dmg']['sha256']+'"',text,flags=re.M)
    recipe.write_text(text)

def install(): brew('install','--cask','--appdir='+str(appdir),token)
def uninstall(): brew('uninstall','--cask',token); assert not app.exists()
backup=root/'private-sparkle-preferences.plist'
saved=False
try:
    # Native Homebrew cross-version upgrade.
    select(older); install(); record('install-genuine-older-release',args.older_version)
    shutil.copytree(app,root/'older-reference.app',symlinks=True)
    select(target); brew('upgrade','--cask',token); record('native-brew-upgrade',args.target_version)
    shutil.copytree(app,root/'target-reference.app',symlinks=True)
    uninstall()
    # Real Sparkle feed, download, EdDSA/publisher verification and replacement.
    select(older); install(); identity(args.older_version)
    run([args.preferences_helper,'save',backup]); saved=True
    run([args.sparkle,app,'--check-immediately','--grant-automatic-checks','--verbose'],timeout=900)
    for _ in range(60):
        if plistlib.loads((app/'Contents/Info.plist').read_bytes())['CFBundleShortVersionString']==args.target_version: break
        time.sleep(1)
    record('native-sparkle-upgrade',args.target_version)
    brew('upgrade','--cask',token); record('older-cask-does-not-downgrade-sparkle-release',args.target_version)
    select(target); brew('upgrade','--cask',token); record('brew-after-sparkle-upgrade',args.target_version)
    uninstall()
    # Adoption rejects different bytes and accepts the genuine current release.
    shutil.copytree(root/'older-reference.app',app,symlinks=True)
    rejected=brew('install','--cask','--adopt','--appdir='+str(appdir),token,check=False)
    assert rejected.returncode!=0, 'Older direct copy was unexpectedly adopted'
    record('reject-adoption-of-older-direct-copy',args.older_version)
    shutil.rmtree(app)  # Only this explicitly disposable fixture copy.
    shutil.copytree(root/'target-reference.app',app,symlinks=True)
    info_path=app/'Contents/Info.plist'
    altered=plistlib.loads(info_path.read_bytes())
    altered['CFBundleIdentifier']='invalid.qualification.signature'
    info_path.write_bytes(plistlib.dumps(altered))
    before=hashlib.sha256(info_path.read_bytes()).hexdigest()
    rejected=brew('install','--cask','--adopt','--appdir='+str(appdir),token,check=False)
    assert rejected.returncode!=0, 'A tampered direct copy was unexpectedly adopted'
    assert info_path.exists() and hashlib.sha256(info_path.read_bytes()).hexdigest()==before
    evidence['phases'].append({'name':'reject-tampered-direct-copy-without-changing-it','result':'passed'})
    shutil.rmtree(app)  # Only the intentionally altered fixture.
    shutil.copytree(root/'target-reference.app',app,symlinks=True)
    brew('install','--cask','--adopt','--appdir='+str(appdir),token)
    record('adopt-current-direct-copy',args.target_version)
    uninstall()
    evidence['result']='passed'
finally:
    recipe.write_text(original)
    if saved: run([args.preferences_helper,'restore',backup])
    (root/'evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
print(json.dumps(evidence,indent=2))
