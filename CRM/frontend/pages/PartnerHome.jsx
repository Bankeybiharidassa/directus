import React from 'react'
import CustomerList from '../components/CustomerList'
import AssetSyncButton from '../components/AssetSyncButton'
import TicketsList from '../components/TicketsList'
import UserMenu from '../components/UserMenu'

export default function PartnerHome() {
  return (
    <div className="dashboard">
      <UserMenu />
      <h2>Partner Dashboard</h2>
      <section>
        <h3>End Users</h3>
        <CustomerList />
      </section>
      <section>
        <h3>Tickets</h3>
        <TicketsList />
      </section>
      <section>
        <h3>Reports</h3>
        <p>Revenue and service usage</p>
      </section>
      <section>
        <h3>Assets</h3>
        <p>Licenses and hardware assignments</p>
      </section>
      <section>
        <h3>EDI</h3>
        <p>Exchange data with distributor</p>
      </section>
      <section>
        <h3>Profile &amp; Security</h3>
        <p>Update login and MFA settings</p>
      </section>
      <AssetSyncButton />
    </div>
  )
}
