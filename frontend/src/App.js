import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import Watched from './watched';
import Header from './header';
import Footer from './footer';
import Home from './home';
import Register from './register';
import Login from './login';
import './App.css';

function AppWrapper() {
    const location = useLocation();
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

    const hideHeaderFooter = location.pathname === '/register' || location.pathname === '/login' ;

    return (
        <>
            {!hideHeaderFooter && (
                    <Header
                        searchQuery={searchQuery}
                        setSearchQuery={setSearchQuery}
                    />
            )}
            
            <Routes>
                <Route path="/" element={<Home filteredMovies={filteredMovies} />} />
                <Route path="/watched" element={<Watched filteredMovies={filteredMovies} />} />
                <Route path="/register" element={<Register />} />
                <Route path="/login" element={<Login />} />
            </Routes>

            {!hideHeaderFooter && <Footer />}
        </>
    );
}

function App(){
    return (
        <Router>
            <AppWrapper />
        </Router>
    )
}

export default App;
