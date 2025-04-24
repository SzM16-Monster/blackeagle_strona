import React from 'react';
import { Link } from 'react-router-dom';
import { Settings, CircleUserRound, Funnel } from 'lucide-react';
import './App.css';

const Header = ({ searchQuery, setSearchQuery }) => {
    return (
        <header className="header-container">
            <div className="header-left">
                <div className="logo">
                    <a href="/">
                        <img src="blackeaglelogo.png" alt="logo" />
                    </a>
                </div>
                <nav className="nav-links">
                    <Link to="/filmy">Filmy</Link>
                    <Link to="/seriale">Seriale</Link>
                    <Link to="/watched">Obejrzane</Link>
                </nav>
            </div>

            <div className="header-right">
                <input
                    type="text"
                    className="search-header"
                    placeholder="Szukaj"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                />
                <Funnel className="icon-funnel" />
                <Settings className="icon-settings" />
                <CircleUserRound className="icon-CircleUserRound" />
            </div>
        </header>
    );
};

export default Header;
