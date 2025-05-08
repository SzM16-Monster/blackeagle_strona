/* Genre */
INSERT INTO Genre (genre_id, genre_name) VALUES
(1, 'Action'),
(2, 'Drama'),
(3, 'Comedy');

/* MovieLanguage */
INSERT INTO MovieLanguage (language_id, language_name) VALUES
(1, 'English'),
(2, 'Spanish'),
(3, 'French');

/* Movie */
INSERT INTO Movie (movie_id, title, prod_year, rated, released, runtime, plot, country, imdb_rating, imdb_id) VALUES
(1, 'The Shawshank Redemption', 1994, 'R', '1994-10-14', 142, 'Two imprisoned men bond over a number of years.', 'USA', 9.3, 'tt0111161'),
(2, 'The Godfather', 1972, 'R', '1972-03-24', 175, 'The aging patriarch of an organized crime dynasty.', 'USA', 9.2, 'tt0068646');

/* Movie_Genre */
INSERT INTO Movie_Genre (movie_genre_id, movie_id, genre_id) VALUES
(1, 1, 2), -- Shawshank: Drama
(2, 2, 2); -- Godfather: Drama

/* Movie_Language */
INSERT INTO Movie_Language (movie_language_id, language_id, movie_id) VALUES
(1, 1, 1), -- Shawshank: English
(2, 1, 2); -- Godfather: English

/* People */
INSERT INTO People (people_id, people_name) VALUES
(1, 'Tim Robbins'),
(2, 'Morgan Freeman'),
(3, 'Marlon Brando');

/* Movie_People */
INSERT INTO Movie_People (movie_people_id, movie_id, people_id, role) VALUES
(1, 1, 1, 'Actor'),
(2, 1, 2, 'Actor'),
(3, 2, 3, 'Actor');

/* AppUser */
INSERT INTO AppUser (appuser_id, first_name, last_name, email, username, password, created_at) VALUES
(1, 'John', 'Doe', 'john.doe@example.com', 'johndoe', 'hashed_password_123', '2025-04-25');

/* AppUser_Movie */
INSERT INTO AppUser_Movie (user_movie_id, appuser_id, movie_id, user_rating) VALUES
(1, 1, 1, 9.5),
(2, 1, 2, 8.8);
