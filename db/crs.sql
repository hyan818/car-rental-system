CREATE TABLE staff (
    staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME
);

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    address TEXT,
    driver_license TEXT UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE vehicles (
    vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    year INTEGER NOT NULL,
    license_plate TEXT UNIQUE NOT NULL,
    mileage INTEGER DEFAULT 0,
    daily_rate DECIMAL(10, 2) NOT NULL,
    description TEXT,
    status TEXT CHECK (status IN ('available', 'rented', 'maintenance')) DEFAULT 'available'
);

CREATE TABLE rentals (
    rental_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER,
    customer_id INTEGER,
    staff_id INTEGER,
    start_date DATETIME NOT NULL,
    expected_return_date DATETIME NOT NULL,
    actual_return_date DATETIME,
    initial_mileage INTEGER,
    return_mileage INTEGER,
    rental_status TEXT CHECK (
        rental_status IN ('active', 'completed', 'cancelled')
    ) DEFAULT 'active',
    total_cost DECIMAL(10, 2),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles (vehicle_id),
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
    FOREIGN KEY (staff_id) REFERENCES staff (staff_id)
);

CREATE TABLE maintenance (
    maintenance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER,
    staff_id INTEGER,
    description TEXT NOT NULL,
    maintenance_date DATETIME NOT NULL,
    cost DECIMAL(10, 2),
    status TEXT CHECK (status IN ('scheduled', 'ongoing', 'completed')) DEFAULT 'scheduled',
    completion_date DATETIME,
    notes TEXT,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles (vehicle_id),
    FOREIGN KEY (staff_id) REFERENCES staff (staff_id)
);

CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    rental_id INTEGER,
    amount DECIMAL(10, 2) NOT NULL,
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    payment_method TEXT,
    payment_status TEXT CHECK (
        payment_status IN ('pending', 'completed', 'failed')
    ) DEFAULT 'pending',
    FOREIGN KEY (rental_id) REFERENCES rentals (rental_id)
);

INSERT INTO
    staff (username, password, full_name, email)
VALUES
    (
        'admin',
        '{bcrypt}$2a$10$546FiLz/YDG81EIThLzSZeZIurLV.HB2rvuERmAs1zmsYzPvXmYDO',
        'Admin User',
        'admin@email.com'
    );

INSERT INTO
    customers (full_name, email, phone, address, driver_license)
VALUES
    (
        'John Smith',
        'john.smith@email.com',
        '555-0123',
        '123 Main St, Anytown, USA',
        'DL123456'
    ),
    (
        'Mary Johnson',
        'mary.j@email.com',
        '555-0124',
        '456 Oak Ave, Somewhere, USA',
        'DL234567'
    ),
    (
        'Robert Wilson',
        'rob.wilson@email.com',
        '555-0125',
        '789 Pine Rd, Elsewhere, USA',
        'DL345678'
    ),
    (
        'Sarah Davis',
        'sarah.d@email.com',
        '555-0126',
        '321 Elm St, Nowhere, USA',
        'DL456789'
    ),
    (
        'Michael Brown',
        'mike.b@email.com',
        '555-0127',
        '654 Maple Dr, Anywhere, USA',
        'DL567890'
    );
