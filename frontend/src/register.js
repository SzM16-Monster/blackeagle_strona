
import React, { useState } from 'react';
import './App.css';

function Register() {
    // Stan dla pól formularza i komunikatów
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        email: '',
        username: '',
        password: '',
        confirmPassword: ''
    });
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');

    // Obsługa zmian w polach formularza
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    // Obsługa wysyłania formularza
    const handleSubmit = async (e) => {
        e.preventDefault();
        setMessage('');
        setError('');

        // Walidacja haseł
        if (formData.password !== formData.confirmPassword) {
            setError('Hasła nie są zgodne');
            return;
        }

        // Przygotowanie danych dla backendu
        const payload = {
            first_name: formData.first_name,
            last_name: formData.last_name,
            email: formData.email,
            username: formData.username,
            password: formData.password
        };

        try {
            const response = await fetch('https://backend-g7rx.onrender.com/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (response.ok) {
                setMessage(data.message || 'Rejestracja zakończona sukcesem!');
                setFormData({
                    first_name: '',
                    last_name: '',
                    email: '',
                    username: '',
                    password: '',
                    confirmPassword: ''
                });
            } else {
                setError(data.error || 'Błąd rejestracji');
            }
        } catch (err) {
            setError('Błąd połączenia z serwerem');
        }
    };

    return (
        <div className="register-page">
            <div className="center">
                <h1 className="formTitle">Rejestracja</h1>
                {message && <p className="success-message">{message}</p>}
                {error && <p className="error-message">{error}</p>}
                <form onSubmit={handleSubmit}>
                    <input
                        type="text"
                        name="first_name"
                        className="imie"
                        placeholder="Imię"
                        value={formData.first_name}
                        onChange={handleChange}
                        required
                    />
                    <input
                        type="text"
                        name="last_name"
                        className="nazwisko"
                        placeholder="Nazwisko"
                        value={formData.last_name}
                        onChange={handleChange}
                        required
                    />
                    <input
                        type="text"
                        name="username"
                        className="login"
                        placeholder="Login"
                        value={formData.username}
                        onChange={handleChange}
                        required
                    />
                    <input
                        type="email"
                        name="email"
                        className="email"
                        placeholder="Email"
                        value={formData.email}
                        onChange={handleChange}
                        required
                    />
                    <input
                        type="password"
                        name="password"
                        className="password"
                        placeholder="Hasło"
                        value={formData.password}
                        onChange={handleChange}
                        required
                    />
                    <input
                        type="password"
                        name="confirmPassword"
                        className="password"
                        placeholder="Powtórz Hasło"
                        value={formData.confirmPassword}
                        onChange={handleChange}
                        required
                    />
                    <input
                        type="submit"
                        className="submitButtonLogin"
                        value="Zarejestuj"
                    />
                </form>
            </div>
        </div>
    );
}

export default Register;
