import React, { useEffect, useState } from 'react'
import axios from 'axios'

export default function ApiConfigForm() {
  const [apiKey, setApiKey] = useState('')
  const [model, setModel] = useState('')
  const [models, setModels] = useState([])

  useEffect(() => {
    axios.get('/config/models').then(res => setModels(res.data))
    axios.get('/config/api').then(res => {
      if (res.data.model) {
        setModel(res.data.model)
      }
    })
  }, [])

  const submit = async e => {
    e.preventDefault()
    await axios.post('/config/api', null, { params: { api_key: apiKey, model } })
    alert('Saved')
  }

  return (
    <form onSubmit={submit}>
      <input type="text" placeholder="API Key" value={apiKey} onChange={e => setApiKey(e.target.value)} />
      <select value={model} onChange={e => setModel(e.target.value)}>
        {models.map(m => (
          <option key={m} value={m}>{m}</option>
        ))}
      </select>
      <button type="submit">Save</button>
    </form>
  )
}
