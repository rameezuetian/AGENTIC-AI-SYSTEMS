import { useEffect, useState } from "react";
import "./App.css";
import ChatPanel from "./components/ChatPanel";
import FileUpload from "./components/FileUpload";
import MemoryPanel from "./components/MemoryPanel";
import api from "./services/api";

const DEFAULT_USER_ID = "demo-user";

function App() {
  const [messages, setMessages] = useState([]);
  const [memories, setMemories] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [files, setFiles] = useState([]);
  const [threadId, setThreadId] = useState("thread-001");
  const [systemStatus, setSystemStatus] = useState({
    gemini_connected: false,
    model: "Local Heuristics",
  });

  const refreshData = async () => {
    try {
      const [memoryData, sessionData, fileData, statusData] = await Promise.all([
        api.get(`/api/memories/${DEFAULT_USER_ID}`),
        api.get("/api/sessions"),
        api.get("/api/files"),
        api.get("/api/status"),
      ]);
      setMemories(memoryData.memories ?? []);
      const nextSessions = sessionData.sessions ?? [];
      setSessions(nextSessions);
      setFiles(fileData.files ?? []);
      setSystemStatus(statusData ?? { gemini_connected: false, model: "Local Heuristics" });
      if (
        nextSessions.length > 0 &&
        !nextSessions.some((session) => session.thread_id === threadId)
      ) {
        setThreadId(nextSessions[0].thread_id);
      }
    } catch (err) {
      console.error("Error refreshing dashboard data:", err);
    }
  };

  const loadThreadHistory = async (id) => {
    try {
      const response = await api.get(`/api/sessions/${id}`);
      setMessages(response.messages ?? []);
    } catch {
      setMessages([]);
    }
  };

  useEffect(() => {
    refreshData();
  }, []);

  useEffect(() => {
    loadThreadHistory(threadId);
  }, [threadId]);

  const handleNewMessage = (message) => {
    setMessages((current) => [...current, message]);
    setTimeout(() => {
      refreshData();
    }, 100);
  };

  const handleSelectThread = (id) => {
    setThreadId(id);
  };

  const handleNewThread = () => {
    const newId = `thread-${Math.floor(1000 + Math.random() * 9000)}`;
    setThreadId(newId);
    setMessages([]);
    setTimeout(() => {
      refreshData();
    }, 100);
  };

  const handleDeleteThread = async (id) => {
    try {
      await api.delete(`/api/sessions/${id}`);
      if (threadId === id) {
        const nextSessions = sessions.filter((s) => s.thread_id !== id);
        if (nextSessions.length > 0) {
          setThreadId(nextSessions[0].thread_id);
        } else {
          setThreadId("thread-001");
        }
      }
      await refreshData();
    } catch (err) {
      console.error("Failed to delete session:", err);
    }
  };

  const handleDeleteFile = async (filename) => {
    try {
      await api.delete(`/api/files/${filename}`);
      refreshData();
    } catch (err) {
      console.error("Failed to delete file:", err);
    }
  };

  const handleDeleteMemory = async (key) => {
    try {
      await api.delete(`/api/memories/${DEFAULT_USER_ID}/${key}`);
      refreshData();
    } catch (err) {
      console.error("Failed to delete memory fact:", err);
    }
  };

  return (
    <main className="app-shell">
      <header className="app-header">
        <section className="hero-banner">
          <p className="eyebrow">
            <span>✨</span> Final Project 11
          </p>
          <h1>AI Intelligence Platform</h1>
          <p className="hero-copy">
            Upload local documents, ask grounded questions, and keep lightweight
            memory across sessions from a single workspace.
          </p>
        </section>
        
        <div className="status-badge">
          <span className={`status-indicator ${systemStatus.gemini_connected ? "connected" : "fallback"}`}></span>
          <span>
            {systemStatus.gemini_connected 
              ? `Gemini Connected: ${systemStatus.model}` 
              : "Running in Local Heuristic Fallback Mode"}
          </span>
        </div>
      </header>

      <section className="workspace-grid">
        <div className="workspace-left">
          <FileUpload 
            files={files} 
            onUploadComplete={refreshData} 
            onDeleteFile={handleDeleteFile}
          />
        </div>

        <div className="workspace-main">
          <ChatPanel
            threadId={threadId}
            userId={DEFAULT_USER_ID}
            messages={messages}
            onNewMessage={handleNewMessage}
          />
        </div>

        <div className="workspace-right">
          <MemoryPanel 
            memories={memories} 
            sessions={sessions} 
            activeThreadId={threadId}
            onSelectThread={handleSelectThread}
            onNewThread={handleNewThread}
            onDeleteThread={handleDeleteThread}
            onDeleteMemory={handleDeleteMemory}
          />
        </div>
      </section>
    </main>
  );
}

export default App;
