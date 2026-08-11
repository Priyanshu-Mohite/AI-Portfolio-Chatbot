import { useState, useRef, useEffect } from 'react'

function App() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello! I am Priyanshu\'s AI assistant. Ask me anything about his skills and projects.' }
  ]);
  const [input, setInput] = useState('');

  // 1. Ek reference bana jo hamesha chat ke end (bottom) ko point karega
  const messagesEndRef = useRef(null);

  // 2. Scroll karne ka function banaya (smooth animation ke sath)
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // 3. Jab bhi 'messages' array update hogi, yeh effect apne aap chalega aur scroll kar dega
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    // User ka message UI pe dikhane ke liye add karo
    const newMessages = [...messages, { role: 'user', content: input }];
    setMessages(newMessages);
    setInput(''); // Input box clear karo

    try {
      // Backend ko API call
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_input: input })
      });
      
      const data = await response.json();

      // AI ka reply UI me add karo
      setMessages([...newMessages, { role: 'assistant', content: data.reply }]);
    } catch (error) {
      console.error("Error backend se connect karne me:", error);
      setMessages([...newMessages, { role: 'assistant', content: 'Oops! Backend se connect nahi ho paya. Server on hai?' }]);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-900 text-white font-sans">
      {/* Header */}
      <header className="bg-gray-800 p-4 shadow-md text-center text-xl font-bold border-b border-gray-700">
        Priyanshu's AI Portfolio
      </header>

      {/* Chat Area */}
      <main className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, index) => (
          <div key={index} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-3xl p-3 rounded-lg ${msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-200'}`}>
              <p className="whitespace-pre-wrap">{msg.content}</p>
            </div>
          </div>
        ))}

        <div ref={messagesEndRef} />
      </main>

      {/* Input Area */}
      <footer className="bg-gray-800 p-4 border-t border-gray-700">
        <div className="max-w-4xl mx-auto flex gap-3">
          <input 
            type="text" 
            className="flex-1 bg-gray-700 text-white rounded-lg p-3 outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Ask about Priyanshu's projects or skills..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
          />
          <button 
            onClick={sendMessage}
            className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg font-semibold transition-colors"
          >
            Send
          </button>
        </div>
      </footer>
    </div>
  )
}

export default App