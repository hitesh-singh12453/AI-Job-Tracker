
import { useState, useEffect } from 'react'
import './App.css'

function StatCard({ title, value }) {
  return (
    <div className="stat-card">
      <p className="stat-title">{title}</p>
      <h2 className="stat-value">{value}</h2>
    </div>
  )
}

function App() {


  const [applications, setApplications] = useState([])
  const [showForm, setShowForm] = useState(false)
  const [company, setCompany] = useState('')
  const [role, setRole] = useState('')
  const [status, setStatus] = useState('Applied')
  const [editingId, setEditingId] = useState(null)
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [token, setToken] = useState(
    () => localStorage.getItem('token')
  )
  const [loading, setLoading] = useState(false)
  const [location, setLocation] = useState('')
  const [jobType, setJobType] = useState('')
  const [salary, setSalary] = useState('')
  const [description, setDescription] = useState('')
  const [notes, setNotes] = useState('')
  const [jobUrl, setJobUrl] = useState('')
  const [appliedDate, setAppliedDate] = useState('')
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('All')
  const [sortBy, setSortBy] = useState('newest')
  const [currentPage, setCurrentPage] = useState(1)
  useEffect(() => {
    setCurrentPage(1)
  }, [searchTerm, statusFilter, sortBy])
  const [error, setError] = useState('')
  const [deletingId, setDeletingId] = useState(null)
  const [successMessage, setSuccessMessage] = useState('')
  useEffect(() => {
    if (!successMessage) return

    const timer = setTimeout(() => {
      setSuccessMessage('')
    }, 3000)

    return () => clearTimeout(timer)
  }, [successMessage])


  async function handleLogin(e) {
    e.preventDefault()
    setError('')

    try {
      const formData = new URLSearchParams()

      formData.append('username', username)
      formData.append('password', password)

      const response = await fetch(
        'http://127.0.0.1:8000/auth/login',
        {
          method: 'POST',
          body: formData,
        }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Invalid username or password')
      }

      localStorage.setItem('token', data.access_token)
      setToken(data.access_token)

    } catch (error) {
      console.error('Login error:', error)

      if (error instanceof TypeError) {
        setError('Cannot connect to the backend. Please check if FastAPI is running.')
      } else {
        setError(error.message)
      }
    }
  }
  function handleLogout() {
    localStorage.removeItem('token')
    setToken(null)
    setApplications([])
    setUsername('')
    setPassword('')
  }

  async function fetchApplications() {
    try {
      setLoading(true)

      const response = await fetch(
        'http://127.0.0.1:8000/applications/',
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )

      if (!response.ok) {
        throw new Error('Failed to fetch applications')
      }

      const data = await response.json()
      setApplications(data)
    } catch (error) {
      console.error('Error:', error)
      alert('Could not load applications')
    }
    finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (token) {
      fetchApplications()
    }
  }, [token])

  function handleClick() {
    setEditingId(null)
    setCompany('')
    setRole('')
    setStatus('Applied')
    setShowForm(true)
    setError('')
  }

  async function handleSubmit(e) {
    e.preventDefault()

    if (!company.trim() || !role.trim()) {
      setError('Please enter both company name and job role.')
      return
    }

    setError('')
    setSuccessMessage('')
    setLoading(true)


    if (editingId !== null) {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/applications/${editingId}`,
          {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
              company,
              role,
              location,
              job_type: jobType,
              salary: Number(salary) || 0,
              status,
              description,
              notes,
              job_url: jobUrl,
              applied_date:
                appliedDate || new Date().toISOString().slice(0, 10),
            }),
          }
        )

        if (!response.ok) {
          throw new Error('Failed to update application')
        }

        const updatedApplication = await response.json()

        setApplications((prev) =>
          prev.map((application) =>
            application.id === editingId
              ? updatedApplication
              : application
          )
        )

        setSuccessMessage('Application updated successfully!')
      } catch (error) {
        console.error('Error:', error)
        setError('Could not update application. Please try again.')
        setLoading(false)
        return
      }
    }

    else {
      try {
        const response = await fetch(
          'http://127.0.0.1:8000/applications/',
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
              company,
              role,
              location,
              job_type: jobType,
              salary: Number(salary) || 0,
              status,
              description,
              notes,
              job_url: jobUrl,
              applied_date:
                appliedDate || new Date().toISOString().slice(0, 10),
            }),
          }
        )

        if (!response.ok) {
          throw new Error('Failed to create application')
        }

        const newApplication = await response.json()

        setApplications((prev) => [newApplication, ...prev])

        setSuccessMessage('Application added successfully!')
      }
      catch (error) {
        console.error('Error:', error)
        setError('Could not add application. Please try again.')
        setLoading(false)
        return
      }
    }
    setLoading(false)

    setCompany('')
    setRole('')
    setStatus('Applied')
    setLocation('')
    setJobType('')
    setSalary('')
    setDescription('')
    setNotes('')
    setJobUrl('')
    setAppliedDate('')
    setEditingId(null)
    setShowForm(false)
  }


  async function handleDelete(id) {
    setError('')
    setSuccessMessage('')
    const confirmDelete = window.confirm(
      'Are you sure you want to delete this application?'
    )

    if (!confirmDelete) {
      return
    }
    setDeletingId(id)

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/applications/${id}`,
        {
          method: 'DELETE',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )

      if (!response.ok) {
        throw new Error('Failed to delete application')
      }

      setApplications((prev) =>
        prev.filter((application) => application.id !== id)
      )

      setSuccessMessage('Application deleted successfully!')
    } catch (error) {
      console.error('Error:', error)
      setError('Could not delete application. Please try again.')
    }
    finally {
      setDeletingId(null)
    }
  }


  function handleEdit(application) {
    setEditingId(application.id)

    setCompany(application.company)
    setRole(application.role)
    setStatus(application.status)

    setLocation(application.location || '')
    setJobType(application.job_type || '')
    setSalary(application.salary ?? '')
    setDescription(application.description || '')
    setNotes(application.notes || '')
    setJobUrl(application.job_url || '')
    setAppliedDate(application.applied_date || '')

    setShowForm(true)
  }


  const totalApplications = applications.length


  const interviewCount = applications.filter(
    (application) => application.status === 'Interview'
  ).length

  const offerCount = applications.filter(
    (application) => application.status === 'Offer'
  ).length

  const rejectedCount = applications.filter(
    (application) => application.status === 'Rejected'
  ).length

  // login screen 
  if (token === null) {
    return (
      <div className="login-page">
        <form className="login-card" onSubmit={handleLogin}>
          <div className="login-header">
            <h1>AI Job Tracker</h1>
            <p>Welcome back! Sign in to manage your job applications.</p>
          </div>

          {error && (
            <p className="error-message">{error}</p>
          )}

          <div className="login-fields">
            <label>Username</label>
            <input
              type="text"
              placeholder="Enter your username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />

            <label>Password</label>
            <input
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button type="submit" className="login-button">
            Login
          </button>

          <p className="login-footer">
            AI Job Tracker · Track your career journey
          </p>
        </form>
      </div>
    )
  }

  const filteredApplications = applications.filter((application) => {
    const matchesSearch =
      application.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
      application.role.toLowerCase().includes(searchTerm.toLowerCase())

    const matchesStatus =
      statusFilter === 'All' || application.status === statusFilter

    return matchesSearch && matchesStatus
  })
  const sortedApplications = [...filteredApplications].sort((a, b) => {
    if (sortBy === 'newest') {
      return new Date(b.applied_date) - new Date(a.applied_date)
    }

    if (sortBy === 'oldest') {
      return new Date(a.applied_date) - new Date(b.applied_date)
    }

    if (sortBy === 'company-asc') {
      return a.company.localeCompare(b.company)
    }

    if (sortBy === 'company-desc') {
      return b.company.localeCompare(a.company)
    }

    return 0
  })

  const itemsPerPage = 5

  const totalPages = Math.ceil(
    sortedApplications.length / itemsPerPage
  )

  const startIndex = (currentPage - 1) * itemsPerPage

  const currentApplications = sortedApplications.slice(
    startIndex,
    startIndex + itemsPerPage
  )

  return (

    <div className="dashboard">
      <header className="dashboard-header">
        <div className="dashboard-heading">
          <h1>AI Job Tracker</h1>
          <p>Track and manage your job applications.</p>
        </div>

        <button
          type="button"
          className="logout-button"
          onClick={handleLogout}
        >
          Logout
        </button>
      </header>

      <div className="dashboard-actions">
        <button className="add-button" onClick={handleClick}>
          + Add Application
        </button>
      </div>
      {successMessage && (
        <p className="success-message">{successMessage}</p>
      )}
      {showForm && (
        <form className="application-form" onSubmit={handleSubmit}>
          <h2>
            {editingId !== null ? 'Edit Application' : 'Add New Application'}
          </h2>
          {error && (
            <p className="error-message">{error}</p>
          )}
          <input
            type="text"
            placeholder="Company Name"
            value={company}
            onChange={(e) => {
              setCompany(e.target.value)
              setError('')
            }}

          />
          <input
            type="text"
            placeholder="Job Role"
            value={role}
            onChange={(e) => {
              setRole(e.target.value)
              setError('')
            }}

          />
          <select
            value={status}
            onChange={(e) => setStatus(e.target.value)}
          >
            <option value="Applied">Applied</option>
            <option value="Interview">Interview</option>
            <option value="Offer">Offer</option>
            <option value="Rejected">Rejected</option>
          </select>

          <input
            type="text"
            placeholder="Location"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
          />

          <input
            type="text"
            placeholder="Job Type"
            value={jobType}
            onChange={(e) => setJobType(e.target.value)}
          />

          <input
            type="number"
            placeholder="Salary"
            value={salary}
            onChange={(e) => setSalary(e.target.value)}
          />

          <textarea
            placeholder="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />

          <textarea
            placeholder="Notes"
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
          />

          <input
            type="url"
            placeholder="Job URL"
            value={jobUrl}
            onChange={(e) => setJobUrl(e.target.value)}
          />

          <input
            type="date"
            value={appliedDate}
            onChange={(e) => setAppliedDate(e.target.value)}
          />

          <button
            type="submit"
            className="save-button"
            disabled={loading}
          >
            {loading
              ? 'Saving...'
              : editingId !== null
                ? 'Update Application'
                : 'Save Application'}
          </button>
          <button
            type="button"
            className="cancel-button"
            onClick={() => {
              setCompany('')
              setRole('')
              setStatus('Applied')
              setShowForm(false)
              setEditingId(null)
            }}
          >
            Cancel
          </button>
        </form>
      )}

      <section className="stats-grid">
        <StatCard
          title="Total Applications"
          value={totalApplications}
        />

        <StatCard
          title="Interviews"
          value={interviewCount}
        />

        <StatCard
          title="Offers"
          value={offerCount}
        />

        <StatCard
          title="Rejected"
          value={rejectedCount}
        />
      </section>

      <section className="applications-section">
        <h2>Recent Applications</h2>
        {error && (
          <p className="error-message">{error}</p>
        )}
        <input
          type="text"
          placeholder="Search by company or job role..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="status-filter"
        >

          <option value="All">All Statuses</option>
          <option value="Applied">Applied</option>
          <option value="Interview">Interview</option>
          <option value="Offer">Offer</option>
          <option value="Rejected">Rejected</option>
        </select>
        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          className="sort-filter"
        >
          <option value="newest">Newest First</option>
          <option value="oldest">Oldest First</option>
          <option value="company-asc">Company (A–Z)</option>
          <option value="company-desc">Company (Z–A)</option>
        </select>
        <div className="applications-list">
          {loading ? (
            <p>Loading applications...</p>
          ) : applications.length === 0 ? (
            <p>No applications found. Add your first application!</p>
          ) : filteredApplications.length === 0 ? (
            <p>No matching applications found.</p>
          ) : (
            currentApplications.map((application) => (
              <div
                className="application-card"
                key={application.id}
              >
                <div>
                  <h3>{application.company}</h3>
                  <p>{application.role}</p>
                </div>

                <span className={`status status-${application.status}`}>
                  {application.status}
                </span>
                <div className="application-actions">
                  <button
                    type="button"
                    className="edit-button"
                    onClick={() => handleEdit(application)}
                  >
                    Edit
                  </button>

                  <button
                    type="button"
                    className="delete-button"
                    onClick={() => handleDelete(application.id)}
                    disabled={deletingId === application.id}
                  >
                    {deletingId === application.id ? 'Deleting...' : 'Delete'}
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
        {totalPages > 0 && (
          <div className="pagination">
            <div className="pagination">
              <button
                type="button"
                onClick={() => setCurrentPage((prev) => prev - 1)}
                disabled={currentPage === 1}
              >
                Previous
              </button>

              <span>
                Page {currentPage} of {totalPages}
              </span>

              <button
                type="button"
                onClick={() => setCurrentPage((prev) => prev + 1)}
                disabled={currentPage === totalPages}
              >
                Next
              </button>
            </div>
          </div>
        )}

      </section>
    </div>
  )
}

export default App