import '../styles/globals.css';
import { useState, useEffect } from 'react';
import Header from '../components/Header';

function MyApp({ Component, pageProps }) {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('access_token');
    if (token) {
      // In a real implementation, we would verify the token and get user info
      // For now, we'll just set a placeholder
      setUser({ id: 1, username: 'admin' });
    }
  }, []);

  return (
    <>
      <Header user={user} setUser={setUser} />
      <Component {...pageProps} user={user} setUser={setUser} />
    </>
  );
}

export default MyApp;