/*==============================================================*/
/* DBMS name:      PostgreSQL 9.x                               */
/* Created on:     25.04.2025                                   */
/* Description:    Improved movie database schema with safe names */
/*==============================================================*/

/* Drop existing objects if they exist */
DROP TABLE IF EXISTS AppUser_Movie;
DROP TABLE IF EXISTS Movie_People;
DROP TABLE IF EXISTS Movie_Language;
DROP TABLE IF EXISTS Movie_Genre;
DROP TABLE IF EXISTS AppUser;
DROP TABLE IF EXISTS People;
DROP TABLE IF EXISTS Movie;
DROP TABLE IF EXISTS MovieLanguage;
DROP TABLE IF EXISTS Genre;

/*==============================================================*/
/* Table: Genre                                                 */
/*==============================================================*/
CREATE TABLE Genre (
   genre_id INT4 NOT NULL,
   genre_name VARCHAR(50) NOT NULL,
   CONSTRAINT PK_GENRE PRIMARY KEY (genre_id)
);

/*==============================================================*/
/* Table: MovieLanguage                                         */
/*==============================================================*/
CREATE TABLE MovieLanguage (
   language_id INT4 NOT NULL,
   language_name VARCHAR(50) NOT NULL,
   CONSTRAINT PK_LANG PRIMARY KEY (language_id)
);

/*==============================================================*/
/* Table: Movie                                                 */
/*==============================================================*/
CREATE TABLE Movie (
   movie_id INT4 NOT NULL,
   title VARCHAR(255) NOT NULL,
   prod_year INT4 NULL,
   rated VARCHAR(10) NULL,
   released DATE NULL,
   runtime INT4 NULL,
   plot TEXT NULL,
   country VARCHAR(100) NULL,
   awards TEXT NULL,
   poster VARCHAR(255) NULL,
   tmdb_rating FLOAT8 NULL,
   rotten_tomatoes FLOAT8 NULL,
   metacritic FLOAT8 NULL,
   imdb_rating FLOAT8 NULL,
   imdb_votes INT4 NULL,
   imdb_id VARCHAR(20) NULL,
   movie_type VARCHAR(50) NULL,
   box_office VARCHAR(50) NULL,
   CONSTRAINT PK_MOVIE PRIMARY KEY (movie_id)
);

/*==============================================================*/
/* Index: idx_movie_title                                       */
/*==============================================================*/
CREATE INDEX idx_movie_title ON Movie (title);

/*==============================================================*/
/* Table: Movie_Genre                                           */
/*==============================================================*/
CREATE TABLE Movie_Genre (
   movie_genre_id INT4 NOT NULL,
   movie_id INT4 NOT NULL,
   genre_id INT4 NOT NULL,
   CONSTRAINT PK_MOVIE_GENRE PRIMARY KEY (movie_genre_id),
   CONSTRAINT FK_MOVIE_GENRE_MOVIE FOREIGN KEY (movie_id)
      REFERENCES Movie (movie_id)
      ON DELETE CASCADE ON UPDATE RESTRICT,
   CONSTRAINT FK_MOVIE_GENRE_GENRE FOREIGN KEY (genre_id)
      REFERENCES Genre (genre_id)
      ON DELETE RESTRICT ON UPDATE RESTRICT
);

/*==============================================================*/
/* Index: idx_movie_genre_movie                                 */
/*==============================================================*/
CREATE INDEX idx_movie_genre_movie ON Movie_Genre (movie_id);

/*==============================================================*/
/* Index: idx_movie_genre_genre                                 */
/*==============================================================*/
CREATE INDEX idx_movie_genre_genre ON Movie_Genre (genre_id);

/*==============================================================*/
/* Table: Movie_Language                                        */
/*==============================================================*/
CREATE TABLE Movie_Language (
   movie_language_id INT4 NOT NULL,
   language_id INT4 NOT NULL,
   movie_id INT4 NOT NULL,
   CONSTRAINT PK_MOVIE_LANG PRIMARY KEY (movie_language_id),
   CONSTRAINT FK_MOVIE_LANG_LANGUAGE FOREIGN KEY (language_id)
      REFERENCES MovieLanguage (language_id)
      ON DELETE RESTRICT ON UPDATE RESTRICT,
   CONSTRAINT FK_MOVIE_LANG_MOVIE FOREIGN KEY (movie_id)
      REFERENCES Movie (movie_id)
      ON DELETE CASCADE ON UPDATE RESTRICT
);

/*==============================================================*/
/* Index: idx_movie_language_language                           */
/*==============================================================*/
CREATE INDEX idx_movie_language_language ON Movie_Language (language_id);

/*==============================================================*/
/* Index: idx_movie_language_movie                              */
/*==============================================================*/
CREATE INDEX idx_movie_language_movie ON Movie_Language (movie_id);

/*==============================================================*/
/* Table: People                                                */
/*==============================================================*/
CREATE TABLE People (
   people_id INT4 NOT NULL,
   people_name VARCHAR(255) NOT NULL,
   CONSTRAINT PK_PEOPLE PRIMARY KEY (people_id)
);

/*==============================================================*/
/* Table: Movie_People                                          */
/*==============================================================*/
CREATE TABLE Movie_People (
   movie_people_id INT4 NOT NULL,
   movie_id INT4 NOT NULL,
   people_id INT4 NOT NULL,
   role VARCHAR(50) NOT NULL,
   CONSTRAINT PK_MOVIE_PEOPLE PRIMARY KEY (movie_people_id),
   CONSTRAINT FK_MOVIE_PEOPLE_MOVIE FOREIGN KEY (movie_id)
      REFERENCES Movie (movie_id)
      ON DELETE CASCADE ON UPDATE RESTRICT,
   CONSTRAINT FK_MOVIE_PEOPLE_PEOPLE FOREIGN KEY (people_id)
      REFERENCES People (people_id)
      ON DELETE RESTRICT ON UPDATE RESTRICT
);

/*==============================================================*/
/* Index: idx_movie_people_movie                                */
/*==============================================================*/
CREATE INDEX idx_movie_people_movie ON Movie_People (movie_id);

/*==============================================================*/
/* Index: idx_movie_people_people                               */
/*==============================================================*/
CREATE INDEX idx_movie_people_people ON Movie_People (people_id);

/*==============================================================*/
/* Table: AppUser                                               */
/*==============================================================*/
CREATE TABLE AppUser (
   appuser_id INT4 NOT NULL,
   first_name VARCHAR(255) NULL,
   last_name VARCHAR(255) NULL,
   email VARCHAR(255) NOT NULL UNIQUE CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
   username VARCHAR(255) NOT NULL UNIQUE,
   password VARCHAR(255) NOT NULL, -- Hashed passwords
   created_at DATE NULL,
   CONSTRAINT PK_APPUSER PRIMARY KEY (appuser_id)
);

/*==============================================================*/
/* Index: idx_appuser_email                                     */
/*==============================================================*/
CREATE INDEX idx_appuser_email ON AppUser (email);

/*==============================================================*/
/* Table: AppUser_Movie                                         */
/*==============================================================*/
CREATE TABLE AppUser_Movie (
   user_movie_id INT4 NOT NULL,
   appuser_id INT4 NOT NULL,
   movie_id INT4 NOT NULL,
   user_rating FLOAT NULL,
   watched_date DATE NULL,
   CONSTRAINT PK_APPUSER_MOVIE PRIMARY KEY (user_movie_id),
   CONSTRAINT FK_APPUSER_MOVIE_APPUSER FOREIGN KEY (appuser_id)
      REFERENCES AppUser (appuser_id)
      ON DELETE CASCADE ON UPDATE RESTRICT,
   CONSTRAINT FK_APPUSER_MOVIE_MOVIE FOREIGN KEY (movie_id)
      REFERENCES Movie (movie_id)
      ON DELETE CASCADE ON UPDATE RESTRICT
);

/*==============================================================*/
/* Index: idx_appuser_movie_user                                */
/*==============================================================*/
CREATE INDEX idx_appuser_movie_user ON AppUser_Movie (appuser_id);

/*==============================================================*/
/* Index: idx_appuser_movie_movie                               */
/*==============================================================*/
CREATE INDEX idx_appuser_movie_movie ON AppUser_Movie (movie_id);