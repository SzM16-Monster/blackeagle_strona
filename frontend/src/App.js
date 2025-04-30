import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import Watched from './watched';
import Header from './header';
import Home from './home';
import './App.css';

function App() {
    const [movies, setMovies] = useState([]);
    const [searchQuery, setSearchQuery] = useState('');

    useEffect(() => {
        fetch('https://backend-g7rx.onrender.com/movies?user_id=1')
            .then((res) => res.json())
            .then((data) => setMovies(data));
    }, []);

    const filteredMovies = movies.filter((movie) =>
        movie.title.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return (
        <Router>
            <Header
                searchQuery={searchQuery}
                setSearchQuery={setSearchQuery}
            />
            <Routes>
                <Route path="/" element={<Home filteredMovies={filteredMovies} />} />
                <Route path="/watched" element={<Watched filteredMovies={filteredMovies} />} />
            </Routes>
        </Router>
    );
}

export default App;
