import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { Navbar } from './components/Navbar';
import { Footer } from './components/Footer';
import { AppRoutes } from './routes/AppRoutes';
import { authService } from './services/authService';
import { User } from './types';

export const App: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loadingAuth, setLoadingAuth] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      try {
        const currentUser = await authService.getCurrentUser();
        setUser(currentUser);
      } catch {
        setUser(null);
      } finally {
        setLoadingAuth(false);
      }
    };
    initAuth();
  }, []);

  const handleLoginSuccess = (loggedInUser: User) => {
    setUser(loggedInUser);
  };

  const handleLogout = async () => {
    await authService.logout();
    setUser(null);
  };

  if (loadingAuth) {
    return (
      <div className="min-h-screen bg-[#fbfcf9] flex items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <div className="w-12 h-12 rounded-2xl bg-agro-900 text-green-400 flex items-center justify-center shadow-lg animate-pulse">
            <span className="font-extrabold text-lg">AI</span>
          </div>
          <p className="text-xs font-bold text-gray-500 uppercase tracking-wider">
            Loading AGRO AI Platform...
          </p>
        </div>
      </div>
    );
  }

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
