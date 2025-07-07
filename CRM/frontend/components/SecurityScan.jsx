import React, { useState } from 'react'
import axios from 'axios'

export default function SecurityScan() {
  const [report, setReport] = useState(null)

  const run = async () => {
    const res = await axios.get('http://localhost:8000/core/security/scan', { auth: { username: 'admin', password: 'pw' } }).catch(() => null)
    if (res && res.status === 200) {
      setReport(res.data)
    } else {
      alert('scan failed')
    }
  }

  return (
    <div>
      <button onClick={run}>Run Security Scan</button>
      {report && <pre>{JSON.stringify(report, null, 2)}</pre>}
    </div>
  )
}
