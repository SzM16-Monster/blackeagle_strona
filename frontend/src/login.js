import React from 'react';
import './App.css';
import { Link } from 'react-router-dom';

//login haslo

function Login() {
    return (
            <div className="login-page">
                    <div className="center">
                        <h1 className="formTitle">Logowanie</h1>
                        <input
                            type="text"
                            className="login"
                            placeholder="Login"
                        />
                        <input
                            type="password"
                            className="password"
                            placeholder="Hasło"
                        />
                        <input
                            type="button"
                            className="submitButtonLogin"
                            value="Zaloguj"
                        />
                        <p className="linkreg">
                            Załóż konto: <Link to="/register">Rejestracja</Link>
                        </p>
                    </div>
            </div>
    );
}

export default Login;
