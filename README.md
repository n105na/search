# TF-IDF Search Engine

A web application for indexing and searching text documents using the TF-IDF algorithm. Built with a **React** frontend and **FastAPI** backend, it allows users to upload `.txt` files, index them, view the TF/IDF and TF-IDF matrices, and search using cosine or Euclidean similarity metrics.

## Features

- **Indexing Interface**: Upload multiple `.txt` files, validate file types, and index documents using TF-IDF.
- **View Index Interface**: Display two tables showing TF/IDF frequencies and TF-IDF scores for indexed documents.
- **Search Interface**: Enter queries, select cosine or Euclidean similarity, and view ranked results with scores.
- **Navigation Bar**: Switch between Indexing, View Index, and Search pages.
- **Backend Processing**: Normalizes text, removes stopwords, and applies stemming using NLTK.
- **IDF Calculation**: Uses `log2` for inverse document frequency.
- **Responsive Design**: Styled with CSS for desktop and mobile compatibility.
- **User Feedback**: Alerts for success and error messages (e.g., invalid file types, empty queries).

## Tech Stack

- **Frontend**: React, React Router, Vite
- **Backend**: FastAPI, Python, NLTK
- **Styling**: Custom CSS
- **API**: RESTful endpoints for indexing (`/index/`), viewing (`/view-index/`), and searching (`/search/`)

## Prerequisites

- **Node.js** (v16 or higher) for the frontend
- **Python** (v3.8 or higher) for the backend
- **Git** for version control
- **GitHub account** for repository hosting

## Setup Instructions

### Backend

1. Clone the repository (after pushing to GitHub, see below):
   ```bash
   git clone https://github.com/n105na/search.git
   cd your-repo-name
   ```
2. Navigate to the backend directory (`backend/`):
   ```bash
   cd backend
   ```
3. Install Python dependencies:
   ```bash
   pip install fastapi uvicorn nltk
   ```
4. Download NLTK data:
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```
5. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
   The backend runs on `http://localhost:8000`.

### Frontend

1. Navigate to the frontend directory (`frontend/`):
   ```bash
   cd frontend
   ```
2. Install Node.js dependencies:
   ```bash
   npm install
   ```
3. Create a `.env` file in the frontend directory with:
   ```env
   VITE_API_URL=http://localhost:8000
   ```
4. Run the React app:
   ```bash
   npm run dev
   ```
   The frontend runs on `http://localhost:5173`.

## Usage

### Indexing
- Go to the Indexing page (`/`).
- Upload `.txt` files (e.g., "The quick brown fox...").
- Click "Start Indexing" to process files and navigate to View Index.

### View Index
- On the View Index page (`/view-index`), view TF/IDF and TF-IDF tables.
- Click "Go to Search" or use the nav bar to search.

### Search
- On the Search page (`/search`), enter a query (e.g., "quick dog").
- Select cosine or Euclidean similarity.
- Click "Rechercher" to view ranked results with scores.

### Navigation
- Use the top navigation bar to switch between Indexing, View Index, and Search.

## Project Structure

```
search/
├── backend/                 # FastAPI backend
│   ├── main.py              # API endpoints
│   ├── search_engine.py     # TF-IDF logic
│   └── requirements.txt     # Python dependencies
├── frontend/                # React frontend
│   ├── src/
│   │   ├── pages/           # React components
│   │   │   ├── Indexing.jsx
│   │   │   ├── ViewIndex.jsx
│   │   │   ├── Search.jsx
│   │   │   ├── Indexing.css
│   │   │   ├── ViewIndex.css
│   │   │   ├── Search.css
│   │   ├── App.jsx          # Routes and nav bar
│   │   ├── App.css          # Nav bar styling
│   │   ├── main.jsx         # Entry point with BrowserRouter
│   │   └── index.css        # Global styles
│   ├── .env                 # VITE_API_URL
│   ├── package.json         # Node.js dependencies
│   └── vite.config.js       # Vite configuration
├── README.md                # This file
└── .gitignore               # Git ignore rules
```

## Notes

- **IDF Calculation**: Uses `log2` for IDF, as specified in `search_engine.py`.
- **Error Handling**: Alerts for invalid file types, empty queries, or API errors.
- **Responsive Design**: Optimized for desktop and mobile with CSS media queries.
- **Security**: Run `npm audit fix` to resolve frontend vulnerabilities before deployment.

## Contributing

This is a student project for educational purposes. Feel free to fork and experiment, but no contributions are expected.

## License

This project is for academic use and not licensed for commercial purposes.

## Acknowledgments

- Built as part of a coursework assignment to implement a TF-IDF search engine.
- Uses NLTK for text processing and FastAPI for efficient API handling.