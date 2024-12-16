INSERT INTO 
    users (nickname, password, email)
VALUES
    (
        'Эль Иванов',
        '4321',
        'morwes4@gmail.com'
    ),
    (
        'Кузьмич Петров',
        '4321',
        'badboy228@gmail.com'
    );

INSERT INTO
    admins(user_id)
VALUES
    (
        1
    );

-- Добавление данных в таблицу vehicles
INSERT INTO vehicles (type, capacity, registration_number)
VALUES
    ('Автобус', 50, 'AB1234'),
    ('Троллейбус', 70, 'TR5678'),
    ('Трамвай', 90, 'TM9101');

-- Добавление данных в таблицу drivers
INSERT INTO drivers (name, license_number, experience_years)
VALUES
    ('Иван Петров', 'LIC-001', 10),
    ('Сергей Иванов', 'LIC-002', 5),
    ('Анна Сидорова', 'LIC-003', 7);

-- Добавление данных в таблицу routes
INSERT INTO routes (start_point, end_point, distance, stops, vehicle_id)
VALUES
    ('Центральная площадь', 'Вокзал', 10.5, '[{"name":"Улица Ленина","time":"08:10"},{"name":"Пр. Мира","time":"08:15"}]', 1),
    ('Автовокзал', 'Парк Горького', 8.0, '[{"name":"Кинотеатр Родина","time":"09:00"},{"name":"Улица Советская","time":"09:10"}]', 2);

-- Добавление данных в таблицу stops
INSERT INTO stops (name, location, route_id)
VALUES
    ('Улица Ленина', 'г. Москва, ул. Ленина, д.5', 1),
    ('Пр. Мира', 'г. Москва, просп. Мира, д.10', 1),
    ('Кинотеатр Родина', 'г. Москва, ул. Гоголя, д.20', 2),
    ('Улица Советская', 'г. Москва, ул. Советская, д.15', 2);

-- Добавление данных в таблицу schedules
INSERT INTO schedules (route_id, departure_time, arrival_time)
VALUES
    (1, '2024-12-14 08:00:00', '2024-12-14 08:30:00'),
    (1, '2024-12-14 10:00:00', '2024-12-14 10:30:00'),
    (2, '2024-12-14 09:00:00', '2024-12-14 09:40:00');

-- Добавление данных в таблицу tickets
INSERT INTO tickets (route_id, price, purchase_date, passenger_name)
VALUES
    (1, 50.00, '2024-12-13 07:55:00', 'Петров Алексей'),
    (1, 50.00, '2024-12-13 07:57:00', 'Иванов Олег'),
    (2, 60.00, '2024-12-13 08:45:00', 'Сидорова Анна');

-- Добавление данных в таблицу shifts
INSERT INTO shifts (driver_id, route_id, shift_start, shift_end)
VALUES
    (1, 1, '2024-12-14 07:00:00', '2024-12-14 11:00:00'),
    (2, 1, '2024-12-14 11:00:00', '2024-12-14 15:00:00'),
    (3, 2, '2024-12-14 08:30:00', '2024-12-14 12:30:00');
