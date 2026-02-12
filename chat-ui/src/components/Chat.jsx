import React, { useState, useRef } from 'react'

function Message({ m }) {
  const cls = m.role === 'user' ? 'msg user' : 'msg bot'
  return (
    <div className={cls}>
      <div className="bubble">{m.content}</div>
    </div>
  )
}

export default function Chat({ apiUrl = '/api/chat' }) {
  const [messages, setMessages] = useState([
    { role: 'bot', content: 'Hello! How can I help you today?' }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const inputRef = useRef(null)

  async function send() {
    const text = input.trim()
    if (!text) return
    const userMsg = { role: 'user', content: text }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setLoading(true)
    try {
      const res = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      })
      if (!res.ok) throw new Error(`status ${res.status}`)
      const data = await res.json()
      const reply = data.reply ?? data.response ?? 'No response'
      setMessages(prev => [...prev, { role: 'bot', content: reply }])
    } catch (err) {
      setMessages(prev => [...prev, { role: 'bot', content: 'Error: ' + err.message }])
    } finally {
      setLoading(false)
      inputRef.current?.focus()
    }
  }

  function handleKey(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      send()
    }
  }

  return (
    <div className="chat">
      <div className="messages">
        {messages.map((m, i) => (
          <Message key={i} m={m} />
        ))}
        {loading && (
          <div className="msg bot"><div className="bubble">Typing…</div></div>
        )}
      </div>

      <div className="composer">
        <textarea
          ref={inputRef}
          className="input"
          rows={2}
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKey}
          placeholder="Type a message and press Enter"
        />
        <button className="send" onClick={send} disabled={loading || !input.trim()}>
          Send
        </button>
      </div>
    </div>
  )
}
