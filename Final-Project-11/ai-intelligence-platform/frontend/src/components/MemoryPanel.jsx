function MemoryPanel({
  memories,
  sessions,
  activeThreadId,
  onSelectThread,
  onNewThread,
  onDeleteThread,
  onDeleteMemory,
}) {
  return (
    <section className="panel sidebar-panel">
      <div className="panel-heading">
        <p className="eyebrow">🧠 Context Vault</p>
        <h2>Memory & Chats</h2>
      </div>

      {/* Remembered facts section */}
      <div className="sidebar-block">
        <h3>Remembered Facts</h3>
        {memories.length ? (
          <ul className="memory-fact-list">
            {memories.map((m) => (
              <li key={m.key} className="memory-fact-item">
                <span className="memory-fact-text">{m.fact}</span>
                <button
                  type="button"
                  className="delete-fact-btn"
                  title="Forget this fact"
                  onClick={() => onDeleteMemory(m.key)}
                >
                  ✕
                </button>
              </li>
            ))}
          </ul>
        ) : (
          <p className="muted" style={{ fontSize: "0.8rem" }}>
            No personal preferences or facts saved. Try saying: "I prefer short answers" or "I am learning Python".
          </p>
        )}
      </div>

      {/* Sessions section */}
      <div className="sidebar-block" style={{ marginTop: "32px" }}>
        <h3>Recent Sessions</h3>
        <button
          type="button"
          className="new-session-btn"
          onClick={onNewThread}
        >
          ➕ New Chat Session
        </button>

        {sessions.length ? (
          <ul className="sidebar-list">
            {sessions.map((s) => (
              <li
                key={s.thread_id}
                className={`session-item ${activeThreadId === s.thread_id ? "active" : ""}`}
                onClick={() => onSelectThread(s.thread_id)}
              >
                <div className="session-meta-info">
                  <span className="session-id">{s.thread_id}</span>
                  <span className="session-preview">
                    {s.last_message || `${s.message_count} messages`}
                  </span>
                </div>
                <button
                  type="button"
                  className="trash-button"
                  title="Delete session"
                  onClick={(e) => {
                    e.stopPropagation(); // Avoid switching session on click
                    onDeleteThread(s.thread_id);
                  }}
                  style={{ padding: "4px" }}
                >
                  🗑️
                </button>
              </li>
            ))}
          </ul>
        ) : (
          <p className="muted" style={{ fontSize: "0.8rem" }}>No saved chat sessions.</p>
        )}
      </div>
    </section>
  );
}

export default MemoryPanel;
