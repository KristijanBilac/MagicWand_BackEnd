CREATE TABLE magic_wands (
    wand_id SERIAL PRIMARY KEY,
    flexibility VARCHAR(50) NOT NULL,
    owner_id INT REFERENCES users(user_id),
    length NUMERIC NOT NULL,
    wood VARCHAR(50) NOT NULL CHECK (wood IN ('alder', 'acacia', 'apple', 'ash', 'blackthorn', 'cherry'))
);
