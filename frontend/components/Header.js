import Link from 'next/link';
import { useRouter } from 'next/router';

export default function Header({ user, setUser }) {
  const router = useRouter();

  const handleLogout = () => {
    // In a real implementation, we would also invalidate the token on the backend
    localStorage.removeItem('access_token');
    setUser(null);
    router.push('/login');
  };

  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">
          <Link href="/">
            <a>CivicShield</a>
          </Link>
        </div>
        
        {user && (
          <nav className="nav-links">
            <Link href="/">
              <a className={`nav-link ${router.pathname === '/' ? 'active' : ''}`}>
                Dashboard
              </a>
            </Link>
            <Link href="/threats">
              <a className={`nav-link ${router.pathname === '/threats' ? 'active' : ''}`}>
                Threats
              </a>
            </Link>
            <Link href="/incidents">
              <a className={`nav-link ${router.pathname === '/incidents' ? 'active' : ''}`}>
                Incidents
              </a>
            </Link>
            <Link href="/analytics">
              <a className={`nav-link ${router.pathname === '/analytics' ? 'active' : ''}`}>
                Analytics
              </a>
            </Link>
          </nav>
        )}
        
        {user && (
          <div className="user-menu">
            <div className="user-avatar">
              {user.username.charAt(0).toUpperCase()}
            </div>
            <span>{user.username}</span>
            <button className="logout-btn" onClick={handleLogout}>
              Logout
            </button>
          </div>
        )}
      </div>
      
      <style jsx>{`
        .header {
          background: white;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
          padding: 1rem 2rem;
          position: sticky;
          top: 0;
          z-index: 100;
        }
        
        .header-content {
          display: flex;
          justify-content: space-between;
          align-items: center;
          max-width: 1200px;
          margin: 0 auto;
        }
        
        .logo a {
          font-size: 1.5rem;
          font-weight: bold;
          color: #0070f3;
        }
        
        .nav-links {
          display: flex;
          gap: 2rem;
        }
        
        .nav-link {
          color: #333;
          font-weight: 500;
          padding: 0.5rem 1rem;
          border-radius: 4px;
          transition: background-color 0.2s;
        }
        
        .nav-link:hover {
          background-color: #f5f5f5;
        }
        
        .nav-link.active {
          background-color: #0070f3;
          color: white;
        }
        
        .user-menu {
          display: flex;
          align-items: center;
          gap: 1rem;
        }
        
        .user-avatar {
          width: 32px;
          height: 32px;
          border-radius: 50%;
          background-color: #0070f3;
          color: white;
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: bold;
        }
        
        .logout-btn {
          background: none;
          border: none;
          color: #0070f3;
          cursor: pointer;
          font-size: 1rem;
        }
        
        .logout-btn:hover {
          text-decoration: underline;
        }
        
        @media (max-width: 768px) {
          .header-content {
            flex-direction: column;
            gap: 1rem;
          }
          
          .nav-links {
            flex-wrap: wrap;
            justify-content: center;
          }
        }
      `}</style>
    </header>
  );
}