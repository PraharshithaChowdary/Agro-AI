import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { Navbar } from './components/Navbar';
import { Footer } from './components/Footer';
import { AppRoutes } from './routes/AppRoutes';
import { authService } from './services/authService';
import { User } from './types';

export const App: React.FC = () => {
  // Synchronous initialization prevents slow loading delays and jarring flashes
  const [user, setUser] = useState<User | null>(() => {
    try {
      const cached = localStorage.getItem('agro_user');
      const token = localStorage.getItem('agro_token');
      if (token && cached) {
        return JSON.parse(cached);
      }
      return null;
    } catch {
      return null;
    }
  });

  useEffect(() => {
    // Non-blocking background verification of current token
    const verifySession = async () => {
      try {
        const currentUser = await authService.getCurrentUser();
        setUser(currentUser);
      } catch {
        // If unauthenticated or token expired, clear session
        setUser(null);
      }
    };
    verifySession();
  }, []);

  const handleLoginSuccess = (loggedInUser: User) => {
    setUser(loggedInUser);
  };

  const handleLogout = async () => {
    await authService.logout();
    setUser(null);
  };

  return (
    <Router>
      <div className="flex flex-col min-h-screen">
        <Navbar user={user} onLogout={handleLogout} />
        <main className="flex-1">
          <AppRoutes
            user={user}
            onLoginSuccess={handleLoginSuccess}
            onLogout={handleLogout}
          />
        </main>
        <Footer />
      </div>
    </Router>
  );
};

export default App;
