import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Indexing.css';

const Indexing = () => {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [fileContents, setFileContents] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const API_URL = import.meta.env.VITE_API_URL;

  const handleFileChange = async (e) => {
    const files = Array.from(e.target.files).filter(file => file.name.endsWith('.txt'));
    if (files.length !== e.target.files.length) {
      alert('Only .txt files are allowed.');
    }
    setSelectedFiles(files);

    if (files.length === 0) {
      setFileContents([]);
      return;
    }

    try {
      const contents = await Promise.all(
        files.map(file => {
          return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = reject;
            reader.readAsText(file);
          });
        })
      );
      setFileContents(contents);
    } catch (error) {
      console.error('Error reading files:', error);
      alert('Failed to read files.');
    }
  };

  const handleIndexing = async () => {
    if (!fileContents.length) {
      alert('Please select some .txt files first.');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API_URL}index/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ documents: fileContents }),
      });

      if (!response.ok) {
        throw new Error('Error during indexing');
      }

      await response.json();
      alert('Indexing completed successfully.');
      navigate('view-index');
    } catch (error) {
      console.error('Indexing failed:', error);
      alert('Indexing failed. Check console for details.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="indexing-container">
      <h1 className="indexing-title">📂 Indexing Interface</h1>
      <input
        type="file"
        multiple
        accept=".txt"
        onChange={handleFileChange}
        className="indexing-file-input"
        disabled={loading}
      />
      {selectedFiles.length > 0 && (
        <div className="indexing-files-container">
          <h3 className="indexing-files-title">Selected Files:</h3>
          <ul className="indexing-files-list">
            {selectedFiles.map((file, idx) => (
              <li key={idx} className="indexing-file-item">{file.name}</li>
            ))}
          </ul>
        </div>
      )}
      <button
        onClick={handleIndexing}
        className="indexing-button"
        disabled={loading || selectedFiles.length === 0}
      >
        {loading ? <span className="indexing-button-spinner"></span> : 'Start Indexing'}
      </button>
    </div>
  );
};

export default Indexing;