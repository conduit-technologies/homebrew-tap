# Homebrew Tap for Conduit Technologies

Homebrew formulae for [conduitAI](https://conduitai.app) tools.

## Install

```bash
brew tap conduit-technologies/tap
brew install conduitai
```

## Usage

```bash
# Authenticate
conduitai auth login

# Search the catalog
conduitai search "code review"

# Install an MCP server into Claude Code
conduitai install mcp-server-github

# Install a skill
conduitai install commit-skill

# List installed assets
conduitai list

# Sync with your conduitAI account
conduitai sync

# Update an installed asset
conduitai update mcp-server-github

# Uninstall
conduitai uninstall mcp-server-github
```

## Update

```bash
brew upgrade conduitai
```

## Available Formulae

| Formula | Description | Version |
|---------|-------------|---------|
| `conduitai` | CLI for searching, installing, and managing AI tools | 0.6.0 |

## Alternative Install (npm)

```bash
npm install -g @conduitai-app/cli
```

## Links

- [conduitAI](https://conduitai.app) - AI tool marketplace
- [CLI Documentation](https://conduitai.app/docs/cli)
- [GitHub](https://github.com/akbaraziz/conduitai-bolt/tree/main/packages/cli)

## macCurrent cask pilot

The proposed installation command, available after the pilot is merged:

```sh
brew install --cask conduit-technologies/tap/maccurrent
```

This installs the official Universal macCurrent app for Apple Silicon and Intel
Macs on macOS 15 or later. It adds no dependency on the conduitAI formula.
The pilot currently tracks the published release, including its published RC
labeling; it does not turn an RC into a production release.

macCurrent keeps its Sparkle self-updater. The cask declares `auto_updates true`,
so normal bulk Brew upgrades skip it; users can explicitly request a Brew upgrade.
Do not use `--greedy` as a substitute for verifying the installed version, and
never force an older cask over an app that Sparkle has already updated.

Ordinary `brew uninstall --cask maccurrent` removes the application and preserves
its saved data. `--zap` additionally removes the listed preferences, cache and
application support, including inventory/history; use it only for an intentional
reset. It does not delete custom backup folders or shared third-party files.

After a successful official release has been publicly verified, save its manifest
with `curl --fail --output release.json
https://downloads.maccurrent.com/releases/direct/latest.json`, run
`python3 scripts/update-maccurrent-cask.py release.json`, inspect the version and
checksum diff, and submit it through the pilot checks. Do not commit release.json.
The updater rejects mutable download aliases, foreign hosts and expiring builds.
Sparkle livecheck provides release discovery. No credentials or signing keys are
needed in this tap.

The pilot checks installation, reinstall and ordinary uninstall on native hosted
Intel macOS 15. Local Apple Silicon macOS 27 evidence is recorded in the app PR.
A real cross-version Sparkle/Brew upgrade must be qualified before claiming that
lifecycle verified; installation checks alone do not establish it.
