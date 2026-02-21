'use client'
import { useState } from 'react'

export default function BatchPage() {
  const [sourceLang, setSourceLang] = useState('python')
  const [targetLang, setTargetLang] = useState('html')
  const [texts, setTexts] = useState('')
  const [translated, setTranslated] = useState<string[]>([])
  const [analyzed, setAnalyzed] = useState<any[]>([])
  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    const base = process.env.NEXT_PUBLIC_API_BASE || 'http://127.0.0.1:5000'
    const res = await fetch(`${base}/batch`, { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams({ source_lang: sourceLang, target_lang: targetLang, texts }).toString() })
    const html = await res.text()
    setTranslated(['OK'])
    setAnalyzed([{ ok: true }])
  }
  return (
    <section className="card">
      <h2>Batch</h2>
      <form className="form" onSubmit={submit}>
        <label>Source</label>
        <select value={sourceLang} onChange={e=>setSourceLang(e.target.value)}>
          <option value="python">Python</option>
          <option value="html">HTML</option>
        </select>
        <label>Target</label>
        <select value={targetLang} onChange={e=>setTargetLang(e.target.value)}>
          <option value="html">HTML</option>
          <option value="javascript">JavaScript</option>
          <option value="python">Python</option>
        </select>
        <label>Items</label>
        <textarea rows={10} value={texts} onChange={e=>setTexts(e.target.value)} />
        <button className="btn" type="submit">Run</button>
      </form>
    </section>
  )
}
