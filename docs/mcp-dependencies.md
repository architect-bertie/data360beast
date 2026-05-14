# Companion MCP Dependencies

Data360 Beast installs the skill pack and public operating docs. It does not
vendor or auto-start companion MCP servers because those services have their
own runtimes, caches, credentials, and release cycles. Agents that need
official Salesforce docs or live Data 360 org operations should install these
MCP servers next.

## Direct URLs

| Server | Direct URL | Suggested Local Path | Purpose |
| --- | --- | --- | --- |
| `sf-docs` | https://github.com/kvirtue123/sf-docs-mcp | `$HOME/.data360beast/mcp-servers/sf-docs-mcp` | Fetch public `help.salesforce.com` and `developer.salesforce.com` pages as clean Markdown. |
| `data360` | https://github.com/forcedotcom/d360-mcp-server | `$HOME/.data360beast/mcp-servers/d360-mcp-server` | Expose Salesforce Data 360 Connect API operations through `search`, `payload_examples`, and `execute`. |
| `datacloud-mcp-query` | https://github.com/forcedotcom/datacloud-mcp-query | `$HOME/.data360beast/mcp-servers/datacloud-mcp-query` | Optional query-plane accelerator for Query SQL, table listing, and table description. |

Note: `https://github.com/kvirtue/sf-docs-mcp` currently redirects to
`https://github.com/kvirtue123/sf-docs-mcp`; use the canonical `kvirtue123`
URL in install docs and automation.

## Install `sf-docs`

Requirements: Git, Node 18-24, npm. Node 20 or 22 LTS is recommended. Install
Chromium after dependencies so developer.salesforce.com extraction works.

```bash
export DATA360BEAST_MCP_ROOT="${DATA360BEAST_MCP_ROOT:-$HOME/.data360beast/mcp-servers}"
mkdir -p "$DATA360BEAST_MCP_ROOT"
git clone https://github.com/kvirtue123/sf-docs-mcp.git "$DATA360BEAST_MCP_ROOT/sf-docs-mcp"
cd "$DATA360BEAST_MCP_ROOT/sf-docs-mcp"
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
        "/absolute/path/to/.data360beast/mcp-servers/sf-docs-mcp/dist/mcp-server.js"
      ],
      "env": {
        "SF_DOCS_CACHE_DB": "/absolute/path/to/.data360beast/mcp-servers/sf-docs-mcp/sf-docs-cache.db"
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
export DATA360BEAST_MCP_ROOT="${DATA360BEAST_MCP_ROOT:-$HOME/.data360beast/mcp-servers}"
mkdir -p "$DATA360BEAST_MCP_ROOT"
git clone https://github.com/forcedotcom/d360-mcp-server.git "$DATA360BEAST_MCP_ROOT/d360-mcp-server"
cd "$DATA360BEAST_MCP_ROOT/d360-mcp-server"
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
        "/absolute/path/to/.data360beast/mcp-servers/d360-mcp-server/target/data360-mcp-server-1.0.0.jar"
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
        "/absolute/path/to/.data360beast/mcp-servers/d360-mcp-server/target/data360-mcp-server-1.0.0.jar"
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

## Optional `datacloud-mcp-query`

Requirements: Git, Python 3.11+, and a Salesforce org auth path supported by
the server. Use this server when the task is only retrieve-plane work: Query
SQL, list tables, or describe table metadata.

```bash
export DATA360BEAST_MCP_ROOT="${DATA360BEAST_MCP_ROOT:-$HOME/.data360beast/mcp-servers}"
mkdir -p "$DATA360BEAST_MCP_ROOT"
git clone https://github.com/forcedotcom/datacloud-mcp-query.git "$DATA360BEAST_MCP_ROOT/datacloud-mcp-query"
cd "$DATA360BEAST_MCP_ROOT/datacloud-mcp-query"
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

MCP client snippet for SF CLI auth:

```json
{
  "mcpServers": {
    "datacloud-query": {
      "command": "/absolute/path/to/python3",
      "args": [
        "/absolute/path/to/.data360beast/mcp-servers/datacloud-mcp-query/server.py"
      ],
      "env": {
        "SF_ORG_ALIAS": "my-datacloud-org"
      }
    }
  }
}
```

Decision note: treat `datacloud-mcp-query` as optional and query-specific. It
does not replace `d360-mcp-server` for broader Connect API operations such as
segments, activations, data actions, connector lifecycle, payload examples, or
search index work. See
[`docs/data360/mcp-tool-selection.md`](data360/mcp-tool-selection.md).

Readiness check:

```bash
python3 tools/mcp_readiness.py
```

## Agent Install Checklist

After installing `architect-bertie/data360beast`, an agent should check:

1. Is `sf-docs` available? If not, install it from the URL above when official
   Salesforce docs are needed.
2. Is `data360` available? If not, install it from the URL above when live Data
   360 org operations are authorized.
3. Is `datacloud-mcp-query` useful for this task? Install it only when the
   proof target is Query SQL, table listing, or table description.
4. Are credentials stored only in local MCP client config or environment
   variables? Never commit tokens, client secrets, caches, org metadata, or
   customer data.
5. If an MCP server is unavailable, continue with OpenAPI, official docs
   fetched through approved browser/web tools, and label live validation as
   unavailable.
