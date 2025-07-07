import React from 'react'
import TicketsList from '../components/TicketsList'
import UserMenu from '../components/UserMenu'

export default function SupportHome() {
  return (
    <div className="dashboard">
      <UserMenu />
      <h2>Support Overview</h2>
      <section>
        <h3>Tickets</h3>
        <TicketsList />
      </section>
      <section>
        <h3>Knowledgebase</h3>
        <p>Browse help articles</p>
      </section>
      <section>
        <h3>Remote Control</h3>
        <p>Authorize remote assistance</p>
      </section>
      <section>
        <h3>Integrations</h3>
        <p>Link to external tools</p>
      </section>
    </div>
  )
}
