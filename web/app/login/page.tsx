'use client'
import { useState } from 'react'

export default function LoginPage() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [msg, setMsg] = useState('')
  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    setMsg('Use the Flask UI login for authenticated actions.')
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
      {msg && <p>{msg}</p>}
    </section>
  )
}
