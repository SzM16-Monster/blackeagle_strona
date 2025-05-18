import React from 'react';
import { useNavigate } from 'react-router-dom';

function Logout() {
    const navigate = useNavigate();

    const handleLogout = () => {
        // Usu� token z localStorage
        localStorage.removeItem('token');

        // Opcjonalnie: Wyczy�� inne dane w localStorage, je�li s�
         localStorage.clear(); // U�yj ostro�nie, je�li przechowujesz inne dane

        // Przekieruj na stron� logowania
        navigate('/login');

        // Opcjonalnie: Wy�wietl komunikat o wylogowaniu
        // Mo�esz u�y� stanu lub toast�w (np. react-toastify)
        console.log('User logged out successfully');
    };

    return (
        <button onClick={handleLogout} className="logout-button">
            Wyloguj
        </button>
    );
}

export default Logout;