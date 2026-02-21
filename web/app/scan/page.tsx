'use client'
import { useState } from 'react'

export default function ScanPage() {
  const [target, setTarget] = useState('')
  const [msg, setMsg] = useState('')
  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    const base = process.env.NEXT_PUBLIC_API_BASE || 'http://127.0.0.1:5000'
    const res = await fetch(`${base}/scan`, { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams({ target }).toString(), credentials: 'include' })
    if (res.ok) setMsg('Scan triggered in backend')
    else setMsg('Scan requires login in Flask UI')
  }
  return (
    <section className="card">
      <h2>Scan</h2>
      <form className="form" onSubmit={submit}>
        <label>Target URL</label>
        <input type="url" value={target} onChange={e=>setTarget(e.target.value)} />
        <button className="btn" type="submit">Run</button>
      </form>
      {msg && <p>{msg}</p>}
    </section>
  )
}
