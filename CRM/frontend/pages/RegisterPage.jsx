import React, { useState } from 'react'
import axios from 'axios'

export default function RegisterPage() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [secret, setSecret] = useState(null)

  const submit = async e => {
    e.preventDefault()
    const res = await axios.post('http://localhost:3001/register', {
      username,
      password,
    })
    setSecret(res.data.secret)
  }

  return (
    <div>
      <h2>Register</h2>
      <form onSubmit={submit}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={e => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
        />
        <button type="submit">Register</button>
      </form>
      {secret && (
        <div>
          <p>Save this TOTP secret in your authenticator app:</p>
          <pre>{secret}</pre>
        </div>
      )}
    </div>
  )
}
