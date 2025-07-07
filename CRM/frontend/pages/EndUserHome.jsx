import React from 'react'
import AssetsList from '../components/AssetsList'
import TicketsList from '../components/TicketsList'
import UserMenu from '../components/UserMenu'

export default function EndUserHome() {
  return (
    <div className="dashboard">
      <UserMenu />
      <h2>End User Dashboard</h2>
      <section>
        <h3>Overview</h3>
        <p>General account summary</p>
      </section>
      <section>
        <h3>Products in Use</h3>
        <p>Active subscriptions</p>
      </section>
      <section>
        <h3>My Assets</h3>
        <AssetsList />
      </section>
      <section>
        <h3>My Tickets</h3>
        <TicketsList />
      </section>
      <section>
        <h3>Change My Products</h3>
        <p>Request upgrades or cancellations</p>
      </section>
      <section>
        <h3>Profile &amp; Security</h3>
        <p>Update login information</p>
      </section>
    </div>
  )
}
