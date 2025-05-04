import React, { Component } from 'react';
import { Routes, Route, NavLink } from 'react-router-dom';
import Indexing from './pages/Indexing';
import ViewIndex from './pages/ViewIndex';
import Search from './pages/Search';
import './App.css';

class ErrorBoundary extends Component {
  state = { hasError: false };

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, info) {
    console.error('ErrorBoundary caught:', error, info);
  }

  render() {
    if (this.state.hasError) {
      return <h1>Something went wrong. Check console for details.</h1>;
    }
    return this.props.children;
  }
}

function App() {
  console.log('App.jsx rendered');
  return (
    <ErrorBoundary>
      <div className="app-container">
        <nav className="app-nav">
          <div className="app-nav-brand">TF-IDF Search</div>
          <ul className="app-nav-list">
            <li className="app-nav-item">
              <NavLink
                to="/"
                className={({ isActive }) => `app-nav-link ${isActive ? 'app-nav-link-active' : ''}`}
                end
                onClick={() => console.log('Navigating to Indexing')}
              >
                Indexing
              </NavLink>
            </li>
            <li className="app-nav-item">
              <NavLink
                to="/view-index"
                className={({ isActive }) => `app-nav-link ${isActive ? 'app-nav-link-active' : ''}`}
                onClick={() => console.log('Navigating to View Index')}
              >
                View Index
              </NavLink>
            </li>
            <li className="app-nav-item">
              <NavLink
                to="/search"
                className={({ isActive }) => `app-nav-link ${isActive ? 'app-nav-link-active' : ''}`}
                onClick={() => console.log('Navigating to Search')}
              >
                Search
              </NavLink>
            </li>
          </ul>
        </nav>
        <main className="app-main">
          <Routes>
            <Route path="/" element={<Indexing />} />
            <Route path="/view-index" element={<ViewIndex />} />
            <Route path="/search" element={<Search />} />
          </Routes>
        </main>
      </div>
    </ErrorBoundary>
  );
}

export default App;