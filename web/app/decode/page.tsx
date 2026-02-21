'use client'
import { useState } from 'react'

export default function DecodePage() {
  const [scheme, setScheme] = useState('base64')
  const [data, setData] = useState('')
  const [key, setKey] = useState('')
  const [output, setOutput] = useState('')
  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    const base = process.env.NEXT_PUBLIC_API_BASE || 'http://127.0.0.1:5000'
    const res = await fetch(`${base}/decode`, { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams({ scheme, data, key }).toString() })
    const html = await res.text()
    setOutput(html)
  }
  return (
    <section className="card">
      <h2>Decode</h2>
      <form className="form" onSubmit={submit}>
        <label>Scheme</label>
        <select value={scheme} onChange={e=>setScheme(e.target.value)}>
          <option value="base64">Base64</option>
          <option value="hex">Hex</option>
          <option value="rot13">ROT13</option>
          <option value="xor">XOR</option>
          <option value="auto">Auto</option>
        </select>
        <label>Data</label>
        <textarea rows={8} value={data} onChange={e=>setData(e.target.value)} />
        <label>Key</label>
        <input type="text" value={key} onChange={e=>setKey(e.target.value)} />
        <button className="btn" type="submit">Decode</button>
      </form>
      {output && <section className="card"><h3>Output</h3><pre><code>{output}</code></pre></section>}
    </section>
  )
}
