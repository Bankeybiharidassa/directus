import React from 'react'
import axios from 'axios'

export default function AssetSyncButton() {
  const sync = async () => {
    await axios.post('/assets/sync', null, { params: { source: 'all' } })
    alert('Assets synced')
  }
  return <button onClick={sync}>Sync Assets</button>
}
