from __future__ import annotations

import json
from collections.abc import AsyncIterator

from graph.workflow import graph


async def stream_graph(state: dict, config: dict) -> AsyncIterator[tuple[str, dict]]:
    async for event in graph.astream_events(state, config=config, version="v1"):
        event_state = event.get("data", {}).get("state", {})
        yield f"data: {json.dumps(event)}\n\n", event_state
