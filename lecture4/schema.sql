/*
CREATE TABLE airport(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	code TEXT NOT NULL,
	city TEXT NOT NULL
);

CREATE TABLE flights(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	origin INTEGER NOT NULL REFERENCES airport(id),
	destination  INTEGER NOT NULL REFERENCES airport(id),
	duration INTEGER NOT NULL
);

CREATE TABLE person(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	first TEXT NOT NULL,
	last TEXT NOT NULL
);

CREATE TABLE passengers(
	person_id INTEGER NOT NULL REFERENCES person(id),
	flight_id INTEGER NOT NULL REFERENCES flights(id)
);
*/

-- 서브쿼리 방식(내가 생각한 방식)
SELECT 
	person.first, 
	person.last, 
	(SELECT city FROM airport WHERE id == flights.origin) AS origin,
	(SELECT city FROM airport WHERE id == flights.destination) AS destination

FROM passengers 
JOIN person ON passengers.person_id == person.id
JOIN flights ON passengers.flight_id == flights.id;

-- JOIN 방식(Coplilot이 더 추천해준 방식)
SELECT 
	person.first, 
	person.last, 
	origin_airport.city AS origin,
	dest_airport.city AS destination
FROM passengers 
JOIN person ON passengers.person_id == person.id
JOIN flights ON passengers.flight_id == flights.id
JOIN airport AS origin_airport ON origin_airport.id == flights.origin
JOIN airport AS dest_airport ON dest_airport.id == flights.destination;



/*
INSERT INTO airport (code, city) VALUES ('JFK', 'New York');
INSERT INTO airport (code, city) VALUES ('PVG', 'Shanghai');
INSERT INTO airport (code, city) VALUES ('IST', 'Istanbul');
INSERT INTO airport (code, city) VALUES ('LHR', 'London');
INSERT INTO airport (code, city) VALUES ('SVO', 'Moscow');
INSERT INTO airport (code, city) VALUES ('LIM', 'Lima');
INSERT INTO airport (code, city) VALUES ('CDG', 'Paris');
INSERT INTO airport (code, city) VALUES ('NRT', 'Tokyo');

INSERT INTO flights (origin, destination, duration) VALUES (1, 4, 415);
INSERT INTO flights (origin, destination, duration) VALUES (2, 7, 760);
INSERT INTO flights (origin, destination, duration) VALUES (3, 8, 700);
INSERT INTO flights (origin, destination, duration) VALUES (1, 7, 435);
INSERT INTO flights (origin, destination, duration) VALUES (5, 7, 245);
INSERT INTO flights (origin, destination, duration) VALUES (6, 1, 455);

INSERT INTO person (first, last) VALUES ('Harry', 'Potter');
INSERT INTO person (first, last) VALUES ('Ron', 'Weasley');
INSERT INTO person (first, last) VALUES ('Hermione', 'Granger');
INSERT INTO person (first, last) VALUES ('Draco', 'Malfoy');
INSERT INTO person (first, last) VALUES ('Luna', 'Lovegood');
INSERT INTO person (first, last) VALUES ('Ginny', 'Weasley');



INSERT INTO passengers (person_id, flight_id) VALUES (1, 1);
INSERT INTO passengers (person_id, flight_id) VALUES (2, 1);
INSERT INTO passengers (person_id, flight_id) VALUES (2, 4);
INSERT INTO passengers (person_id, flight_id) VALUES (3, 2);
INSERT INTO passengers (person_id, flight_id) VALUES (4, 4);
INSERT INTO passengers (person_id, flight_id) VALUES (5, 6);
INSERT INTO passengers (person_id, flight_id) VALUES (6, 6);
*/

