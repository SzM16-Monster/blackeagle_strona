import React, { useState, useEffect } from 'react';
import './Movie.css';

function Recommendations() {
    const [recommendations, setRecommendations] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchRecommendations = async () => {
            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    throw new Error('No token found. Please log in.');
                }
                if (process.env.NODE_ENV === 'development') {
                    console.debug('Token exists:', !!token);
                    console.debug('Token (first 10 chars):', token.substring(0, 10));
                }

                const response = await fetch('http://127.0.0.1:5000/recommendations', {
                    method: 'GET',
                    headers: {
                        Authorization: `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(`HTTP error! status: ${response.status}, message: ${JSON.stringify(errorData)}`);
                }

                const data = await response.json();
                setRecommendations(data.recommendation || []);
            } catch (error) {
                console.error('Error fetching recommendations:', error);
                setError(error.message);
            }
        };

        const token = localStorage.getItem('token');
        if (token) {
            fetchRecommendations();
        } else {
            setError('Please log in to see recommendations.');
        }
    }, []);

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div className="movie-container">
            <h2>Recommended Movies</h2>
            {recommendations.length === 0 ? (
                <p>No recommendations available</p>
            ) : (
                recommendations.map((movie) => (
                    <div key={movie.movie_id} className="movie-item-watched">
                        <img
                            src={movie.poster || 'https://via.placeholder.com/150x225'}
                            alt={movie.title || 'No title'}
                        />
                        <h3>{movie.title || 'No title'}</h3>
                        <p>Year: {movie.prod_year || 'N/A'}</p>
                        <p>IMDb Rating: {movie.imdb_rating || 'N/A'}</p>
                        <p>Type: {movie.movie_type || 'N/A'}</p>
                    </div>
                ))
            )}
        </div>
    );
}

export default Recommendations;