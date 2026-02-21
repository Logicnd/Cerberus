'use client'
import { useState } from 'react'

export default function AnalyzePage() {
  const [lang, setLang] = useState('python')
  const [code, setCode] = useState('')
  const [analysis, setAnalysis] = useState<any>(null)
  const [links, setLinks] = useState<any>(null)
  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    const base = process.env.NEXT_PUBLIC_API_BASE || 'http://127.0.0.1:5000'
    const res = await fetch(`${base}/analyze`, { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams({ lang, code }).toString() })
    const html = await res.text()
    setAnalysis({ ok: true })
    setLinks({ ok: true })
  }
  return (
    <section className="card">
      <h2>Analyze</h2>
      <form className="form" onSubmit={submit}>
        <label>Language</label>
        <select value={lang} onChange={e=>setLang(e.target.value)}>
          <option value="python">Python</option>
          <option value="html">HTML</option>
        </select>
        <label>Code</label>
        <textarea rows={10} value={code} onChange={e=>setCode(e.target.value)} />
        <button className="btn" type="submit">Analyze</button>
      </form>
    </section>
  )
}
