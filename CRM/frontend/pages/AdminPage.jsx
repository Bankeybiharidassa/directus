import React, { useState, useEffect } from 'react'
import axios from 'axios'
import KeycloakWizard from './KeycloakWizard'
import SecurityScan from '../components/SecurityScan'
import UserMenu from '../components/UserMenu'

export default function AdminPage() {
  const [tab, setTab] = useState('system')
  const [apiKey, setApiKey] = useState('')
  const [model, setModel] = useState('gpt-4')

  useEffect(() => {
    axios.get('http://localhost:8000/config/api').then(res => {
      if (res.data.model) {
        setModel(res.data.model)
      }
    })
  }, [])

  const save = async e => {
    e.preventDefault()
    await axios.post('http://localhost:8000/config/api', null, {
      params: { api_key: apiKey, model },
    })
    alert('saved')
  }

  return (
    <div>
      <UserMenu />
      <h2>Admin</h2>
      <div>
        <button onClick={() => setTab('system')}>System</button>
        <button onClick={() => setTab('user')}>Super User</button>
        <button onClick={() => setTab('keycloak')}>Keycloak</button>
        <button onClick={() => setTab('security')}>Security Scan</button>
      </div>
      {tab === 'system' && (
        <form onSubmit={save}>
          <input
            type="text"
            placeholder="API Key"
            value={apiKey}
            onChange={e => setApiKey(e.target.value)}
          />
          <select value={model} onChange={e => setModel(e.target.value)}>
            <option value="gpt-4">gpt-4</option>
            <option value="gpt-3.5-turbo">gpt-3.5-turbo</option>
          </select>
          <button type="submit">Save</button>
        </form>
      )}
      {tab === 'user' && <div>Super user management</div>}
      {tab === 'keycloak' && <KeycloakWizard />}
      {tab === 'security' && <SecurityScan />}
    </div>
  )
}
