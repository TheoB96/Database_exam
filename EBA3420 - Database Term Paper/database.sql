
/*Movie table*/
CREATE TABLE "movie" (
    "movie_id" INT(4) NOT NULL,
    "movie_title" VARCHAR(50),
    "movie_description" VARCHAR(1000),
    PRIMARY KEY("movie_id")
);

/*Movie sample data*/
INSERT INTO movie (movie_id,movie_title,movie_description )
VALUES
    ("1", "Spider-Man: No Way Home", "With Spider-Man's identity now revealed, Peter asks Doctor Strange for help. When a spell goes wrong, dangerous foes from other worlds start to appear, forcing Peter to discover what it truly means to be Spider-Man. "),
    ("2", "No Time to Die", "James Bond has left active service. His peace is short-lived when Felix Leiter, an old friend from the CIA, turns up asking for help, leading Bond onto the trail of a mysterious villain armed with dangerous new technology. "),
    ("3", "The Godfather", "The aging patriarch of an organized crime dynasty in postwar New York City transfers control of his clandestine empire to his reluctant youngest son. "),
    ("4", "Fire Island", "A pair of best friends set out to have a legendary week-long summer vacation with the help of cheap rosé and a group of eclectic friends. "),
    ("5", "Forrest Gump", "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75, whose only desire is to be reunited with his childhood sweetheart. "),
    ("6", "The Matrix", "When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth--the life he knows is the elaborate deception of an evil cyber-intelligence. "),
    ("7", "Interstellar", "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival. "),
    ("8", "WALL·E", "In the distant future, a small waste-collecting robot inadvertently embarks on a space journey that will ultimately decide the fate of mankind. ");

/*Auditorium table*/
CREATE TABLE "auditorium" (
    "auditorium_id" INT(4) NOT NULL,
    "auditorium_name" VARCHAR(4),
    "auditorium_capacity" INT(1000),
    PRIMARY KEY("auditorium_id")
);

/*Auditorium sample data*/
INSERT INTO auditorium (auditorium_id,auditorium_name,auditorium_capacity)
VALUES ("1", "A1", "500"),
("2", "A2", "300"),
("3", "B1", "100"),
("4", "B2", "50");

/*Cinema viewings table*/
CREATE TABLE "cinema_viewings" (
    "program_id" INT(4) NOT NULL,
    "movie_id" INT(4) NOT NULL,
    "auditorium_id" INT(4) NOT NULL,
    "ticket_price" INT(1000),
    "date_time" DATETIME,
    PRIMARY KEY("program_id")
);

/*Cinema viewings sample data*/

INSERT INTO cinema_viewings (program_id,movie_id,auditorium_id,ticket_price,date_time)
VALUES ("1", "1", "1", "499", "2022-05-14 20:00:00"),
("2", "2", "1", "499", "2022-05-15 20:00:00"),
("3", "3", "4", "359", "2022-05-16 12:00:00"),
("4", "4", "3", "359", "2022-05-21 12:00:00"),
("5", "2", "2", "299", "2022-05-21 12:00:00"),
("6", "5", "1", "379", "2022-05-21 12:00:00"),
("7", "8", "1", "329", "2022-05-18 17:00:00");


/*Booking table*/
CREATE TABLE "booking" (
    "order_id" INT(4) NOT NULL,
    "program_id" INT(4) NOT NULL,
    "user_id" INT(4) NOT NULL,
    "tickets" INT(4),
    PRIMARY KEY("order_id")
);

/*Users table*/
CREATE TABLE "users" (
    "user_id" INT(4) NOT NULL,
    "last_name" VARCHAR(50),
    "first_name" VARCHAR(50),
    "email" VARCHAR(100) UNIQUE,
    "phone_number" INT(8),
    PRIMARY KEY("user_id")
);

/*Users sample data*/

INSERT INTO users (user_id,last_name,first_name,email,phone_number )
VALUES ("1", "Musk", "Elon", "musk@bi.no", "99999999"),
    ("2", "Bezos", "Jeff", "bezos@bi.no", "98989898"),
    ("3", "Fredriksen", "John", "fredriksen@bi.no", "97979797"),
    ("4", "Andreas", "Ole Halvorsen", "andreas@bi.no", "96969696"),
    ("5", "Reitan", "Odd", "reitan@bi.no", "95959595"),
    ("6", "Johannson", "Johan", "johannson@bi.no", "94949494"),
    ("7", "Witzøe", "Gustav ", "witzøe@bi.no", "93939393"),
    ("8", "Andresen", "Johan H. ", "andresen@bi.no", "92929292"),
    ("9", "Tollefsen", "Ivar Erik ", "tollefsen@bi.no", "91919191"),
    ("10", "Røkke", "Kjell Inge", "røkke@bi.no", "90909090"),
    ("11", "Stordalen", "Petter", "stordalen@bi.no", "89898989"),
    ("12", "Hagen", "Stein Erik", "hagen@bi.no", "88888888");