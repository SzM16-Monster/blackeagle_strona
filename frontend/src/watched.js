import React, { useEffect, useState } from 'react';
import './App.css';
import Header from './header';

const Watched = ({ filteredMovies }) => {
    const [movies, setMovies] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch('https://black-eagle-backend.onrender.com/movies?user_id=1')
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Błąd przy pobieraniu danych');
                }
                return response.json();
            })
            .then((data) => {
                setMovies(data);
                setLoading(false);
            })
            .catch((err) => {
                setError(err.message);
                setLoading(false);
            });
    }, []);

    if (loading) return <p>Ładowanie filmów...</p>;
    if (error) return <p>Błąd: {error}</p>;

    return (
        <div className="watched-container">
            <h1 class="header_text_watched">Obejrzane Filmy</h1>
            <div className="movie-list">
                {filteredMovies.map((movie, i) => (
                    <div className="movie-item" key={i}>
                        <img
                            className="movie-poster-watched"
                            src={movie.poster || 'https://via.placeholder.com/150x220'}
                            alt={movie.title}
                        />
                        <div className="movie-details">
                            <h2>{movie.title}</h2>
                            <p><strong>Data premiery:</strong> {movie.release_date}</p>
                            <p><strong>Gatunki:</strong> {movie.genres}</p>
                            <p className="movie-description">{movie.description}</p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Watched;
