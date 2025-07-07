import React from 'react'
import CustomerList from '../components/CustomerList'
import AssetSyncButton from '../components/AssetSyncButton'
import TicketsList from '../components/TicketsList'
import UserMenu from '../components/UserMenu'


export default function DistributorHome() {
  return (
    <div className="dashboard">
      <UserMenu />
      <h2>Distributor Dashboard</h2>
      <section>
        <h3>Resellers</h3>
        <CustomerList />
      </section>
      <section>
        <h3>Tickets</h3>
        <TicketsList />
      </section>
      <section>
        <h3>Reports</h3>
        <p>Sales and subscription metrics</p>
      </section>
      <section>
        <h3>Assets</h3>
        <p>Managed licenses and hardware</p>
      </section>
      <section>
        <h3>EDI</h3>
        <p>Exchange data with partners and company</p>
      </section>
      <section>
        <h3>Profile &amp; Security</h3>
        <p>Update password and MFA</p>
      </section>
      <AssetSyncButton />
    </div>
  )
}
