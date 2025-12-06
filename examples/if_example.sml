PROGRAM ifexample;
VAR a, b : INTEGER;
    x    : FLOAT;
BEGIN
    { Read two integers }
    READ (a);
    READ (b);

    IF (a = b) THEN
        WRITE ('equal')
    ELSE
    BEGIN
        WRITE ('notequal');

        IF (a > b) THEN
            WRITE (a)
        ELSE
            WRITE (b)
    END
END.