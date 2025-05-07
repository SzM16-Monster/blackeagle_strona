import React from 'react';
import './App.css';
// imie nazwisko mail username password

function Register() {
    return (
        <div className="register-page">
                <div className="center">
                    <h1 className="formTitle">Rejestracja</h1>
                    <input
                        type="text"
                        className="imie"
                        placeholder="Imię"
                    />
                    <input
                        type="text"
                        className="nazwisko"
                        placeholder="Nazwisko"
                    />
                    <input
                        type="text"
                        className="login"
                        placeholder="Login"
                    />
                    <input
                        type="text"
                        className="email"
                        placeholder="Email"
                    />
                    <input
                        type="password"
                        className="password"
                        placeholder="Hasło"

                    />
                    <input
                        type="password"
                        className="password"
                        placeholder="Powtórz Hasło"
                    />
                    <input
                        type="button"
                        className="submitButtonLogin"
                        value="Zarejestuj"
                    />
                </div>
        </div>
    );
}

export default Register;
