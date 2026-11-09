"""MCP server exposing business process context to AI agents."""

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

from process_context_mcp.catalog import Process, ProcessCatalog, ProcessSummary

catalog = ProcessCatalog.load()

mcp = MCPServer(
    "process-context",
    instructions=(
        "Provides business process context: the processes an organization runs, "
        "their steps, and the role responsible for each step. Call list_processes "
        "first to discover valid process IDs."
    ),
)


@mcp.tool()
def list_processes() -> list[ProcessSummary]:
    """List all available business processes with their ID, name and owner."""
    return catalog.summaries()


@mcp.tool()
def get_process(process_id: str) -> Process:
    """Return a business process with its ordered steps and the role responsible for each."""
    process = catalog.get(process_id)
    if process is None:
        raise ToolError(
            f"Unknown process '{process_id}'. Valid IDs: {', '.join(catalog.ids)}"
        )
    return process


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
