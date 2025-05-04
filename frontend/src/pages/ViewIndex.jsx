import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './ViewIndex.css';

function ViewIndex() {
  const [indexData, setIndexData] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchIndex = async () => {
      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/view-index/`);
        const data = await response.json();
        if (response.ok) {
          setIndexData(data);
        } else {
          throw new Error('Error fetching index');
        }
      } catch (err) {
        console.error(err);
        alert('Error fetching index.');
      }
    };
    fetchIndex();
  }, []);

  return (
    <div className="view-index-container">
      <h1 className="view-index-title">View Index</h1>
      {indexData ? (
        <div>
          {/* TF and IDF Table */}
          <h2 className="view-index-subtitle">Term Frequency (TF) and IDF</h2>
          <table className="view-index-table">
            <thead>
              <tr className="view-index-table-header">
                <th>Term</th>
                {indexData.documents.map((_, docId) => (
                  <th key={docId}>Doc {docId}</th>
                ))}
                <th>IDF</th>
              </tr>
            </thead>
            <tbody>
              {Object.keys(indexData.tfidf).map(term => (
                <tr key={term} className="view-index-table-row">
                  <td>{term}</td>
                  {indexData.documents.map((_, docId) => (
                    <td key={docId}>
                      {(indexData.tf[docId][term] || 0).toFixed(4)}
                    </td>
                  ))}
                  <td>{indexData.idf[term].toFixed(4)}</td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* TF-IDF Table */}
          <h2 className="view-index-subtitle">TF-IDF Values</h2>
          <table className="view-index-table">
            <thead>
              <tr className="view-index-table-header">
                <th>Term</th>
                {indexData.documents.map((_, docId) => (
                  <th key={docId}>Doc {docId}</th>
                ))}
                
              </tr>
            </thead>
            <tbody>
              {Object.keys(indexData.tfidf).map(term => (
                <tr key={term} className="view-index-table-row">
                  <td>{term}</td>
                  {indexData.documents.map((_, docId) => (
                    <td key={docId}>
                      {indexData.tfidf[term][docId].toFixed(4)}
                    </td>
                  ))}
                  
                </tr>
              ))}
            </tbody>
          </table>

          <button
            onClick={() => navigate('/search', { state: { indexData } })}
            className="view-index-button"
          >
            Go to Search
          </button>
        </div>
      ) : (
        <p className="view-index-loading">Loading...</p>
      )}
    </div>
  );
}

export default ViewIndex;