import { useState, useRef, useEffect } from "react";
import api from "../services/api";

const BACKEND_HINT_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

function ChatPanel({ threadId, userId, messages, onNewMessage }) {
  const [question, setQuestion] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [activeSteps, setActiveSteps] = useState([]);
  const [toggledSources, setToggledSources] = useState({});
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, activeSteps]);

  const toggleSources = (msgIndex) => {
    setToggledSources((prev) => ({
      ...prev,
      [msgIndex]: !prev[msgIndex],
    }));
  };

  const parseMarkdown = (text) => {
    if (!text) return "";
    
    // Safety check: protect HTML tags
    let html = text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");

    // Code blocks
    html = html.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
    
    // Inline code
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
    
    // Bold
    html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    
    // Line breaks & lists
    const lines = html.split("\n");
    let inList = false;
    const processedLines = lines.map((line) => {
      const trimmed = line.trim();
      if (trimmed.startsWith("- ") || trimmed.startsWith("* ")) {
        let content = line.substring(2);
        let listPrefix = "";
        if (!inList) {
          inList = true;
          listPrefix = "<ul>";
        }
        return `${listPrefix}<li>${content}</li>`;
      } else {
        let listSuffix = "";
        if (inList) {
          inList = false;
          listSuffix = "</ul>";
        }
        return `${listSuffix}${line}`;
      }
    });

    if (inList) {
      processedLines.push("</ul>");
    }

    return processedLines.join("\n");
  };

  const executeChatStream = async (event) => {
    event.preventDefault();
    const queryText = question.trim();
    if (!queryText || isSending) return;

    setIsSending(true);
    setQuestion("");
    setActiveSteps([
      { id: "memory", label: "🧠 Memory Agent: Analyzing context", status: "active" },
      { id: "safety", label: "🛡️ Safety Agent: Auditing input safety", status: "pending" },
      { id: "retriever", label: "🔍 Retriever Agent: Fetching relevant documents", status: "pending" },
      { id: "analyst", label: "📊 Analyst Agent: Synthesizing facts", status: "pending" },
      { id: "writer", label: "✍️ Writer Agent: Generating grounded answer", status: "pending" },
    ]);

    // Append the user's message immediately
    onNewMessage({ role: "user", content: queryText });

    let finalAnswer = "";
    let retrievedDocs = [];
    let safetyDecision = "Passed";
    let finalSources = [];
    let executedAgents = [];

    try {
      const response = await api.stream("/api/chat/stream", {
        question: queryText,
        user_id: userId,
        thread_id: threadId,
      });

      if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n\n");
        buffer = lines.pop() || ""; // Keep the incomplete line in buffer

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const dataStr = line.substring(6).trim();
            if (!dataStr) continue;

            try {
              const payload = JSON.parse(dataStr);
              if (payload.event === "node_complete") {
                const nodeName = payload.data.node;
                const nodeState = payload.data.state;
                executedAgents.push(nodeName);

                // Update steps timeline
                setActiveSteps((prev) =>
                  prev.map((step) => {
                    if (step.id === nodeName) {
                      return { ...step, status: "completed" };
                    }
                    // Find next step to set as active
                    if (
                      (nodeName === "memory" && step.id === "safety") ||
                      (nodeName === "safety" && nodeState.safe && step.id === "retriever") ||
                      (nodeName === "retriever" && step.id === "analyst") ||
                      (nodeName === "analyst" && step.id === "writer")
                    ) {
                      return { ...step, status: "active" };
                    }
                    return step;
                  })
                );

                // If input is unsafe, reject node triggers immediately after safety
                if (nodeName === "safety" && !nodeState.safe) {
                  safetyDecision = nodeState.safety_decision || "Flagged";
                  setActiveSteps((prev) =>
                    prev.map((step) =>
                      step.id !== "memory" && step.id !== "safety"
                        ? { ...step, status: "pending", label: `🚫 Blocked: ${safetyDecision}` }
                        : step
                    )
                  );
                }

                // Gather intermediate details
                if (nodeState.retrieved_docs) {
                  retrievedDocs = nodeState.retrieved_docs;
                  finalSources = nodeState.sources || [];
                }
                if (nodeState.answer) {
                  finalAnswer = nodeState.answer;
                  safetyDecision = nodeState.safety_decision || safetyDecision;
                }
              }
            } catch (err) {
              console.error("Error parsing stream token payload:", err, dataStr);
            }
          }
        }
      }

      // Finish streaming and append assistant message
      onNewMessage({
        role: "assistant",
        content: finalAnswer || "Rejection: Request blocked by safety policy.",
        sources: retrievedDocs,
        safety_decision: safetyDecision,
        agents_run: executedAgents,
      });
    } catch (err) {
      console.error("Chat error:", err);
      onNewMessage({
        role: "assistant",
        content: `Could not connect to the assistant: ${err.message}. Please verify the backend is running on ${BACKEND_HINT_URL}.`,
        safety_decision: "Error",
      });
    } finally {
      setIsSending(false);
      setActiveSteps([]);
    }
  };

  return (
    <section className="panel chat-panel">
      <div className="panel-heading">
        <p className="eyebrow">🤖 Assistant Hub</p>
        <h2>Ask Project Intelligence</h2>
      </div>

      <div className="chat-thread">
        {messages.length === 0 ? (
          <div className="empty-state">
            <span className="empty-icon">💬</span>
            <h3>No Messages Yet</h3>
            <p style={{ fontSize: "0.85rem", marginTop: "6px" }}>
              Upload documents in the sidebar, then ask questions here. The workspace uses memory persistence to retain preferences.
            </p>
          </div>
        ) : (
          messages.map((message, index) => (
            <article key={`${message.role}-${index}`} className={`bubble bubble-${message.role}`}>
              <div className="bubble-role">
                <span>{message.role === "user" ? "👤 You" : "⚡ Agent System"}</span>
              </div>
              
              <div
                className="bubble-content"
                dangerouslySetInnerHTML={{ __html: parseMarkdown(message.content) }}
              />

              {message.role === "assistant" && (
                <div className="bubble-meta">
                  {message.safety_decision && (
                    <span className={`meta-item ${message.safety_decision.toLowerCase().includes("passed") ? "passed" : "flagged"}`}>
                      🛡️ {message.safety_decision}
                    </span>
                  )}
                  {message.agents_run && (
                    <span className="meta-item" style={{ fontSize: "0.7rem", fontFamily: "var(--font-mono)" }} title="Workflow Execution Pipeline">
                      🔗 {message.agents_run.join(" ➔ ")}
                    </span>
                  )}
                </div>
              )}

              {message.role === "assistant" && message.sources && message.sources.length > 0 && (
                <div className="sources-section">
                  <button
                    type="button"
                    className="sources-toggle"
                    onClick={() => toggleSources(index)}
                  >
                    🔍 {toggledSources[index] ? "Hide" : "Show"} Grounded Sources ({message.sources.length})
                  </button>
                  {toggledSources[index] && (
                    <div className="sources-grid">
                      {message.sources.map((src, srcIdx) => (
                        <div key={srcIdx} className="source-card">
                          <div className="source-header">📄 {src.metadata?.source || "Unknown Chunk"}</div>
                          <div className="source-snippet">
                            {src.page_content ? `"${src.page_content.substring(0, 240)}..."` : "No excerpt available"}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </article>
          ))
        )}

        {isSending && activeSteps.length > 0 && (
          <div className="agent-timeline">
            <h4 style={{ fontSize: "0.82rem", color: "var(--text-secondary)", marginBottom: "4px" }}>
              Multi-Agent Orchestration Pipeline
            </h4>
            {activeSteps.map((step) => (
              <div key={step.id} className={`timeline-step ${step.status}`}>
                <span className="timeline-bullet" />
                <span>{step.label}</span>
              </div>
            ))}
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      <form className="chat-form" onSubmit={executeChatStream}>
        <div className="chat-input-wrapper">
          <textarea
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="Ask a question about your files or set preferences (e.g. 'I prefer concise answers')"
            rows={3}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                executeChatStream(e);
              }
            }}
          />
        </div>
        <div className="chat-actions">
          <p className="meta-status-text">
            Active Workspace Thread: <strong style={{ color: "var(--text-primary)" }}>{threadId}</strong>
          </p>
          <button type="submit" className="primary-button" disabled={isSending || !question.trim()}>
            {isSending ? "Processing..." : "Submit Inquiry ⚡"}
          </button>
        </div>
      </form>
    </section>
  );
}

export default ChatPanel;
