PROGRAM example;
VAR x, y : INTEGER;
BEGIN
    READ (x);
    READ (y);
    WHILE (x <> 0) OR (y <> 0) DO
    BEGIN
        WRITE (x + y);
        READ (x);
        READ (y)
    END
END.