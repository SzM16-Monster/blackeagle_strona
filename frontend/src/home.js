function Home({ filteredMovies }) {
    return (
        <div className="movie-grid">
            {filteredMovies.length > 0 ? (
                filteredMovies.map((movie, i) => (
                    <div key={movie.id} className="movie-card">                        
                            <img
                                src={movie.poster || 'https://via.placeholder.com/200x300'}
                                alt={movie.title}
                                className="movie-poster"
                            />
                        <h3 className="movieTitle">{movie.title}</h3>
                        <p>{movie.year}</p>
                    </div>
                ))
            ) : (
                <p>Brak filmów do wyświetlenia</p>
            )}
        </div>
    );
}

export default Home;
