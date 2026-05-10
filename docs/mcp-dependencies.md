# Companion MCP Dependencies

Data360 Beast installs the skill pack and public operating docs. It does not
vendor or auto-start companion MCP servers because those services have their
own runtimes, caches, credentials, and release cycles. Agents that need
official Salesforce docs or live Data 360 org operations should install these
MCP servers next.

## Direct URLs

| Server | Direct URL | Suggested Local Path | Purpose |
| --- | --- | --- | --- |
| `sf-docs` | https://github.com/kvirtue123/sf-docs-mcp | `$HOME/.codex/mcp-servers/sf-docs-mcp` | Fetch public `help.salesforce.com` and `developer.salesforce.com` pages as clean Markdown. |
| `data360` | https://github.com/forcedotcom/d360-mcp-server | `$HOME/.codex/mcp-servers/d360-mcp-server` | Expose Salesforce Data 360 Connect API operations through `search`, `payload_examples`, and `execute`. |

Note: `https://github.com/kvirtue/sf-docs-mcp` currently redirects to
`https://github.com/kvirtue123/sf-docs-mcp`; use the canonical `kvirtue123`
URL in install docs and automation.

## Install `sf-docs`

Requirements: Git, Node 18-24, npm. Node 20 or 22 LTS is recommended. Install
Chromium after dependencies so developer.salesforce.com extraction works.

```bash
mkdir -p "$HOME/.codex/mcp-servers"
git clone https://github.com/kvirtue123/sf-docs-mcp.git "$HOME/.codex/mcp-servers/sf-docs-mcp"
cd "$HOME/.codex/mcp-servers/sf-docs-mcp"
npm install
npm run build
npx playwright install chromium
```

MCP client snippet:

```json
{
  "mcpServers": {
    "sf-docs": {
      "command": "node",
      "args": [
        "/absolute/path/to/.codex/mcp-servers/sf-docs-mcp/dist/mcp-server.js"
      ],
      "env": {
        "SF_DOCS_CACHE_DB": "/absolute/path/to/.codex/mcp-servers/sf-docs-mcp/sf-docs-cache.db"
      }
    }
  }
}
```

Tools exposed:

- `scrape_sf_docs`: fetch one Salesforce Help or Developer docs URL.
- `analyze_page_structure`: diagnose Developer docs pages that scrape empty.

## Install `data360`

Requirements: Git, Java 17+, Maven 3.9+, and a Salesforce org with Data 360
Connect API access. The server is developer preview and should run through
stdio, not as a public network service.

```bash
mkdir -p "$HOME/.codex/mcp-servers"
git clone https://github.com/forcedotcom/d360-mcp-server.git "$HOME/.codex/mcp-servers/d360-mcp-server"
cd "$HOME/.codex/mcp-servers/d360-mcp-server"
mvn clean package -DskipTests
```

Preferred MCP client snippet for refreshable client-credentials auth:

```json
{
  "mcpServers": {
    "data360": {
      "command": "java",
      "args": [
        "-jar",
        "/absolute/path/to/.codex/mcp-servers/d360-mcp-server/target/data360-mcp-server-1.0.0.jar"
      ],
      "env": {
        "DATA360_CLIENT_ID": "your_client_id",
        "DATA360_CLIENT_SECRET": "your_client_secret",
        "DATA360_AUTH_FLOW": "client_credentials",
        "DATA360_LOGIN_URL": "https://login.salesforce.com",
        "DATA360_API_VERSION": "66.0"
      }
    }
  }
}
```

Fast local proof snippet for an existing `sf` CLI session:

```json
{
  "mcpServers": {
    "data360": {
      "command": "java",
      "args": [
        "-jar",
        "/absolute/path/to/.codex/mcp-servers/d360-mcp-server/target/data360-mcp-server-1.0.0.jar"
      ],
      "env": {
        "DATA360_INSTANCE_URL": "https://your-instance.my.salesforce.com",
        "DATA360_ACCESS_TOKEN": "YOUR_SHORT_LIVED_TOKEN"
      }
    }
  }
}
```

The Data 360 MCP exposes three facade tools:

- `search`: discover Data 360 tool families by intent.
- `payload_examples`: fetch expected payload shapes.
- `execute`: run an underlying Data 360 tool by name.

Use the normal loop: `search -> payload_examples -> execute`.

## Agent Install Checklist

After installing `architect-bertie/data360beast`, an agent should check:

1. Is `sf-docs` available? If not, install it from the URL above when official
   Salesforce docs are needed.
2. Is `data360` available? If not, install it from the URL above when live Data
   360 org operations are authorized.
3. Are credentials stored only in local MCP client config or environment
   variables? Never commit tokens, client secrets, caches, org metadata, or
   customer data.
4. If either MCP server is unavailable, continue with OpenAPI, official docs
   fetched through approved browser/web tools, and label live validation as
   unavailable.
