import React from 'react'

export default function UserMenu({ username = 'User' }) {
  return (
    <div style={{ position: 'absolute', top: 10, right: 10 }}>
      <span>{username}</span>
      {' | '}
      <a href="#profile">Profile</a>
      {' | '}
      <a href="#security">Security</a>
    </div>
  )
}
