import React, { useState, useEffect } from 'react';
import './Movie.css';

function Movie() {
    const [movies, setMovies] = useState([]);
    const [error, setError] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        const fetchMovies = async () => {
            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    throw new Error('No token found');
                }
                const response = await fetch('http://127.0.0.1:5000/user/movies', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                });
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                setMovies(data.movies || []);
            } catch (error) {
                console.error('Error fetching movies:', error);
                setError(error.message);
            }
        };
        fetchMovies();
    }, []);

    const filteredMovies = movies.filter(movie =>
        movie.title && typeof movie.title === 'string'
            ? movie.title.toLowerCase().includes(searchTerm.toLowerCase())
            : false
    );

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div className="movie-container">
            <input
                type="text"
                placeholder="Search movies..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
            />
            {filteredMovies.length === 0 ? (
                <p>No movies found</p>
            ) : (
                filteredMovies.map((movie) => (
                    <div key={movie.movie_id} className="movie-item-watched">
                        <img
                            src={movie.poster || 'https://via.placeholder.com/150x225'}
                            alt={movie.title || 'No title'}
                        />
                        <h3>{movie.title || 'No title'}</h3>
                        <p>Year: {movie.prod_year || 'N/A'}</p>
                        <p>Rating: {movie.user_rating || 'Not rated'}</p>
                        <p>Watched: {movie.watched_date ? new Date(movie.watched_date).toLocaleDateString() : 'N/A'}</p>
                    </div>
                ))
            )}
        </div>
    );
}

export default Movie;



