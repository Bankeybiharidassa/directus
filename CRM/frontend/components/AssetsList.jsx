import React, { useEffect, useState } from 'react'
import axios from 'axios'

export default function AssetsList() {
  const [assets, setAssets] = useState([])

  useEffect(() => {
    axios.get('/assets/').then(res => setAssets(res.data))
  }, [])

  return (
    <ul>
      {assets.map(a => (
        <li key={a.id}>{a.hostname} ({a.status})</li>
      ))}
    </ul>
  )
}
