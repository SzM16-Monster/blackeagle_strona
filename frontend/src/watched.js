import React, { useEffect, useState } from 'react';
import './App.css';
import Header from './header';

const Watched = ({ filteredMovies }) => {
    if (!filteredMovies || filteredMovies.length === 0) {
        return <p>Brak filmów do wyświetlenia.</p>;
    }

    return (
        <div className="watched-container">
            <h1 className="header_text_watched">Obejrzane Filmy</h1>
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
                            <p><strong>Data premiery:</strong> {movie.released || 'N/A'}</p>
                            <p><strong>Opis:</strong> {movie.plot || 'Brak opisu'}</p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Watched;
