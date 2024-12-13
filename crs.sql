CREATE TABLE `car` (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    make TEXT,
    model TEXT,
    year INT,
    registration TEXT,
    daily_rate REAL,
    available INT DEFAULT 1
);

CREATE TABLE `customer` (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT
);

INSERT INTO
    customer (id, first_name, last_name, email, phone)
VALUES
    (
        1,
        'John',
        'Smith',
        'john.smith@email.com',
        '555-0101'
    ),
    (
        2,
        'Mary',
        'Johnson',
        'mary.j@email.com',
        '555-0102'
    ),
    (
        3,
        'Robert',
        'Williams',
        'rwilliams@email.com',
        '555-0103'
    ),
    (
        4,
        'Patricia',
        'Brown',
        'pbrown@email.com',
        '555-0104'
    ),
    (
        5,
        'Michael',
        'Jones',
        'mjones@email.com',
        '555-0105'
    ),
    (
        6,
        'Linda',
        'Garcia',
        'lgarcia@email.com',
        '555-0106'
    ),
    (
        7,
        'James',
        'Miller',
        'james.miller@email.com',
        '555-0107'
    ),
    (
        8,
        'Jennifer',
        'Davis',
        'jdavis@email.com',
        '555-0108'
    ),
    (
        9,
        'William',
        'Rodriguez',
        'wrodriguez@email.com',
        '555-0109'
    ),
    (
        10,
        'Elizabeth',
        'Martinez',
        'emartinez@email.com',
        '555-0110'
    ),
    (
        11,
        'David',
        'Hernandez',
        'dhernandez@email.com',
        '555-0111'
    ),
    (
        12,
        'Barbara',
        'Lopez',
        'blopez@email.com',
        '555-0112'
    ),
    (
        13,
        'Richard',
        'Gonzalez',
        'rgonzalez@email.com',
        '555-0113'
    ),
    (
        14,
        'Susan',
        'Wilson',
        'swilson@email.com',
        '555-0114'
    ),
    (
        15,
        'Joseph',
        'Anderson',
        'janderson@email.com',
        '555-0115'
    ),
    (
        16,
        'Jessica',
        'Thomas',
        'jthomas@email.com',
        '555-0116'
    ),
    (
        17,
        'Thomas',
        'Taylor',
        'ttaylor@email.com',
        '555-0117'
    ),
    (
        18,
        'Sarah',
        'Moore',
        'smoore@email.com',
        '555-0118'
    ),
    (
        19,
        'Charles',
        'Jackson',
        'cjackson@email.com',
        '555-0119'
    ),
    (
        20,
        'Karen',
        'White',
        'kwhite@email.com',
        '555-0120'
    );

INSERT INTO
    car (id, make, model, year, registration, daily_rate)
VALUES
    (1, 'Toyota', 'Corolla', 2020, 'ABC123', 45.00),
    (2, 'Honda', 'Civic', 2019, 'DEF456', 48.00),
    (3, 'Ford', 'Focus', 2021, 'GHI789', 50.00),
    (4, 'Volkswagen', 'Golf', 2020, 'JKL012', 52.00),
    (5, 'Hyundai', 'Elantra', 2021, 'MNO345', 47.00),
    (6, 'Mazda', '3', 2019, 'PQR678', 49.00),
    (7, 'Nissan', 'Sentra', 2020, 'STU901', 46.00),
    (8, 'Kia', 'Forte', 2021, 'VWX234', 45.00),
    (9, 'Chevrolet', 'Cruze', 2019, 'YZA567', 48.00),
    (10, 'BMW', '3 Series', 2020, 'BCD890', 75.00),
    (11, 'Mercedes', 'C-Class', 2021, 'EFG123', 80.00),
    (12, 'Audi', 'A4', 2020, 'HIJ456', 78.00),
    (13, 'Lexus', 'IS', 2019, 'KLM789', 77.00),
    (14, 'Tesla', 'Model 3', 2021, 'NOP012', 85.00),
    (15, 'Subaru', 'Impreza', 2020, 'QRS345', 51.00),
    (16, 'Volvo', 'S60', 2019, 'TUV678', 65.00),
    (17, 'Chrysler', '300', 2020, 'WXY901', 60.00),
    (18, 'Dodge', 'Charger', 2021, 'ZAB234', 65.00),
    (19, 'Jeep', 'Cherokee', 2020, 'CDE567', 70.00),
    (20, 'Acura', 'TLX', 2021, 'FGH890', 72.00);
