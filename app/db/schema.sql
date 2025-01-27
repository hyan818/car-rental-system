CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role_id INTEGER,
    last_login DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles (role_id)
);

CREATE TABLE roles (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE staff (
    staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT NOT NULL,
    address TEXT,
    driver_license TEXT UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);

CREATE TABLE vehicles (
    vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
    make TEXT NOT NULL,
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
        rental_status IN (
            'apply',
            'active',
            'reject',
            'completed',
            'cancelled'
        )
    ) DEFAULT 'apply',
    total_cost DECIMAL(10, 2),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles (vehicle_id),
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
    FOREIGN KEY (staff_id) REFERENCES staff (staff_id)
);

INSERT INTO
    roles (role_name)
VALUES
    ('staff'),
    ('customer');

INSERT INTO
    users (username, password, role_id)
VALUES
    (
        'admin',
        '$2b$12$LWdTnqauV6Qxv2wcKl306ehLM0zUCKlvFKJiY5NF7qLySZD6qBxQS',
        1
    );

INSERT INTO
    staff (user_id, full_name, email)
VALUES
    (1, 'Admin User', 'admin@email.com');

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
