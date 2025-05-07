import React from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';
import { EffectCoverflow, Navigation, Autoplay } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/effect-coverflow';
import 'swiper/css/navigation';
import './App.css'; 

function Home({ filteredMovies }) {

    return (
        <div className="movie-slider">
            {filteredMovies.length > 0 ? (
                <>
                    <Swiper
                        loop={true}
                        autoHeight = {true}
                        slidesPerView = {3}
                        spaceBetween = {10}
                        breakpoints={{
                            320: { slidesPerView: 2, spaceBetween: 20 },
                            480: { slidesPerView: 3, spaceBetween: 30 },
                            640: { slidesPerView: 4, spaceBetween: 40 }}}
                        centeredSlides={true}
                        effect = "coverflow"
                        coverflowEffect={{
                            rotate: 0,
                            slideShadows: false,
                            depth: 300,
                            stretch: 0,
                            }}
                        autoplay={{
                            delay: 3000,
                            disableOnInteraction: false,
                        }}
                        modules={[EffectCoverflow, Navigation, Autoplay]}
                        className="coverflowSwiper"
                    >
                        {filteredMovies.map((movie) => (
                            <SwiperSlide key={`slide-${movie.movie_id}`}>
                                <div className="carousel-item">
                                    <img
                                        src={movie.poster || 'https://placehold.co/200x300'}
                                        alt={movie.title}
                                        className="carousel-poster"
                                    />
                                    <h3 className="carousel-title">{movie.title}</h3>
                                    <p className="carousel-meta">{movie.prod_year}</p>
                                </div>
                            </SwiperSlide>
                        ))}
                    </Swiper>

                    <div className="categories-slider">
                        <div className="category-section">
                            <h2 className="category-title">Filmy</h2>
                            <Swiper
                                loop={true}
                                spaceBetween={15}
                                slidesPerView={8}
                                navigationmodules={[Navigation]}
                            >
                                {filteredMovies.map((movie) => (
                                    <SwiperSlide key={movie.movie_id}>
                                        <div className="movie-card">
                                            <img
                                                src={movie.poster || 'https://placehold.co/200x300'}
                                                alt={movie.title}
                                                className="movie-poster"
                                            />
                                            {/* <h3 className="movieTitle">{movie.title}</h3>
                                            <p>{movie.prod_year}</p> */}
                                        </div>
                                    </SwiperSlide>
                                ))}
                            </Swiper>
                        </div>
                    </div>
                    <div className="categories-slider">
                        <div className="category-section">
                            <h2 className="category-title">Filmy</h2>
                            <Swiper
                                loop={true}
                                spaceBetween={15}
                                slidesPerView={8}
                                navigationmodules={[Navigation]}
                            >
                                {filteredMovies.map((movie) => (
                                    <SwiperSlide key={movie.movie_id}>
                                        <div className="movie-card">
                                            <img
                                                src={movie.poster || 'https://placehold.co/200x300'}
                                                alt={movie.title}
                                                className="movie-poster"
                                            />
                                            {/* <h3 className="movieTitle">{movie.title}</h3>
                                            <p>{movie.prod_year}</p> */}
                                        </div>
                                    </SwiperSlide>
                                ))}
                            </Swiper>
                        </div>
                    </div>
                    <div className="categories-slider">
                        <div className="category-section">
                            <h2 className="category-title">Filmy</h2>
                            <Swiper
                                loop={true}
                                spaceBetween={15}
                                slidesPerView={8}
                                navigationmodules={[Navigation]}
                            >
                                {filteredMovies.map((movie) => (
                                    <SwiperSlide key={movie.movie_id}>
                                        <div className="movie-card">
                                            <img
                                                src={movie.poster || 'https://placehold.co/200x300'}
                                                alt={movie.title}
                                                className="movie-poster"
                                            />
                                            {/* <h3 className="movieTitle">{movie.title}</h3>
                                            <p>{movie.prod_year}</p> */}
                                        </div>
                                    </SwiperSlide>
                                ))}
                            </Swiper>
                        </div>
                    </div>
                    <div className="categories-slider">
                        <div className="category-section">
                            <h2 className="category-title">Filmy</h2>
                            <Swiper
                                loop={true}
                                spaceBetween={15}
                                slidesPerView={8}
                                navigationmodules={[Navigation]}
                            >
                                {filteredMovies.map((movie) => (
                                    <SwiperSlide key={movie.movie_id}>
                                        <div className="movie-card">
                                            <img
                                                src={movie.poster || 'https://placehold.co/200x300'}
                                                alt={movie.title}
                                                className="movie-poster"
                                            />
                                            {/* <h3 className="movieTitle">{movie.title}</h3>
                                            <p>{movie.prod_year}</p> */}
                                        </div>
                                    </SwiperSlide>
                                ))}
                            </Swiper>
                        </div>
                    </div>
                    <div className="categories-slider">
                            <div className="category-section">
                                <h2 className="category-title">Seriale</h2>
                                <Swiper
                                    loop={true}
                                    spaceBetween={15}
                                    slidesPerView={8}
                                    navigationmodules={[Navigation]}
                                >
                                    {filteredMovies.map((movie) => (
                                        <SwiperSlide key={movie.movie_id}>
                                            <div className="movie-card">
                                                <img
                                                    src={movie.poster || 'https://placehold.co/200x300'}
                                                    alt={movie.title}
                                                    className="movie-poster"
                                                />
                                                {/* <h3 className="movieTitle">{movie.title}</h3>
                                                <p>{movie.prod_year}</p> */}
                                            </div>
                                        </SwiperSlide>
                                    ))}
                                </Swiper>
                            </div>
                    </div>
                </>
            ) : (
                <p>Brak filmów do wyświetlenia</p>
            )}
        </div>
    );
}

export default Home;
