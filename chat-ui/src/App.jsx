import React from 'react'
import Chat from './components/Chat'

export default function App() {
  return (
    <div className="app">
      <header className="app-header">Chat Bot UI</header>
      <main className="app-main">
        <Chat apiUrl='www.google/api/chat' /> 
        {/* <Chat apiUrl={process.env.API_URL || '/api/chat'} /> */}
      </main>
    </div>
  )
}
