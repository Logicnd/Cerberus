'use client'
import { useState } from 'react'
export default function LoginPage() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [msg, setMsg] = useState('')
  const [ok, setOk] = useState<boolean | null>(null)
  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    const base = process.env.NEXT_PUBLIC_API_BASE || 'http://127.0.0.1:5000'
    try {
      const res = await fetch(`${base}/api/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
        credentials: 'include',
      })
      const j = await res.json().catch(()=>({}))
      if (res.ok && j?.ok) {
        setOk(true)
        setMsg('Logged in')
      } else {
        setOk(false)
        setMsg('Invalid credentials')
      }
    } catch {
      setOk(false)
      setMsg('Login failed')
    }
  }
  return (
    <section className="card">
      <h2>Login</h2>
      <form className="form" onSubmit={submit}>
        <label>Username</label>
        <input type="text" value={username} onChange={e=>setUsername(e.target.value)} />
        <label>Password</label>
        <input type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        <button className="btn" type="submit">Login</button>
      </form>
      {msg && <p style={{color: ok ? 'green' : 'var(--fg)'}}>{msg}</p>}
    </section>
  )
}
