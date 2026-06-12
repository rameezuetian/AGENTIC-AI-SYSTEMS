from __future__ import annotations

from agents.analyst_agent import analyst_agent
from agents.memory_agent import memory_agent
from agents.reject_agent import reject_agent
from agents.retriever_agent import retriever_agent
from agents.safety_agent import safety_agent
from agents.writer_agent import writer_agent


class LocalWorkflow:
    def __init__(self):
        self.node_map = {
            "memory": memory_agent,
            "safety": safety_agent,
            "reject": reject_agent,
            "retriever": retriever_agent,
            "analyst": analyst_agent,
            "writer": writer_agent,
        }

    def _run_pipeline(self, state: dict):
        working_state = dict(state)

        for node_name in ("memory", "safety"):
            update = self.node_map[node_name](working_state)
            working_state.update(update)
            yield node_name, dict(working_state)

        if not working_state.get("safe", True):
            update = self.node_map["reject"](working_state)
            working_state.update(update)
            yield "reject", dict(working_state)
            return

        for node_name in ("retriever", "analyst", "writer"):
            update = self.node_map[node_name](working_state)
            working_state.update(update)
            yield node_name, dict(working_state)

    def invoke(self, state: dict, config: dict | None = None) -> dict:
        final_state = dict(state)
        for _, updated_state in self._run_pipeline(state):
            final_state = updated_state
        return final_state

    async def astream_events(self, state: dict, config: dict | None = None, version: str = "v1"):
        for node_name, updated_state in self._run_pipeline(state):
            payload = {
                "event": "node_complete",
                "data": {
                    "node": node_name,
                    "state": updated_state,
                },
            }
            yield payload


graph = LocalWorkflow()
