import React from 'react'
import SecurityScan from '../components/SecurityScan'
import AssetSyncButton from '../components/AssetSyncButton'
import CustomerList from '../components/CustomerList'
import UserMenu from '../components/UserMenu'

export default function CompanyHome() {
  return (
    <div className="dashboard">
      <UserMenu />
      <h2>Company Dashboard</h2>
      <section>
        <h3>Internal News</h3>
        <p>Latest company announcements...</p>
      </section>
      <section>
        <h3>Customers</h3>
        <CustomerList />
      </section>
      <section>
        <h3>CRM</h3>
        <p>Customer relationship management tools</p>
      </section>
      <section>
        <h3>CMS</h3>
        <p>Manage website content</p>
      </section>
      <section>
        <h3>Finance</h3>
        <p>Invoices and reports</p>
      </section>
      <section>
        <h3>Import/Export</h3>
        <p>Data import and export utilities</p>
      </section>
      <section>
        <h3>Email</h3>
        <p>Company email settings</p>
      </section>
      <section>
        <h3>Agenda</h3>
        <p>Upcoming events and meetings</p>
      </section>
      <section>
        <h3>Knowledgebase</h3>
        <p>Documentation and help articles</p>
      </section>
      <section>
        <h3>Support</h3>
        <p>Contact support or open a ticket</p>
      </section>
      <AssetSyncButton />
      <SecurityScan />
    </div>
  )
}
