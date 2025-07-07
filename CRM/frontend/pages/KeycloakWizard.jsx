import React, { useState, useEffect } from 'react'
import axios from 'axios'

export default function KeycloakWizard() {
  const [url, setUrl] = useState('')
  const [realm, setRealm] = useState('')
  const [clientId, setClientId] = useState('')
  const [clientSecret, setClientSecret] = useState('')

  useEffect(() => {
    axios.get('http://localhost:8000/keycloak/').then(res => {
      if (res.data.url) {
        setUrl(res.data.url)
        setRealm(res.data.realm)
        setClientId(res.data.client_id)
      }
    })
  }, [])

  const save = async e => {
    e.preventDefault()
    await axios.post('http://localhost:8000/keycloak/', null, {
      params: { url, realm, client_id: clientId, client_secret: clientSecret },
    })
    alert('saved')
  }

  return (
    <div>
      <h3>Keycloak Integration</h3>
      <form onSubmit={save}>
        <input
          type="text"
          placeholder="URL"
          value={url}
          onChange={e => setUrl(e.target.value)}
        />
        <input
          type="text"
          placeholder="Realm"
          value={realm}
          onChange={e => setRealm(e.target.value)}
        />
        <input
          type="text"
          placeholder="Client ID"
          value={clientId}
          onChange={e => setClientId(e.target.value)}
        />
        <input
          type="password"
          placeholder="Client Secret"
          value={clientSecret}
          onChange={e => setClientSecret(e.target.value)}
        />
        <button type="submit">Save</button>
      </form>
    </div>
  )
}
