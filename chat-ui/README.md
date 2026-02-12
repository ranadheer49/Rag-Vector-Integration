# Chat UI (React + Vite)

Simple chat UI that sends POST requests to a backend API at `/api/chat`.

Quick start:

1. Install dependencies

```bash
cd chat-ui
npm install
```

2. Run dev server

```bash
npm run dev
```

3. Backend API

The UI expects a POST `/api/chat` that receives JSON `{ message: string }` and returns JSON `{ reply: string }` (or `{ response: string }`).

Example Express handler:

```js
app.post("/api/chat", express.json(), async (req, res) => {
  const { message } = req.body;
  // call your model or service
  res.json({ reply: `Echo: ${message}` });
});
```

Files of interest:

- `src/components/Chat.jsx` — main chat UI and API logic
- `src/App.jsx` — mounts the chat
