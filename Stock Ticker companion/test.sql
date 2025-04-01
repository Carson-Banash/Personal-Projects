-- CREATE TABLE player_info (
--     id INTEGER PRIMARY KEY,
--     recent INTEGER,
--     name TEXT,
--     cash INTEGER,
--     grain INTEGER,
--     ind INTEGER,
--     bonds INTEGER,  
--     oil INTEGER,
--     silver INTEGER,
--     gold INTEGER
-- );

-- BOARD INFO TABLE INITIALIZATION
/*
CREATE TABLE board_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grain INTEGER,
    ind INTEGER,
    bonds INTEGER,  
    oil INTEGER,
    silver INTEGER,
    gold INTEGER
);

INSERT INTO board_info VALUES (NULL, 1000,1000,1000,1000,1000,1000);
*/

-- SELECT * FROM player_info WHERE name='Gracie' AND recent=(SELECT max(recent) FROM player_info WHERE name='Gracie');
-- SELECT * FROM player_info WHERE name='Mom' AND recent=(SELECT max(recent) FROM player_info WHERE name='Mom');

-- SELECT DISTINCT name FROM player_info WHERE name=* RECENT=(SELECT max(RECENT) FROM player_info);