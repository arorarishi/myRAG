import { useState } from 'react';
import { MessageCircle, FolderOpen, Settings, Send } from 'lucide-react';
import ConfigPanel from './components/ConfigPanel';
import DocumentsTab from './components/DocumentsTab';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('chat');
  const [file, setFile] = useState(null);
  const [messages, setMessages] = useState([]);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [vectorDb, setVectorDb] = useState('FAISS');
  const [metadataDb, setMetadataDb] = useState('SQLITE');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    try {
      const result = await uploadPDF(file);
      alert(`Document uploaded: ${file.name}`);
      setFile(null);
    } catch (err) {
      alert('Failed to upload document');
    } finally {
      setLoading(false);
    }
  };

  const handleSendQuery = () => {
    if (!query.trim()) return;

    // Add user message
    const userMessage = { role: 'user', content: query };
    setMessages([...messages, userMessage]);

    // Simulate AI response
    setTimeout(() => {
      const aiMessage = {
        role: 'assistant',
        content: 'This is a simulated response. In production, this would retrieve relevant chunks from your documents and generate a response using the configured LLM.',
        sources: [
          { name: 'document1.pdf', chunk: 3 },
          { name: 'document2.docx', chunk: 7 }
        ]
      };
      setMessages(prev => [...prev, aiMessage]);
    }, 1000);

    setQuery('');
  };

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <h1>RAG System</h1>
          <p className="subtitle">Modular & Extensible</p>
        </div>

        <nav className="sidebar-nav">
          <button
            className={`nav-item ${activeTab === 'chat' ? 'active' : ''}`}
            onClick={() => setActiveTab('chat')}
          >
            <MessageCircle size={20} className="icon" />
            <span>Chat</span>
          </button>
          <button
            className={`nav-item ${activeTab === 'documents' ? 'active' : ''}`}
            onClick={() => setActiveTab('documents')}
          >
            <FolderOpen size={20} className="icon" />
            <span>Documents</span>
          </button>
          <button
            className={`nav-item ${activeTab === 'settings' ? 'active' : ''}`}
            onClick={() => setActiveTab('settings')}
          >
            <Settings size={20} className="icon" />
            <span>Settings</span>
          </button>
        </nav>

        <div className="sidebar-footer">
          <div className="db-info">
            <div>Vector DB: <strong>{vectorDb}</strong></div>
            <div>Metadata DB: <strong>{metadataDb}</strong></div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        {/* Chat Tab */}
        {activeTab === 'chat' && (
          <div className="chat-container">
            <div className="chat-header">
              <h2>Chat with Documents</h2>
              <p>Ask questions about your indexed documents</p>
            </div>

            <div className="chat-messages">
              {messages.length === 0 ? (
                <div className="empty-state">
                  <p>Start asking questions about your documents...</p>
                </div>
              ) : (
                messages.map((msg, idx) => (
                  <div key={idx} className={`message ${msg.role}`}>
                    <div className="message-content">
                      {msg.content}
                      {msg.sources && (
                        <div className="sources">
                          <strong>Sources:</strong>
                          <ul>
                            {msg.sources.map((src, i) => (
                              <li key={i}>
                                {src.name} (chunk {src.chunk})
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>

            <div className="chat-input-container">
              <input
                type="text"
                className="chat-input"
                placeholder="Ask a question about your documents..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSendQuery()}
              />
              <button className="send-btn" onClick={handleSendQuery}>
                <Send size={18} />
                <span>Send</span>
              </button>
            </div>
          </div>
        )}

        {/* Documents Tab */}
        {activeTab === 'documents' && (
          <DocumentsTab
            vectorDb={vectorDb}
            metadataDb={metadataDb}
          />
        )}

        {/* Settings Tab */}
        {activeTab === 'settings' && <ConfigPanel />}
      </main>
    </div>
  );
}

export default App;
