CREATE TABLE movie_db.db_manager(  
    username VARCHAR(20),  
    password VARCHAR(20),     
    PRIMARY KEY(username) 
);

CREATE TABLE movie_db.audience(  
	name VARCHAR(20),     
    surname VARCHAR(20),     
    password VARCHAR(20),     
    username VARCHAR(20),     
    PRIMARY KEY(username) 
);

CREATE TABLE movie_db.director(  
	name VARCHAR(20),     
    surname VARCHAR(20),     
    password VARCHAR(20),  
    username VARCHAR(20),     
    nation VARCHAR(20) NOT NULL, 
    PRIMARY KEY(username) 
);

CREATE TABLE movie_db.experienced_director(  
	name VARCHAR(20),     
    surname VARCHAR(20),     
    password VARCHAR(20),     
    username VARCHAR(20),     
    nation VARCHAR(20) NOT NULL, 
    PRIMARY KEY(username) 
);

CREATE TABLE movie_db.rating_platform(  
	platform_id INT,     
    platform_name VARCHAR(20),     
    PRIMARY KEY(platform_id),     
    UNIQUE(platform_name) 
);

CREATE TABLE movie_db.movie(  
	movie_id INT,     
    duration INT,     
    movie_name VARCHAR(20),     
    average_rating FLOAT DEFAULT 0.0,
    reviewer_num INT DEFAULT 0,
    PRIMARY KEY(movie_id) 
);

CREATE TABLE movie_db.genre(  
	genre_id INT,     
    genre_name VARCHAR(20),     
    PRIMARY KEY(genre_id),     
    UNIQUE(genre_name)
);

CREATE TABLE movie_db.movie_session(  
	date VARCHAR(20),     
    time_slot INT,     
    PRIMARY KEY(date, time_slot) 
);

CREATE TABLE movie_db.theater(  
	theater_id INT, 
    theater_name VARCHAR(20),
    theater_capacity INT,     
    theater_district VARCHAR(20),     
    PRIMARY KEY(theater_id) 
);

CREATE TABLE movie_db.in_host(
	date VARCHAR(20),     
    time_slot INT, 
    theater_id INT, 
	PRIMARY KEY (date, time_slot, theater_id),
	FOREIGN KEY (date, time_slot) REFERENCES movie_session(date, time_slot)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (theater_id) REFERENCES theater(theater_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE movie_db.in_session(
	movie_id INT,
    session_id INT,
	date VARCHAR(20),     
    time_slot INT, 
    theater_id INT, 
    PRIMARY KEY (session_id, movie_id),
    UNIQUE(session_id),
	UNIQUE (date, time_slot, theater_id),
	FOREIGN KEY (date, time_slot, theater_id) REFERENCES in_host(date, time_slot, theater_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE movie_db.contract(
    username VARCHAR(20),
    platform_id INT,
    PRIMARY KEY (username),
    FOREIGN KEY (username) REFERENCES experienced_director(username)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (platform_id) REFERENCES rating_platform(platform_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE movie_db.directed_by(
	movie_id INT,
    username VARCHAR(20),
    PRIMARY KEY (movie_id),
	FOREIGN KEY (movie_id) REFERENCES movie(movie_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (username) REFERENCES contract(username)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE movie_db.which_genre(
	movie_id INT,
    genre_name VARCHAR(20),
    PRIMARY KEY (movie_id, genre_name),
	FOREIGN KEY (movie_id) REFERENCES movie(movie_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (genre_name) REFERENCES genre(genre_name)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE movie_db.preceded(
	child_movie_id INT,
    predecessor_movie_id INT,
    PRIMARY KEY (child_movie_id, predecessor_movie_id),
	FOREIGN KEY (child_movie_id) REFERENCES movie(movie_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (predecessor_movie_id) REFERENCES movie(movie_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE movie_db.subscribe(
	audience_username VARCHAR(20), 
    platform_id INT,
    PRIMARY KEY (audience_username, platform_id),
	FOREIGN KEY (audience_username) REFERENCES audience(username)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (platform_id) REFERENCES rating_platform(platform_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE movie_db.ticket(
	ticket_no VARCHAR(20),
	purchaser VARCHAR(20),
    session_id INT,
    movie_id INT,
    PRIMARY KEY (ticket_no, purchaser, movie_id),
    UNIQUE(ticket_no),
	FOREIGN KEY (purchaser) REFERENCES audience(username)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (session_id, movie_id) REFERENCES in_session(session_id, movie_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE movie_db.review(
	rating FLOAT,
    ticket_no VARCHAR(20),
	subscribed_audience VARCHAR(20),
    movie_id INT,
    reviewer_platform_id INT,
    PRIMARY KEY (subscribed_audience, movie_id),
    FOREIGN KEY (ticket_no, subscribed_audience, movie_id) REFERENCES ticket(ticket_no, purchaser, movie_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
	FOREIGN KEY (subscribed_audience, reviewer_platform_id) REFERENCES subscribe(audience_username, platform_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

DELIMITER //

CREATE TRIGGER movie_db.update_avg_rating
AFTER INSERT ON movie_db.review
FOR EACH ROW
BEGIN
    DECLARE existing_rating FLOAT;
    DECLARE existing_reviewers INT;

    SELECT average_rating, reviewer_num INTO existing_rating, existing_reviewers
    FROM movie_db.movie
    WHERE movie_id = NEW.movie_id;

    UPDATE movie_db.movie
    SET average_rating = (existing_rating * existing_reviewers + NEW.rating) / (existing_reviewers + 1),
        reviewer_num = existing_reviewers + 1
    WHERE movie_id = NEW.movie_id;
END //

DELIMITER ;