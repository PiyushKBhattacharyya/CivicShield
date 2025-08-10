import { useState, useEffect } from 'react';
import Head from 'next/head';

export default function Home({ user }) {
  const [threats, setThreats] = useState([]);
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In a real implementation, we would fetch data from the backend API
    // For now, we'll use mock data
    const mockThreats = [
      { id: 1, title: 'Cyber Attack Detected', severity: 'High', status: 'Active', timestamp: '2023-01-15T10:30:00Z' },
      { id: 2, title: 'Social Unrest Reported', severity: 'Medium', status: 'Monitoring', timestamp: '2023-01-14T15:45:00Z' },
      { id: 3, title: 'Natural Disaster Warning', severity: 'Low', status: 'Resolved', timestamp: '2023-01-13T08:20:00Z' },
    ];

    const mockIncidents = [
      { id: 1, title: 'Data Breach Investigation', priority: 'High', status: 'In Progress', timestamp: '2023-01-15T09:15:00Z' },
      { id: 2, title: 'Security Protocol Update', priority: 'Medium', status: 'Planned', timestamp: '2023-01-16T14:30:00Z' },
    ];

    setThreats(mockThreats);
    setIncidents(mockIncidents);
    setLoading(false);
  }, []);

  if (!user) {
    return (
      <div className="container">
        <Head>
          <title>CivicShield - Login</title>
          <meta name="description" content="AI-Driven Threat Detection & Crisis Management Platform" />
        </Head>

        <main>
          <h1>Welcome to CivicShield</h1>
          <p>Please log in to access the dashboard.</p>
          <button onClick={() => {
            // In a real implementation, this would redirect to a login page
            alert('Login functionality would be implemented here');
          }}>
            Login
          </button>
        </main>
      </div>
    );
  }

  return (
    <div className="container">
      <Head>
        <title>CivicShield - Dashboard</title>
        <meta name="description" content="AI-Driven Threat Detection & Crisis Management Platform" />
      </Head>

      <main>
        <h1>CivicShield Dashboard</h1>
        
        <div className="dashboard-grid">
          <div className="card">
            <h2>Active Threats</h2>
            {loading ? (
              <p>Loading...</p>
            ) : (
              <ul>
                {threats.map(threat => (
                  <li key={threat.id} className={`threat-${threat.severity.toLowerCase()}`}>
                    <strong>{threat.title}</strong> - {threat.status}
                    <br />
                    <small>{new Date(threat.timestamp).toLocaleString()}</small>
                  </li>
                ))}
              </ul>
            )}
          </div>

          <div className="card">
            <h2>Current Incidents</h2>
            {loading ? (
              <p>Loading...</p>
            ) : (
              <ul>
                {incidents.map(incident => (
                  <li key={incident.id} className={`incident-${incident.priority.toLowerCase()}`}>
                    <strong>{incident.title}</strong> - {incident.status}
                    <br />
                    <small>{new Date(incident.timestamp).toLocaleString()}</small>
                  </li>
                ))}
              </ul>
            )}
          </div>

          <div className="card">
            <h2>Quick Actions</h2>
            <button>Create New Threat Report</button>
            <button>Create New Incident</button>
            <button>View Analytics</button>
          </div>
        </div>
      </main>

      <style jsx>{`
        .container {
          min-height: 100vh;
          padding: 0 0.5rem;
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
        }

        main {
          padding: 5rem 0;
          flex: 1;
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
        }

        .dashboard-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 2rem;
          width: 100%;
          max-width: 1200px;
        }

        .card {
          background: #f5f5f5;
          border-radius: 8px;
          padding: 1.5rem;
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .threat-high {
          color: #d32f2f;
        }

        .threat-medium {
          color: #f57c00;
        }

        .threat-low {
          color: #388e3c;
        }

        .incident-high {
          color: #d32f2f;
        }

        .incident-medium {
          color: #f57c00;
        }

        button {
          background: #0070f3;
          color: white;
          border: none;
          padding: 0.5rem 1rem;
          border-radius: 4px;
          cursor: pointer;
          margin: 0.5rem 0;
        }

        button:hover {
          background: #0051cc;
        }
      `}</style>
    </div>
  );
}