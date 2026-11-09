# Process Context MCP

An [MCP](https://modelcontextprotocol.io) server that gives AI agents structured context about business processes: which processes exist, their ordered steps, and the role responsible for each step.

Agents that know *how work is supposed to happen* can route tasks to the right owner, explain a procedure step by step, and check whether an action fits the process before taking it.

## Tools

| Tool | Description |
| --- | --- |
| `list_processes` | Lists all processes with their ID, name and owner. |
| `get_process` | Returns a process with its ordered steps and the responsible role for each. Unknown IDs return an error listing the valid IDs, so the agent can correct itself. |

Both tools return typed, structured output (Pydantic models), so clients receive a JSON schema for every result.

## Installation

Requires Python 3.10+.

```bash
git clone https://github.com/MeshaalAlharthy/process-context-mcp.git
cd process-context-mcp
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

The server communicates over stdio, so MCP clients launch it directly.

**Claude Desktop** — add this to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "process-context": {
      "command": "/absolute/path/to/process-context-mcp/.venv/bin/process-context-mcp"
    }
  }
}
```

## Process catalog

The server includes a default catalog of three data-protection processes in `src/process_context_mcp/data/processes.json`. To load your own, point `PROCESS_CATALOG_PATH` at a JSON file with the same structure:

```json
[
  {
    "id": "access-provisioning",
    "name": "User Access Provisioning",
    "description": "Grants employees access to systems and data based on their role and clearance.",
    "owner": "IT Security Manager",
    "steps": [
      {"order": 1, "name": "Submit access request", "role": "Employee"},
      {"order": 2, "name": "Approve business need", "role": "Line Manager"}
    ]
  }
]
```

The catalog is validated on startup, so a malformed file fails fast with a clear error.

## Development

```bash
pip install -e ".[dev]"
pytest
```

Tests connect an in-process MCP client to the server and exercise every tool, including the error path.

## License

MIT
