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
