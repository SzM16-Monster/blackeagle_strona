
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './App.css';

function Login() {
    const [formData, setFormData] = useState({
        email: '',
        password: ''
    });
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setMessage('');
        setError('');

        const payload = {
            email: formData.email,
            password: formData.password
        };

        try {
            const response = await fetch('https://backend-g7rx.onrender.com/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem('token', data.token);
                setMessage('Logowanie zakończone sukcesem!');
                setTimeout(() => {
                    navigate('/home');
                }, 1000);
            } else {
                setError(data.error || 'Błąd logowania');
            }
        } catch (err) {
            setError('Błąd połączenia z serwerem');
        }
    };

    return (
        <div className="login-page">
            <div className="center">
                <h1 className="formTitle">Logowanie</h1>
                {message && <p className="success-message">{message}</p>}
                {error && <p className="error-message">{error}</p>}
                <form onSubmit={handleSubmit}>
                    <input
                        type="email"
                        name="email"
                        className="login"
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
                        type="submit"
                        className="submitButtonLogin"
                        value="Zaloguj"
                    />
                </form>
                <p className="linkreg">
                    Załóż konto: <Link to="/register">Rejestracja</Link>
                </p>
            </div>
        </div>
    );
}

export default Login;
