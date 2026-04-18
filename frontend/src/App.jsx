import { useState, useRef, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [isStarted, setIsStarted] = useState(false);
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleFileUpload = async (e) => {
    const selectedFile = e.target.files[0];
    if (!selectedFile) return;
    
    setFile(selectedFile);
    setUploading(true);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      await axios.post("http://127.0.0.1:8000/upload", formData);
      setIsStarted(true);
    } catch (err) {
      console.error("Upload failed", err);
      alert("Failed to process PDF.");
    } finally {
      setUploading(false);
    }
  };

  const handleAsk = async () => {
    if (!question.trim()) return;

    const userMsg = { type: "user", text: question };
    setMessages((prev) => [...prev, userMsg]);
    setQuestion("");
    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:8000/chat", { question });
      const aiMsg = {
        type: "ai",
        text: res.data.answer,
        image: res.data.image,
      };
      setMessages((prev) => [...prev, aiMsg]);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (!isStarted) {
    return (
      <div className="landing-page">
        <div className="landing-content">
          <div className="badge">AI-Powered Learning</div>
          <h1>
            Your Personal <span className="text-gradient">AI Tutor</span>
          </h1>
          <p>Upload your chapter PDF and start learning with interactive explanations and visual aids.</p>
          
          <div className="upload-section">
            <label className={`upload-card ${uploading ? 'loading' : ''}`}>
              <input type="file" onChange={handleFileUpload} accept=".pdf" hidden />
              <div className="upload-icon">{uploading ? '⏳' : '📄'}</div>
              <span>{uploading ? 'Processing PDF...' : 'Drop your PDF here or Click to Browse'}</span>
            </label>
          </div>
        </div>
        <div className="bg-blur-1"></div>
        <div className="bg-blur-2"></div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="chat-header">
        <div className="tutor-info">
          <div className="status-dot"></div>
          <span>AI Tutor • {file?.name}</span>
        </div>
        <button className="reset-btn" onClick={() => setIsStarted(false)}>New Chapter</button>
      </header>

      <div className="grid-wrapper">
        <div className="grid-background"></div>
        <div className="chat">
          {messages.length === 0 && (
            <div className="empty-state">
              <p>PDF Loaded! Ask me anything about the content.</p>
            </div>
          )}
          {messages.map((msg, i) => (
            <div key={i} className={`msg-wrapper ${msg.type}`}>
              <div className={`msg ${msg.type}`}>
                <p>{msg.text}</p>
                {msg.image && (
                  <div className="image-container">
                    <img
                      src={`http://127.0.0.1:8000/static/images/${msg.image.filename}`}
                      alt={msg.image.title}
                    />
                    <span className="image-caption">{msg.image.title}</span>
                  </div>
                )}
              </div>
            </div>
          ))}
          {loading && (
            <div className="msg-wrapper ai">
              <div className="msg ai typing-indicator">
                <span></span><span></span><span></span>
              </div>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>
      </div>

      <div className="input-container">
        <div className="input-bar">
          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask a question about the chapter..."
            onKeyDown={(e) => e.key === "Enter" && handleAsk()}
          />
          <button className="send-btn" onClick={handleAsk} disabled={loading}>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
              <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;