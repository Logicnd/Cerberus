import Link from 'next/link'

export default function Page() {
  return (
    <section className="card">
      <h2>Welcome</h2>
      <p>Select a task from the navigation.</p>
      <div className="grid">
        <div>
          <h3>Code Intelligence</h3>
          <ul>
            <li><Link href="/translate">Translate</Link></li>
            <li><Link href="/analyze">Analyze</Link></li>
            <li><Link href="/decode">Decode</Link></li>
            <li><Link href="/batch">Batch</Link></li>
          </ul>
        </div>
        <div>
          <h3>Security</h3>
          <ul>
            <li><Link href="/scan">Scan</Link></li>
          </ul>
        </div>
      </div>
    </section>
  )
}
