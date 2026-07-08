DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE orders (
    id          INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    total       REAL NOT NULL,
    status      TEXT NOT NULL
);

INSERT INTO customers (id, name, email) VALUES
    (1, 'Ada Lovelace',   'ada@example.com'),
    (2, 'Alan Turing',    'alan@example.com'),
    (3, 'Grace Hopper',   'grace@example.com');

INSERT INTO orders (id, customer_id, total, status) VALUES
    (100, 1, 250.00, 'paid'),
    (101, 1,  80.50, 'pending'),
    (102, 2, 999.99, 'paid'),
    (103, 3,  12.00, 'cancelled');
