import './globals.css'
import Link from 'next/link'

export const metadata = {
  title: 'Cerberus',
  description: 'Educational Vulnerability Assessment'
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="header">
          <div className="container">
            <h1>Cerberus</h1>
            <p>Educational Vulnerability Assessment</p>
            <nav className="nav">
              <Link href="/">Home</Link>
              <Link href="/scan">Scan</Link>
              <Link href="/translate">Translate</Link>
              <Link href="/analyze">Analyze</Link>
              <Link href="/decode">Decode</Link>
              <Link href="/batch">Batch</Link>
              <Link href="/login">Login</Link>
            </nav>
          </div>
        </header>
        <main className="container">{children}</main>
      </body>
    </html>
  )
}
