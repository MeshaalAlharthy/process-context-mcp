import pytest

from mcp import Client
from process_context_mcp.server import mcp


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_exposes_expected_tools():
    async with Client(mcp) as client:
        tools = await client.list_tools()
    assert {tool.name for tool in tools.tools} == {"list_processes", "get_process"}


@pytest.mark.anyio
async def test_list_processes_returns_catalog():
    async with Client(mcp) as client:
        result = await client.call_tool("list_processes", {})
    assert not result.is_error
    ids = [p["id"] for p in result.structured_content["result"]]
    assert "data-subject-request" in ids


@pytest.mark.anyio
async def test_get_process_returns_ordered_steps():
    async with Client(mcp) as client:
        result = await client.call_tool("get_process", {"process_id": "data-subject-request"})
    assert not result.is_error
    steps = result.structured_content["steps"]
    assert [s["order"] for s in steps] == list(range(1, len(steps) + 1))
    assert steps[1]["role"] == "Privacy Officer"


@pytest.mark.anyio
async def test_unknown_process_returns_error_with_valid_ids():
    async with Client(mcp) as client:
        result = await client.call_tool("get_process", {"process_id": "unknown"})
    assert result.is_error
    assert "data-subject-request" in result.content[0].text
