import React, { useState } from "react";

function App() {
    // Miejsce, gdzie trzymamy filmy i błąd
    const [movies, setMovies] = useState([]);
    const [errorMessage, setErrorMessage] = useState("");

    // Funkcja do pobierania filmów
    function getMovies() {
        // Wysyłamy prośbę do serwera
        fetch("https://backend-g7rx.onrender.com/movies")
            .then((response) => {
                // Jeśli coś poszło nie tak, pokazujemy błąd
                if (!response.ok) {
                    setErrorMessage("Nie udało się pobrać filmów!");
                    return;
                }
                // Zamieniamy odpowiedź na dane (filmy)
                response.json().then((data) => {
                    setMovies(data); // Zapisujemy filmy
                });
            })
            .catch(() => {
                // Jeśli serwer nie działa, pokazujemy błąd
                setErrorMessage("Błąd połączenia z serwerem!");
            });
    }

    // Uruchamiamy pobieranie filmów zaraz po załadowaniu strony
    if (movies.length === 0 && errorMessage === "") {
        getMovies();
    }

    // Co wyświetlamy na stronie
    return (
        <div style={{ padding: "20px" }}>
            <h1>Moje filmy</h1>

            {/* Pokazujemy błąd, jeśli jest */}
            {errorMessage !== "" && <p style={{ color: "red" }}>{errorMessage}</p>}

            {/* Pokazujemy "Ładowanie", jeśli nie ma filmów ani błędu */}
            {movies.length === 0 && errorMessage === "" && <p>Ładowanie...</p>}

            {/* Pokazujemy tabelę, jeśli są filmy */}
            {movies.length > 0 && (
                <table border="1" style={{ marginTop: "20px" }}>
                    <thead>
                        <tr>
                            <th>Plakat</th>
                            <th>Tytuł</th>
                            <th>Opis</th>
                            <th>Gatunki</th>
                            <th>Data premiery</th>
                        </tr>
                    </thead>
                    <tbody>
                        {movies.map((movie, index) => (
                            <tr key={index}>
                                <td>
                                    {movie.poster ? (
                                        <img src={movie.poster} alt={movie.title} width="100" />
                                    ) : (
                                        "Brak plakatu"
                                    )}
                                </td>
                                <td>{movie.title || "Brak tytułu"}</td>
                                <td>{movie.description || "Brak opisu"}</td>
                                <td>{movie.genres || "Brak gatunków"}</td>
                                <td>{movie.release_date || "Brak daty"}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}

export default App;