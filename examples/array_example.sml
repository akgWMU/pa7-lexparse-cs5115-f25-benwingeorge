PROGRAM arrayexample;
VAR i   : INTEGER;
    arr : ARRAY [ 1 .. 5 ] OF INTEGER;
BEGIN
    i := 1;

    { Read 5 elements into the array }
    WHILE (i <= 5) DO
    BEGIN
        READ (arr[i]);
        i := i + 1
    END;

    i := 1;

    { Write 5 elements from the array }
    WHILE (i <= 5) DO
    BEGIN
        WRITE (arr[i]);
        i := i + 1
    END
END.