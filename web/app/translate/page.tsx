'use client'
import { useState } from 'react'

export default function TranslatePage() {
  const [src, setSrc] = useState('python')
  const [dst, setDst] = useState('html')
  const [code, setCode] = useState('')
  const [output, setOutput] = useState('')
  const [analysis, setAnalysis] = useState<any>(null)
  const [links, setLinks] = useState<any>(null)
  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    const base = process.env.NEXT_PUBLIC_API_BASE || 'http://127.0.0.1:5000'
    const res = await fetch(`${base}/translate`, { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams({ src, dst, code }).toString() })
    const html = await res.text()
    setOutput(html)
    setAnalysis({ ok: true })
    setLinks({ ok: true })
  }
  return (
    <section className="card">
      <h2>Translate</h2>
      <form className="form" onSubmit={submit}>
        <label>Source</label>
        <select value={src} onChange={e=>setSrc(e.target.value)}>
          <option value="python">Python</option>
          <option value="html">HTML</option>
        </select>
        <label>Target</label>
        <select value={dst} onChange={e=>setDst(e.target.value)}>
          <option value="html">HTML</option>
          <option value="javascript">JavaScript</option>
          <option value="python">Python</option>
        </select>
        <label>Code</label>
        <textarea rows={10} value={code} onChange={e=>setCode(e.target.value)} />
        <button className="btn" type="submit">Translate</button>
      </form>
      {output && <section className="card"><h3>Output</h3><pre><code>{output}</code></pre></section>}
    </section>
  )
}
