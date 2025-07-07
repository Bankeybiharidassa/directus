import React, { useEffect, useState } from 'react'
import axios from 'axios'

export default function StatusPage() {
  const [status, setStatus] = useState(null)

  useEffect(() => {
    axios.get('http://localhost:8000/core/status').then(res => setStatus(res.data))
  }, [])

  if (!status) return <div>Loading...</div>

  return (
    <div>
      <h2>Status</h2>
      <pre>{JSON.stringify(status, null, 2)}</pre>
    </div>
  )
}
