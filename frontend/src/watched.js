import React, { useEffect, useState } from 'react';
import './App.css';

const Watched = ({ filteredMovies }) => {
    const [movies, setMovies] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch('https://backend-g7rx.onrender.com/movies?userId=1')
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

    const formatPolishDate = (dateString) => {
        if (!dateString) return '';

        const date = new Date(dateString);
        const months = [
            'Stycznia', 'Lutego', 'Marca', 'Kwietnia', 'Maja', 'Czerwca',
            'Lipca', 'Sierpnia', 'Września', 'Października', 'Listopada', 'Grudnia'
        ];

        const day = date.getDate();
        const month = months[date.getMonth()];
        const year = date.getFullYear();

        return `${day} ${month} ${year}`;
    };

    if (loading) return <p>Ładowanie filmów...</p>;
    if (error) return <p>Błąd: {error}</p>;

    return (
        <div className="watched-container">
            <h1 class="header_text_watched">Obejrzane Filmy</h1>
            <div className="movie-list-watched">
                {filteredMovies.map((movie, i) => (
                    <div className="movie-item-watched" key={i}>
                        <div className="movie-poster-container">
                            <img
                                className="movie-poster-watched"
                                src={movie.poster || 'https://via.placeholder.com/150x220'}
                                alt={movie.title}
                            />
                        </div>
                        <div className="movie-details-watched">
                            <h2>{movie.title}</h2>
                            <p><strong>Data premiery:</strong> {formatPolishDate(movie.released)}</p>
                            <p><strong>Rok produkcji:</strong> {movie.prod_year}</p>
                            <p><strong>Oznaczenie wiekowe:</strong> {movie.rated}</p>
                            <p><strong>Długość trwania:</strong> {movie.runtime} min</p>
                            <p><strong>Kraj pochodzenia:</strong> {movie.country}</p>
                            <p><strong>Box Office:</strong> {movie.box_office}</p>
                            <p><strong>IMDb:</strong> {movie.imdb_rating} / 10 ({movie.imdb_votes?.toLocaleString() || 0} głosów)</p>
                            <p><strong>Metacritic:</strong> {movie.metacritic ? `${movie.metacritic}/100` : 'Brak danych'}</p>
                            <p><strong>Rotten Tomatoes:</strong> {movie.rotten_tomatoes ? `${movie.rotten_tomatoes}%` : 'Brak danych'}</p>
                            <p><strong>Nagrody:</strong> {movie.awards || 'Brak danych'}</p>
                            <p className="movie-description-watched">{movie.plot}</p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Watched;
