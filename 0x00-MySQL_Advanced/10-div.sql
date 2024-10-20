-- creates a function SafeDiv that divides (and returns) 
-- the first by the second number or returns 0 if the second number is equal to 0.
DROP FUNCTION IF EXISTS SafeDiv;
DELIMITER $$
CREATE FUNCTION SafeDiv (I INT, j INT)
RETURNS FLOAT DETERMINISTIC
BEGIN
    DECLARE result FLOAT DEFAULT 0;


    IF j != 0 THEN
	SET result = i / j;
    END IF;
    RETURN result;
END $$
DELIMITER ;
