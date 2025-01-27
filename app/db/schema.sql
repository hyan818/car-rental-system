PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE roles (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO roles VALUES(1,'staff','2024-12-31 09:45:50');
INSERT INTO roles VALUES(2,'customer','2024-12-31 09:45:50');
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role_id INTEGER,
    last_login DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles (role_id)
);
INSERT INTO users VALUES(1,'admin','$2b$12$LWdTnqauV6Qxv2wcKl306ehLM0zUCKlvFKJiY5NF7qLySZD6qBxQS',1,'2025-01-27 17:27:37.235554');
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
    email TEXT UNIQUE,
    phone TEXT,
    address TEXT,
    driver_license TEXT UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
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
INSERT INTO vehicles VALUES(1,'Toyota','Camry',2022,'ABC123',15000,45,'Comfortable midsize sedan with excellent fuel economy','available');
INSERT INTO vehicles VALUES(2,'Honda','CR-V',2021,'XYZ789',25000,55,'Popular compact SUV with plenty of cargo space','available');
INSERT INTO vehicles VALUES(3,'Ford','Mustang',2023,'MUS555',5000,75,'Sporty muscle car with powerful engine','available');
INSERT INTO vehicles VALUES(4,'BMW','3 Series',2022,'BMW444',20000,85,'Luxury sedan with premium features','available');
INSERT INTO vehicles VALUES(5,'Tesla','Model 3',2023,'TSL789',10000,95,'Electric vehicle with advanced autopilot','available');
INSERT INTO vehicles VALUES(6,'Mercedes','C-Class',2021,'MRC123',30000,80,'Elegant luxury sedan requiring scheduled service','available');
INSERT INTO vehicles VALUES(7,'Audi','Q5',2022,'AUD456',18000,75,'Premium SUV under routine maintenance','available');
INSERT INTO vehicles VALUES(8,'Volkswagen','Golf',2022,'VWG123',12000,40,'Compact hatchback with great handling','available');
INSERT INTO vehicles VALUES(9,'Hyundai','Tucson',2023,'HYN789',8100,50,'Modern SUV with latest safety features','available');
INSERT INTO vehicles VALUES(10,'Chevrolet','Malibu',2022,'CHV456',22000,45,'Reliable family sedan with good fuel efficiency','available');
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('roles',2);
INSERT INTO sqlite_sequence VALUES('users',1);
INSERT INTO sqlite_sequence VALUES('customers',1);
INSERT INTO sqlite_sequence VALUES('vehicles',11);
INSERT INTO sqlite_sequence VALUES('rentals',1);
INSERT INTO sqlite_sequence VALUES('staff',2);
COMMIT;