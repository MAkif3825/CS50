-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Find crime scene description
SELECT description FROM crime_scene_reports
WHERE year = 2021
AND month = 7
AND day = 28;
-- Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
--Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.

--Find interviews of wittnesses
SELECT transcript FROM interviews WHERE year = 2021 AND month = 7 AND day = 28;
-- RUTH: Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
--If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.

--EUGENE:I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery,
--I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.

--RAYMOND: As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were
--planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.


--Find license plates of suspects
SELECT license_plate FROM bakery_security_logs
WHERE year = 2021 AND month = 7 AND day = 28 AND activity = 'entrance' AND ((hour < 10) OR (hour = 10 AND minute < 15))
INTERSECT
SELECT license_plate FROM bakery_security_logs
WHERE year = 2021 AND month = 7 AND day = 28 AND activity = 'exit' AND hour = 10 AND (minute > 15 AND minute < 26);


--Find the names of suspects
SELECT * FROM people
WHERE license_plate IN
(SELECT license_plate FROM bakery_security_logs
WHERE year = 2021 AND month = 7 AND day = 28 AND activity = 'entrance' AND ((hour < 10) OR (hour = 10 AND minute < 15))
INTERSECT
SELECT license_plate FROM bakery_security_logs
WHERE year = 2021 AND month = 7 AND day = 28 AND activity = 'exit' AND hour = 10 AND (minute > 15 AND minute < 26));


--Check ATM
SELECT * FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street';

--Find people withdrawing money among suspects
SELECT * FROM people WHERE id IN(SELECT person_id FROM bank_accounts WHERE account_number IN
(SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street'))
INTERSECT
SELECT * FROM people
WHERE license_plate IN
(SELECT license_plate FROM bakery_security_logs
WHERE year = 2021 AND month = 7 AND day = 28 AND activity = 'entrance' AND ((hour < 10) OR (hour = 10 AND minute < 15))
INTERSECT
SELECT license_plate FROM bakery_security_logs
WHERE year = 2021 AND month = 7 AND day = 28 AND activity = 'exit' AND hour = 10 AND (minute > 15 AND minute < 26));

--Check phone calls
SELECT * FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60;

--Find people calling sbd among suspects
SELECT * FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60)
INTERSECT
SELECT * FROM people WHERE id IN(SELECT person_id FROM bank_accounts WHERE account_number IN
(SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street'))
INTERSECT
SELECT * FROM people
WHERE license_plate IN
(SELECT license_plate FROM bakery_security_logs
WHERE year = 2021 AND month = 7 AND day = 28 AND activity = 'entrance' AND ((hour < 10) OR (hour = 10 AND minute < 15))
INTERSECT
SELECT license_plate FROM bakery_security_logs
WHERE year = 2021 AND month = 7 AND day = 28 AND activity = 'exit' AND hour = 10 AND (minute > 15 AND minute < 26));

--Find the earliest flight
SELECT * FROM flights WHERE
origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville') AND year = 2021 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1;

--Find passengers
SELECT * FROM passengers WHERE flight_id =
(SELECT id FROM flights WHERE origin_airport_id = (SELECT id FROM airports
WHERE city = 'Fiftyville') AND year = 2021 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1);

--Find the man among the suspects
SELECT * from people WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id =
(SELECT id FROM flights WHERE origin_airport_id = (SELECT id FROM airports
WHERE city = 'Fiftyville') AND year = 2021 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1));

--Find the thief
SELECT people.id,name,phone_number,passport_number,license_plate FROM people JOIN phone_calls ON people.phone_number = phone_calls.caller WHERE
caller IN (SELECT phone_number from people WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id =
(SELECT id FROM flights WHERE origin_airport_id = (SELECT id FROM airports
WHERE city = 'Fiftyville') AND year = 2021 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1)))
INTERSECT
SELECT * FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60)
INTERSECT
SELECT * FROM people WHERE id IN(SELECT person_id FROM bank_accounts WHERE account_number IN
(SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street'))
INTERSECT
SELECT * FROM people
WHERE license_plate IN
(SELECT license_plate FROM bakery_security_logs
WHERE year = 2021 AND month = 7 AND day = 28 AND activity = 'entrance' AND ((hour < 10) OR (hour = 10 AND minute < 15))
INTERSECT
SELECT license_plate FROM bakery_security_logs
WHERE year = 2021 AND month = 7 AND day = 28 AND activity = 'exit' AND hour = 10 AND (minute > 15 AND minute < 26));

--Find ACCOMPLISH
SELECT name FROM people JOIN phone_calls ON phone_calls.receiver = people.phone_number WHERE caller = (SELECT phone_number FROM people WHERE name = 'Bruce') AND year = 2021 AND month = 7 AND day = 28 AND duration < 60;

--Find City
SELECT city FROM airports WHERE id = (SELECT destination_airport_id FROM flights WHERE
origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville') AND year = 2021 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1);