import React, { useState } from 'react'
import axios from 'axios'

export default function LoginForm() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [otp, setOtp] = useState('')

  const submit = async e => {
    e.preventDefault()
    const res = await axios.post('http://localhost:3001/login', { username, password, otp })
    alert(res.data.message)
  }

  return (
    <form onSubmit={submit}>
      <input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
      <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
      <input type="text" placeholder="OTP" value={otp} onChange={e => setOtp(e.target.value)} />
      <button type="submit">Login</button>
    </form>
  )
}
