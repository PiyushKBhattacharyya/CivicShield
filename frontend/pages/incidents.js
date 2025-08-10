import { useState, useEffect } from 'react';
import Head from 'next/head';

export default function Incidents({ user }) {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [newIncident, setNewIncident] = useState({
    incident_title: '',
    incident_description: '',
    incident_type: '',
    severity_level: 'Medium',
    priority_level: 'Medium',
    status: 'Open',
    geolocation: ''
  });

  useEffect(() => {
    // In a real implementation, we would fetch data from the backend API
    // For now, we'll use mock data
    const mockIncidents = [
      { 
        id: 1, 
        incident_title: 'Data Breach Investigation', 
        incident_type: 'Cyber Security', 
        severity_level: 'High', 
        priority_level: 'High',
        status: 'In Progress', 
        timestamp: '2023-01-15T09:15:00Z',
        assigned_to: 'John Smith',
        reported_by: 'Security Team'
      },
      { 
        id: 2, 
        incident_title: 'Security Protocol Update', 
        incident_type: 'Administrative', 
        severity_level: 'Medium', 
        priority_level: 'Low',
        status: 'Planned', 
        timestamp: '2023-01-16T14:30:00Z',
        assigned_to: 'Jane Doe',
        reported_by: 'Management'
      },
      { 
        id: 3, 
        incident_title: 'Unauthorized Access Attempt', 
        incident_type: 'Physical Security', 
        severity_level: 'High', 
        priority_level: 'High',
        status: 'Resolved', 
        timestamp: '2023-01-14T11:20:00Z',
        assigned_to: 'Robert Johnson',
        reported_by: 'Security Team'
      },
    ];

    setIncidents(mockIncidents);
    setLoading(false);
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewIncident({
      ...newIncident,
      [name]: value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // In a real implementation, we would submit to the backend API
    console.log('Submitting new incident:', newIncident);
    alert('Incident submitted successfully!');
    setShowForm(false);
    setNewIncident({
      incident_title: '',
      incident_description: '',
      incident_type: '',
      severity_level: 'Medium',
      priority_level: 'Medium',
      status: 'Open',
      geolocation: ''
    });
  };

  if (!user) {
    return (
      <div className="container">
        <Head>
          <title>CivicShield - Incidents</title>
          <meta name="description" content="View and manage incidents" />
        </Head>
        <main>
          <h1>Incidents</h1>
          <p>Please log in to view incidents.</p>
        </main>
      </div>
    );
  }

  return (
    <div className="container">
      <Head>
        <title>CivicShield - Incidents</title>
        <meta name="description" content="View and manage incidents" />
      </Head>

      <main>
        <div className="header">
          <h1>Incident Management</h1>
          <button onClick={() => setShowForm(!showForm)}>
            {showForm ? 'Cancel' : 'New Incident'}
          </button>
        </div>

        {showForm && (
          <div className="form-card">
            <h2>Create New Incident</h2>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="incident_title">Incident Title</label>
                <input
                  type="text"
                  id="incident_title"
                  name="incident_title"
                  value={newIncident.incident_title}
                  onChange={handleInputChange}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="incident_description">Description</label>
                <textarea
                  id="incident_description"
                  name="incident_description"
                  value={newIncident.incident_description}
                  onChange={handleInputChange}
                  rows="3"
                />
              </div>

              <div className="form-group">
                <label htmlFor="incident_type">Incident Type</label>
                <select
                  id="incident_type"
                  name="incident_type"
                  value={newIncident.incident_type}
                  onChange={handleInputChange}
                  required
                >
                  <option value="">Select a type</option>
                  <option value="Cyber Security">Cyber Security</option>
                  <option value="Physical Security">Physical Security</option>
                  <option value="Natural Disaster">Natural Disaster</option>
                  <option value="Civil Unrest">Civil Unrest</option>
                  <option value="Administrative">Administrative</option>
                </select>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="severity_level">Severity Level</label>
                  <select
                    id="severity_level"
                    name="severity_level"
                    value={newIncident.severity_level}
                    onChange={handleInputChange}
                  >
                    <option value="Low">Low</option>
                    <option value="Medium">Medium</option>
                    <option value="High">High</option>
                    <option value="Critical">Critical</option>
                  </select>
                </div>

                <div className="form-group">
                  <label htmlFor="priority_level">Priority Level</label>
                  <select
                    id="priority_level"
                    name="priority_level"
                    value={newIncident.priority_level}
                    onChange={handleInputChange}
                  >
                    <option value="Low">Low</option>
                    <option value="Medium">Medium</option>
                    <option value="High">High</option>
                    <option value="Urgent">Urgent</option>
                  </select>
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="status">Status</label>
                <select
                  id="status"
                  name="status"
                  value={newIncident.status}
                  onChange={handleInputChange}
                >
                  <option value="Open">Open</option>
                  <option value="In Progress">In Progress</option>
                  <option value="Resolved">Resolved</option>
                  <option value="Closed">Closed</option>
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="geolocation">Geolocation</label>
                <input
                  type="text"
                  id="geolocation"
                  name="geolocation"
                  value={newIncident.geolocation}
                  onChange={handleInputChange}
                  placeholder="lat,lng"
                />
              </div>

              <button type="submit">Submit Incident</button>
            </form>
          </div>
        )}

        <div className="incidents-list">
          <h2>Current Incidents</h2>
          {loading ? (
            <p>Loading incidents...</p>
          ) : incidents.length === 0 ? (
            <p>No incidents found.</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Type</th>
                  <th>Severity</th>
                  <th>Priority</th>
                  <th>Status</th>
                  <th>Assigned To</th>
                  <th>Reported By</th>
                  <th>Date</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {incidents.map(incident => (
                  <tr key={incident.id}>
                    <td>{incident.incident_title}</td>
                    <td>{incident.incident_type}</td>
                    <td>
                      <span className={`severity ${incident.severity_level.toLowerCase()}`}>
                        {incident.severity_level}
                      </span>
                    </td>
                    <td>{incident.priority_level}</td>
                    <td>
                      <span className={`status ${incident.status.toLowerCase().replace(' ', '-')}`}>
                        {incident.status}
                      </span>
                    </td>
                    <td>{incident.assigned_to}</td>
                    <td>{incident.reported_by}</td>
                    <td>{new Date(incident.timestamp).toLocaleDateString()}</td>
                    <td>
                      <button className="action-btn">View</button>
                      <button className="action-btn">Edit</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </main>

      <style jsx>{`
        .container {
          min-height: 100vh;
          padding: 0 2rem;
        }

        main {
          padding: 2rem 0;
        }

        .header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 2rem;
        }

        h1 {
          color: #333;
        }

        h2 {
          color: #555;
          margin-bottom: 1rem;
        }

        button {
          background: #0070f3;
          color: white;
          border: none;
          padding: 0.5rem 1rem;
          border-radius: 4px;
          cursor: pointer;
        }

        button:hover {
          background: #0051cc;
        }

        .form-card {
          background: white;
          border-radius: 8px;
          padding: 2rem;
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
          margin-bottom: 2rem;
        }

        .form-group {
          margin-bottom: 1.5rem;
        }

        .form-row {
          display: flex;
          gap: 1rem;
        }

        label {
          display: block;
          margin-bottom: 0.5rem;
          font-weight: 500;
        }

        input, select, textarea {
          width: 100%;
          padding: 0.75rem;
          border: 1px solid #ddd;
          border-radius: 4px;
          font-size: 1rem;
        }

        input:focus, select:focus, textarea:focus {
          outline: none;
          border-color: #0070f3;
        }

        table {
          width: 100%;
          border-collapse: collapse;
          background: white;
          border-radius: 8px;
          overflow: hidden;
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        th, td {
          padding: 1rem;
          text-align: left;
          border-bottom: 1px solid #eee;
        }

        th {
          background: #f8f9fa;
          font-weight: 600;
        }

        .severity {
          padding: 0.25rem 0.5rem;
          border-radius: 4px;
          font-size: 0.8rem;
          font-weight: 500;
        }

        .severity.low {
          background: #e8f5e9;
          color: #2e7d32;
        }

        .severity.medium {
          background: #fff8e1;
          color: #f57f17;
        }

        .severity.high {
          background: #ffebee;
          color: #c62828;
        }

        .severity.critical {
          background: #ffccbc;
          color: #bf360c;
        }

        .status {
          padding: 0.25rem 0.5rem;
          border-radius: 4px;
          font-size: 0.8rem;
          font-weight: 500;
        }

        .status.open {
          background: #e3f2fd;
          color: #1565c0;
        }

        .status.in-progress {
          background: #f3e5f5;
          color: #6a1b9a;
        }

        .status.resolved {
          background: #e8f5e9;
          color: #2e7d32;
        }

        .status.closed {
          background: #eeeeee;
          color: #616161;
        }

        .action-btn {
          background: #f5f5f5;
          color: #333;
          border: none;
          padding: 0.25rem 0.5rem;
          border-radius: 4px;
          cursor: pointer;
          margin-right: 0.5rem;
          font-size: 0.875rem;
        }

        .action-btn:hover {
          background: #e0e0e0;
        }
      `}</style>
    </div>
  );
}