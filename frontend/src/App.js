import React, { useState, useEffect } from 'react';
import './App.css'; // Zakładam, że masz styl w App.css

function App() {
    const [movies, setMovies] = useState([]); // Wszystkie filmy z API
    const [filteredMovies, setFilteredMovies] = useState([]); // Filtrowane filmy
    const [searchQuery, setSearchQuery] = useState(''); // Zapytanie wyszukiwania

    // Pobierz filmy z backendu przy ładowaniu strony
    useEffect(() => {
        fetch('https://moj-backend.onrender.com/movies') // Zmień na Twój URL backendu
            .then((response) => response.json())
            .then((data) => {
                setMovies(data);
                setFilteredMovies(data); // Początkowo pokazuj wszystkie filmy
            })
            .catch((error) => console.error('Błąd pobierania filmów:', error));
    }, []);

    // Funkcja wyszukiwania
    const handleSearch = () => {
        const filtered = movies.filter((movie) =>
            movie.title.toLowerCase().includes(searchQuery.toLowerCase())
        );
        setFilteredMovies(filtered);
    };

    // Obsługa Enter w polu wyszukiwania
    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleSearch();
        }
    };

    return (
        <div className="app">
            <header className="header">
                <h1>Moje Filmy</h1>
                <div className="search-bar">
                    <input
                        type="text"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder="Szukaj filmu..."
                        className="search-input"
                    />
                    <button onClick={handleSearch} className="search-button">
                        Szukaj
                    </button>
                </div>
            </header>
            <div className="movie-grid">
                {filteredMovies.length > 0 ? (
                    filteredMovies.map((movie) => (
                        <div key={movie.id} className="movie-card">
                            <img
                                src={movie.poster || 'https://via.placeholder.com/200x300'}
                                alt={movie.title}
                                className="movie-poster"
                            />
                            <h3>{movie.title}</h3>
                            <p>{movie.year}</p>
                        </div>
                    ))
                ) : (
                    <p>Brak filmów do wyświetlenia</p>
                )}
            </div>
        </div>
    );
}

export default App;