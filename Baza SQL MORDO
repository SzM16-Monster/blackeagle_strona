/*==============================================================*/
/* DBMS name:      Microsoft SQL Server 2012                    */
/* Created on:     17.04.2025 20:35:59                          */
/*==============================================================*/


if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('Movie_Genres') and o.name = 'FK_MOVIE_GE_RELATIONS_GENRES')
alter table Movie_Genres
   drop constraint FK_MOVIE_GE_RELATIONS_GENRES
go

if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('Movie_Genres') and o.name = 'FK_MOVIE_GE_RELATIONS_MOVIES')
alter table Movie_Genres
   drop constraint FK_MOVIE_GE_RELATIONS_MOVIES
go

if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('Movie_Language') and o.name = 'FK_MOVIE_LA_RELATIONS_MOVIES')
alter table Movie_Language
   drop constraint FK_MOVIE_LA_RELATIONS_MOVIES
go

if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('Movie_People') and o.name = 'FK_MOVIE_PE_RELATIONS_PEOPLE')
alter table Movie_People
   drop constraint FK_MOVIE_PE_RELATIONS_PEOPLE
go

if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('Movie_People') and o.name = 'FK_MOVIE_PE_RELATIONS_MOVIES')
alter table Movie_People
   drop constraint FK_MOVIE_PE_RELATIONS_MOVIES
go

if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('User_Movie') and o.name = 'FK_USER_MOV_RELATIONS_USER')
alter table User_Movie
   drop constraint FK_USER_MOV_RELATIONS_USER
go

if exists (select 1
   from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F')
   where r.fkeyid = object_id('User_Movie') and o.name = 'FK_USER_MOV_RELATIONS_MOVIES')
alter table User_Movie
   drop constraint FK_USER_MOV_RELATIONS_MOVIES
go

if exists (select 1
            from  sysobjects
           where  id = object_id('Genres')
            and   type = 'U')
   drop table Genres
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('Movie_Genres')
            and   name  = 'Relationship_5_FK'
            and   indid > 0
            and   indid < 255)
   drop index Movie_Genres.Relationship_5_FK
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('Movie_Genres')
            and   name  = 'Relationship_4_FK'
            and   indid > 0
            and   indid < 255)
   drop index Movie_Genres.Relationship_4_FK
go

if exists (select 1
            from  sysobjects
           where  id = object_id('Movie_Genres')
            and   type = 'U')
   drop table Movie_Genres
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('Movie_Language')
            and   name  = 'Relationship_8_FK'
            and   indid > 0
            and   indid < 255)
   drop index Movie_Language.Relationship_8_FK
go

if exists (select 1
            from  sysobjects
           where  id = object_id('Movie_Language')
            and   type = 'U')
   drop table Movie_Language
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('Movie_People')
            and   name  = 'Relationship_3_FK'
            and   indid > 0
            and   indid < 255)
   drop index Movie_People.Relationship_3_FK
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('Movie_People')
            and   name  = 'Relationship_2_FK'
            and   indid > 0
            and   indid < 255)
   drop index Movie_People.Relationship_2_FK
go

if exists (select 1
            from  sysobjects
           where  id = object_id('Movie_People')
            and   type = 'U')
   drop table Movie_People
go

if exists (select 1
            from  sysobjects
           where  id = object_id('Movies')
            and   type = 'U')
   drop table Movies
go

if exists (select 1
            from  sysobjects
           where  id = object_id('People')
            and   type = 'U')
   drop table People
go

if exists (select 1
            from  sysobjects
           where  id = object_id('"User"')
            and   type = 'U')
   drop table "User"
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('User_Movie')
            and   name  = 'Relationship_7_FK'
            and   indid > 0
            and   indid < 255)
   drop index User_Movie.Relationship_7_FK
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('User_Movie')
            and   name  = 'Relationship_6_FK'
            and   indid > 0
            and   indid < 255)
   drop index User_Movie.Relationship_6_FK
go

if exists (select 1
            from  sysobjects
           where  id = object_id('User_Movie')
            and   type = 'U')
   drop table User_Movie
go

/*==============================================================*/
/* Table: Genres                                                */
/*==============================================================*/
create table Genres (
   Genre_id             int                  not null,
   Genres_name          varchar(50)          not null,
   constraint PK_GENRES primary key nonclustered (Genre_id)
)
go

/*==============================================================*/
/* Table: Movie_Genres                                          */
/*==============================================================*/
create table Movie_Genres (
   Movie_genres_id      int                  not null,
   Genre_id             int                  null,
   Movie_id             int                  null,
   constraint PK_MOVIE_GENRES primary key nonclustered (Movie_genres_id)
)
go

/*==============================================================*/
/* Index: Relationship_4_FK                                     */
/*==============================================================*/
create index Relationship_4_FK on Movie_Genres (
Genre_id ASC
)
go

/*==============================================================*/
/* Index: Relationship_5_FK                                     */
/*==============================================================*/
create index Relationship_5_FK on Movie_Genres (
Movie_id ASC
)
go

/*==============================================================*/
/* Table: Movie_Language                                        */
/*==============================================================*/
create table Movie_Language (
   Movie_language_id    int                  not null,
   Movie_id             int                  null,
   Language             varchar(30)          not null,
   constraint PK_MOVIE_LANGUAGE primary key nonclustered (Movie_language_id)
)
go

/*==============================================================*/
/* Index: Relationship_8_FK                                     */
/*==============================================================*/
create index Relationship_8_FK on Movie_Language (
Movie_id ASC
)
go

/*==============================================================*/
/* Table: Movie_People                                          */
/*==============================================================*/
create table Movie_People (
   Movie_people_id      int                  not null,
   People_id            int                  null,
   Movie_id             int                  null,
   Role                 varchar(30)          not null,
   constraint PK_MOVIE_PEOPLE primary key nonclustered (Movie_people_id)
)
go

/*==============================================================*/
/* Index: Relationship_2_FK                                     */
/*==============================================================*/
create index Relationship_2_FK on Movie_People (
People_id ASC
)
go

/*==============================================================*/
/* Index: Relationship_3_FK                                     */
/*==============================================================*/
create index Relationship_3_FK on Movie_People (
Movie_id ASC
)
go

/*==============================================================*/
/* Table: Movies                                                */
/*==============================================================*/
create table Movies (
   Movie_id             int                  not null,
   Title                varchar(120)         not null,
   Year                 int                  not null,
   Rated                varchar(30)          not null,
   Released             datetime             not null,
   Runtime              int                  not null,
   Plot                 varchar(1024)        not null,
   Country              varchar(50)          not null,
   Awards               varchar(50)          not null,
   Poster               char(200)            not null,
   "Movie Database"     float(30)            not null,
   "Rotten Tomatoes"    float(30)            not null,
   Metacritic           float(30)            not null,
   Metascore            float(30)            not null,
   imdbRating           float(30)            not null,
   imdbVotes            float(30)            not null,
   imdbID               varchar(30)          not null,
   Type                 varchar(30)          not null,
   BoxOffice            varchar(50)          not null,
   Response             varchar(30)          not null,
   constraint PK_MOVIES primary key nonclustered (Movie_id)
)
go

/*==============================================================*/
/* Table: People                                                */
/*==============================================================*/
create table People (
   People_id            int                  not null,
   People_name          varchar(80)          not null,
   constraint PK_PEOPLE primary key nonclustered (People_id)
)
go

/*==============================================================*/
/* Table: "User"                                                */
/*==============================================================*/
create table "User" (
   User_id              int                  not null,
   First_name           varchar(30)          not null,
   Last_name            varchar(30)          not null,
   E_Mail               varchar(50)          not null,
   Username             varchar(30)          not null,
   PasswordHash         varchar(40)          not null,
   CreatedAt            datetime             not null,
   constraint PK_USER primary key nonclustered (User_id)
)
go

/*==============================================================*/
/* Table: User_Movie                                            */
/*==============================================================*/
create table User_Movie (
   User_movie_id        int                  not null,
   User_id              int                  null,
   Movie_id             int                  null,
   User_rated           varchar(30)          null,
   constraint PK_USER_MOVIE primary key nonclustered (User_movie_id)
)
go

/*==============================================================*/
/* Index: Relationship_6_FK                                     */
/*==============================================================*/
create index Relationship_6_FK on User_Movie (
User_id ASC
)
go

/*==============================================================*/
/* Index: Relationship_7_FK                                     */
/*==============================================================*/
create index Relationship_7_FK on User_Movie (
Movie_id ASC
)
go

alter table Movie_Genres
   add constraint FK_MOVIE_GE_RELATIONS_GENRES foreign key (Genre_id)
      references Genres (Genre_id)
go

alter table Movie_Genres
   add constraint FK_MOVIE_GE_RELATIONS_MOVIES foreign key (Movie_id)
      references Movies (Movie_id)
go

alter table Movie_Language
   add constraint FK_MOVIE_LA_RELATIONS_MOVIES foreign key (Movie_id)
      references Movies (Movie_id)
go

alter table Movie_People
   add constraint FK_MOVIE_PE_RELATIONS_PEOPLE foreign key (People_id)
      references People (People_id)
go

alter table Movie_People
   add constraint FK_MOVIE_PE_RELATIONS_MOVIES foreign key (Movie_id)
      references Movies (Movie_id)
go

alter table User_Movie
   add constraint FK_USER_MOV_RELATIONS_USER foreign key (User_id)
      references "User" (User_id)
go

alter table User_Movie
   add constraint FK_USER_MOV_RELATIONS_MOVIES foreign key (Movie_id)
      references Movies (Movie_id)
go

