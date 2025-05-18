import React from 'react';
import { useNavigate } from 'react-router-dom';

function Logout() {
    const navigate = useNavigate();

    const handleLogout = () => {
        // Usuñ token z localStorage
        localStorage.removeItem('token');

        // Opcjonalnie: Wyczyœæ inne dane w localStorage, jeœli s¹
         localStorage.clear(); // U¿yj ostro¿nie, jeœli przechowujesz inne dane

        // Przekieruj na stronê logowania
        navigate('/login');

        // Opcjonalnie: Wyœwietl komunikat o wylogowaniu
        // Mo¿esz u¿yæ stanu lub toastów (np. react-toastify)
        console.log('User logged out successfully');
    };

    return (
        <button onClick={handleLogout} className="logout-button">
            Wyloguj
        </button>
    );
}

export default Logout;