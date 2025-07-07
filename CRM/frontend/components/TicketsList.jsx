import React, { useEffect, useState } from 'react'
import axios from 'axios'

export default function TicketsList() {
  const [tickets, setTickets] = useState([])

  useEffect(() => {
    axios.get('/tickets/').then(res => setTickets(res.data))
  }, [])

  return (
    <ul>
      {tickets.map(t => (
        <li key={t.id}>{t.title} - {t.status}</li>
      ))}
    </ul>
  )
}
