"""
E2E test for the graph_rag_query MCP tool using the e2e-test workspace.
Run: python test_graphrag_mcp.py
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport

E2E_WORKSPACE = str(Path(__file__).parent / "e2e-test")

QUERIES = [
    {
        "name": "local – error types",
        "args": {
            "query": "What error types are defined and how are they handled?",
            "method": "local",
            "response_type": "Single Paragraph",
            "community_level": 2,
        },
    },
    {
        "name": "local – dead letter config",
        "args": {
            "query": "What dead letter queue configuration exists and when does a message end up there?",
            "method": "local",
            "response_type": "Single Paragraph",
            "community_level": 2,
        },
    },
    {
        "name": "global – system overview",
        "args": {
            "query": "Give a high-level overview of the system's topics, publishers, and consumers.",
            "method": "global",
            "response_type": "Multiple Paragraphs",
            "community_level": 2,
        },
    },
]


async def run_tests():
    print(f"Using GraphRAG workspace: {E2E_WORKSPACE}\n")
    print(f"Python: {sys.executable}\n")

    passed = 0
    failed = 0

    transport = PythonStdioTransport(
        script_path=str(Path(__file__).parent / "log_mcp_server.py"),
        python_cmd=sys.executable,
        env={**os.environ, "GRAPH_RAG_ROOT": E2E_WORKSPACE},
    )
    async with Client(transport) as mcp:
        tools = [t.name for t in await mcp.list_tools()]
        if "graph_rag_query" not in tools:
            print("FAIL: graph_rag_query not found in tool list")
            sys.exit(1)
        print(f"Tools available: {tools}\n")

        for test in QUERIES:
            print(f"--- {test['name']} ---")
            print(f"Query: {test['args']['query']}")
            try:
                result = await mcp.call_tool("graph_rag_query", test["args"])
                data = result.content[0].text if result.content else "{}"

                parsed = json.loads(data)

                if parsed.get("success"):
                    response_preview = parsed["response"][:300].replace("\n", " ")
                    print(f"PASS  response preview: {response_preview}...")
                    passed += 1
                else:
                    print(f"FAIL  graphrag error: {parsed.get('error')}")
                    failed += 1
            except Exception as exc:
                print(f"FAIL  exception: {exc}")
                failed += 1
            print()

    print(f"Results: {passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    asyncio.run(run_tests())
