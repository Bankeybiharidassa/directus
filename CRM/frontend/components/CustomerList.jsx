import React, { useEffect, useState } from 'react'
import axios from 'axios'

export default function CustomerList() {
  const [customers, setCustomers] = useState([])

  useEffect(() => {
    axios.get('/customers/').then(res => setCustomers(res.data))
  }, [])

  return (
    <ul>
      {customers.map(c => (
        <li key={c.id}>{c.name} ({c.contact_email})</li>
      ))}
    </ul>
  )
}
