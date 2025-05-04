import React, { useState } from 'react';
import './Search.css';

const Search = () => {
  const [query, setQuery] = useState('');
  const [similarityMethod, setSimilarityMethod] = useState('cosine');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query) {
      alert('Please enter a query.');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}search/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          query,
          metric: similarityMethod
        })
      });

      if (!response.ok) {
        throw new Error('Search failed');
      }

      const data = await response.json();
      setResults(data.results || []);
      if (data.results.length === 0) {
        alert('No matching documents found.');
      }
    } catch (error) {
      console.error('Search error:', error);
      alert('Search failed. Check console for details.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="search-container">
      <h1 className="search-title">Recherche</h1>
      <div className="search-input-container">
        <textarea
          placeholder="Saisissez votre requête..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          rows={4}
          className="search-textarea"
          disabled={loading}
        />
      </div>
      <div className="search-metric-container">
        <label className="search-label">Choisir une méthode de similarité: </label>
        <select
          value={similarityMethod}
          onChange={(e) => setSimilarityMethod(e.target.value)}
          className="search-select"
          disabled={loading}
        >
          <option value="cosine">Similarité Cosinus</option>
          <option value="euclidean">Distance Euclidienne</option>
        </select>
      </div>
      <button
        onClick={handleSearch}
        className="search-button"
        disabled={loading}
      >
        {loading ? 'Searching...' : 'Rechercher'}
      </button>
      <div className="search-results-container">
        <h2 className="search-results-title">Résultats :</h2>
        {loading ? (
          <p className="search-loading">Loading...</p>
        ) : (
          <ul className="search-results-list">
            {results.length === 0 && <p className="search-no-results">Aucun résultat</p>}
            {results.map((result, index) => (
              <li key={index} className="search-result-item">
                <strong>Doc {result.doc_id} (Score: {result.score.toFixed(4)}):</strong> {result.content}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default Search;