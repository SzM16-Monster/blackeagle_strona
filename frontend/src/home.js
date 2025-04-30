import React from 'react';
import Slider from 'react-slick';

function Home({ filteredMovies }) {
    const settings = {
        infinite: true,
        autoplay: true,
        autoplaySpeed: 6000,
        fade: true,
        dots: true,
        arrows: false,
        slidesToShow: 1,
        slidesToScroll: 1,
        customPaging: i => (
            <button
                type="button"
                aria-label={`Przejdź do slajdu ${i + 1}`}
                className="dot-btn"
            />
        ),
        appendDots: dots => (
            <ul className="dots-container">{dots}</ul>
        )
    };

    return (
        <div className="movie-slider">
            {filteredMovies.length > 0 ? (
                <>
                    <Slider {...settings}>
                        {filteredMovies.map(movie => (
                            <div key={movie.movie_id}>
                                <div
                                    className="hero"
                                    style={{ backgroundImage: `url(${movie.backdrop || movie.poster})` }}
                                >
                                    <div className="gradient" />
                                    <div className="hero-content">
                                        <img src="/searchlight.svg" className="studio" alt="" />
                                        <h2 className="title">{movie.title}</h2>
                                        <p className="meta">
                                            {movie.prod_year && <>{movie.prod_year}</>}
                                            {movie.rated && <>&nbsp;• {movie.rated}</>}
                                            {movie.genre && movie.genre.length > 0 && <>&nbsp;• {movie.genre.join(', ')}</>}
                                            {movie.runtime && <>&nbsp;• {movie.runtime} min</>}
                                            {movie.country && <>&nbsp;• {movie.country}</>}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </Slider>
                    <div className="movie-grid">
                        {filteredMovies.map(movie => (
                            <div key={movie.movie_id} className="movie-card">
                                <img
                                    src={movie.poster || 'https://placehold.co/200x300'}
                                    alt={movie.title}
                                    className="movie-poster"
                                />
                                <h3 className="movieTitle">{movie.title}</h3>
                                <p>{movie.prod_year}</p>
                            </div>
                        ))}
                    </div>
                </>
            ) : (
                <p>Brak filmów do wyświetlenia</p>
            )}
        </div>
    );
}

export default Home;
