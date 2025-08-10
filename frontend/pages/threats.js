import { useState, useEffect } from 'react';
import Head from 'next/head';

export default function Threats({ user }) {
  const [threats, setThreats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [newThreat, setNewThreat] = useState({
    threat_title: '',
    threat_description: '',
    threat_type: '',
    severity_score: 5,
    confidence_score: 5,
    geolocation: ''
  });

  useEffect(() => {
    // In a real implementation, we would fetch data from the backend API
    // For now, we'll use mock data
    const mockThreats = [
      { 
        id: 1, 
        threat_title: 'Cyber Attack Detected', 
        threat_type: 'Cyber', 
        severity_score: 8.5, 
        confidence_score: 9.2,
        status: 'Active', 
        timestamp: '2023-01-15T10:30:00Z',
        assigned_to: 'John Smith'
      },
      { 
        id: 2, 
        threat_title: 'Social Unrest Reported', 
        threat_type: 'Civil Unrest', 
        severity_score: 6.2, 
        confidence_score: 7.8,
        status: 'Monitoring', 
        timestamp: '2023-01-14T15:45:00Z',
        assigned_to: 'Jane Doe'
      },
      { 
        id: 3, 
        threat_title: 'Natural Disaster Warning', 
        threat_type: 'Natural Disaster', 
        severity_score: 7.1, 
        confidence_score: 8.5,
        status: 'Resolved', 
        timestamp: '2023-01-13T08:20:00Z',
        assigned_to: 'Robert Johnson'
      },
    ];

    setThreats(mockThreats);
    setLoading(false);
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewThreat({
      ...newThreat,
      [name]: value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // In a real implementation, we would submit to the backend API
    console.log('Submitting new threat:', newThreat);
    alert('Threat submitted successfully!');
    setShowForm(false);
    setNewThreat({
      threat_title: '',
      threat_description: '',
      threat_type: '',
      severity_score: 5,
      confidence_score: 5,
      geolocation: ''
    });
  };

  if (!user) {
    return (
      <div className="container">
        <Head>
          <title>CivicShield - Threats</title>
          <meta name="description" content="View and manage threats" />
        </Head>
        <main>
          <h1>Threats</h1>
          <p>Please log in to view threats.</p>
        </main>
      </div>
    );
  }

  return (
    <div className="container">
      <Head>
        <title>CivicShield - Threats</title>
        <meta name="description" content="View and manage threats" />
      </Head>

      <main>
        <div className="header">
          <h1>Threat Management</h1>
          <button onClick={() => setShowForm(!showForm)}>
            {showForm ? 'Cancel' : 'New Threat'}
          </button>
        </div>

        {showForm && (
          <div className="form-card">
            <h2>Create New Threat</h2>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="threat_title">Threat Title</label>
                <input
                  type="text"
                  id="threat_title"
                  name="threat_title"
                  value={newThreat.threat_title}
                  onChange={handleInputChange}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="threat_description">Description</label>
                <textarea
                  id="threat_description"
                  name="threat_description"
                  value={newThreat.threat_description}
                  onChange={handleInputChange}
                  rows="3"
                />
              </div>

              <div className="form-group">
                <label htmlFor="threat_type">Threat Type</label>
                <select
                  id="threat_type"
                  name="threat_type"
                  value={newThreat.threat_type}
                  onChange={handleInputChange}
                  required
                >
                  <option value="">Select a type</option>
                  <option value="Cyber">Cyber</option>
                  <option value="Physical">Physical</option>
                  <option value="Natural Disaster">Natural Disaster</option>
                  <option value="Civil Unrest">Civil Unrest</option>
                  <option value="Intelligence">Intelligence</option>
                </select>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="severity_score">Severity Score (0-10)</label>
                  <input
                    type="number"
                    id="severity_score"
                    name="severity_score"
                    value={newThreat.severity_score}
                    onChange={handleInputChange}
                    min="0"
                    max="10"
                    step="0.1"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="confidence_score">Confidence Score (0-10)</label>
                  <input
                    type="number"
                    id="confidence_score"
                    name="confidence_score"
                    value={newThreat.confidence_score}
                    onChange={handleInputChange}
                    min="0"
                    max="10"
                    step="0.1"
                  />
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="geolocation">Geolocation</label>
                <input
                  type="text"
                  id="geolocation"
                  name="geolocation"
                  value={newThreat.geolocation}
                  onChange={handleInputChange}
                  placeholder="lat,lng"
                />
              </div>

              <button type="submit">Submit Threat</button>
            </form>
          </div>
        )}

        <div className="threats-list">
          <h2>Active Threats</h2>
          {loading ? (
            <p>Loading threats...</p>
          ) : threats.length === 0 ? (
            <p>No active threats found.</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Type</th>
                  <th>Severity</th>
                  <th>Confidence</th>
                  <th>Status</th>
                  <th>Assigned To</th>
                  <th>Date</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {threats.map(threat => (
                  <tr key={threat.id}>
                    <td>{threat.threat_title}</td>
                    <td>{threat.threat_type}</td>
                    <td>{threat.severity_score}</td>
                    <td>{threat.confidence_score}</td>
                    <td>
                      <span className={`status ${threat.status.toLowerCase()}`}>
                        {threat.status}
                      </span>
                    </td>
                    <td>{threat.assigned_to}</td>
                    <td>{new Date(threat.timestamp).toLocaleDateString()}</td>
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

        .status {
          padding: 0.25rem 0.5rem;
          border-radius: 4px;
          font-size: 0.8rem;
          font-weight: 500;
        }

        .status.active {
          background: #ffebee;
          color: #c62828;
        }

        .status.monitoring {
          background: #fff8e1;
          color: #f57f17;
        }

        .status.resolved {
          background: #e8f5e9;
          color: #2e7d32;
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