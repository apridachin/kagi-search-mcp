# Kagi MCP server

MCP server that allows to search web using Kagi API

<a href="https://glama.ai/mcp/servers/rl6yu8g58l"><img width="380" height="200" src="https://glama.ai/mcp/servers/rl6yu8g58l/badge" alt="Kagi Server MCP server" /></a>

## Components

### Resources

The server implements calls of [API methods](https://help.kagi.com/kagi/api/overview.html):
- fastgpt
- enrich/web
- enrich/news

### Prompts

The server provides doesn't provide any prompts:

### Tools

The server implements several tools:
- ask_fastgpt to search web and find an answer
- enrich_web to enrich model context with web content
- enrich_news to enrich model context with latest news

## Configuration

## Quickstart

### Install

#### Claude Desktop

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`

<details>
  <summary>Development/Unpublished Servers Configuration</summary>
  ```
  "mcpServers": {
    "kagi-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "path_to_project",
        "run",
        "kagi-mcp"
      ],
      "env": {
        "KAGI_API_KEY": "YOUR API KEY"
      }
    }
  }
  ```
</details>

## Development

### Building and Publishing

To prepare the package for distribution:

1. Sync dependencies and update lockfile:
```bash
uv sync
```

2. Build package distributions:
```bash
uv build
```

This will create source and wheel distributions in the `dist/` directory.

3. Publish to PyPI:
```bash
uv publish
```

Note: You'll need to set PyPI credentials via environment variables or command flags:
- Token: `--token` or `UV_PUBLISH_TOKEN`
- Or username/password: `--username`/`UV_PUBLISH_USERNAME` and `--password`/`UV_PUBLISH_PASSWORD`

### Debugging

```bash
npx @modelcontextprotocol/inspector uv --directory path_to_project run kagi-mcp
```
