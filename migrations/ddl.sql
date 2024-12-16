DROP TABLE IF EXISTS shifts CASCADE;
DROP TABLE IF EXISTS tickets CASCADE;
DROP TABLE IF EXISTS schedules CASCADE;
DROP TABLE IF EXISTS stops CASCADE;
DROP TABLE IF EXISTS routes CASCADE;
DROP TABLE IF EXISTS drivers CASCADE;
DROP TABLE IF EXISTS vehicles CASCADE;
DROP TABLE IF EXISTS admins CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS assignment_logs CASCADE;

DROP PROCEDURE IF EXISTS assign_drivers();

CREATE TABLE users(
    user_id SERIAL PRIMARY KEY,
    password TEXT,
    nickname VARCHAR(255) UNIQUE,
    email VARCHAR(255)
);

COMMENT ON TABLE users IS 'Информация о пользователях';
COMMENT ON COLUMN users.user_id IS 'Уникальный идентификатор пользователя';
COMMENT ON COLUMN users.nickname IS 'Имя пользователя';
COMMENT ON COLUMN users.email IS 'Email пользователя';

CREATE TABLE admins(
    admin_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE
);

-- Создание таблицы для ТС (автобусы, трамваи и т.п.)
CREATE TABLE vehicles (
    vehicle_id SERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    capacity INT NOT NULL,
    registration_number VARCHAR(100) UNIQUE NOT NULL
);

COMMENT ON TABLE vehicles IS 'Информация о транспортных средствах';
COMMENT ON COLUMN vehicles.vehicle_id IS 'Уникальный идентификатор ТС';
COMMENT ON COLUMN vehicles.type IS 'Тип ТС (автобус, трамвай, троллейбус и т.п.)';
COMMENT ON COLUMN vehicles.capacity IS 'Вместимость ТС';
COMMENT ON COLUMN vehicles.registration_number IS 'Регистрационный номер ТС';

-- Создание таблицы водителей
CREATE TABLE drivers (
    driver_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    license_number VARCHAR(100) UNIQUE NOT NULL,
    experience_years INT NOT NULL
);

COMMENT ON TABLE drivers IS 'Информация о водителях';
COMMENT ON COLUMN drivers.driver_id IS 'Уникальный идентификатор водителя';
COMMENT ON COLUMN drivers.name IS 'Имя водителя';
COMMENT ON COLUMN drivers.license_number IS 'Номер водительской лицензии';
COMMENT ON COLUMN drivers.experience_years IS 'Стаж (кол-во лет опыта)';

-- Создание таблицы маршрутов
-- В схеме присутствует поле stops: JSON, но также есть отдельная сущность Stops.
-- В данном случае предполагается хранить общую информацию о маршруте в таблице Routes,
-- а конкретные остановки будут связаны с маршрутом через таблицу Stops.
-- Поле stops: JSON можно оставить для дополнительной информации или для кэширования.
CREATE TABLE routes (
    route_id SERIAL PRIMARY KEY,
    start_point VARCHAR(100) NOT NULL,
    end_point VARCHAR(100) NOT NULL,
    distance FLOAT NOT NULL,
    stops JSON,
    vehicle_id INT REFERENCES vehicles(vehicle_id) ON DELETE SET NULL
);

COMMENT ON TABLE routes IS 'Информация о маршрутах';
COMMENT ON COLUMN routes.route_id IS 'Уникальный идентификатор маршрута';
COMMENT ON COLUMN routes.start_point IS 'Начальная точка маршрута';
COMMENT ON COLUMN routes.end_point IS 'Конечная точка маршрута';
COMMENT ON COLUMN routes.distance IS 'Длина маршрута';
COMMENT ON COLUMN routes.stops IS 'Дополнительная информация о промежуточных остановках (формат JSON)';
COMMENT ON COLUMN routes.vehicle_id IS 'Идентификатор ТС, которое используется на данном маршруте';

-- Создание таблицы остановок
CREATE TABLE stops (
    stop_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(255),
    route_id INT REFERENCES routes(route_id) ON DELETE CASCADE
);

COMMENT ON TABLE stops IS 'Информация об остановках';
COMMENT ON COLUMN stops.stop_id IS 'Уникальный идентификатор остановки';
COMMENT ON COLUMN stops.name IS 'Название остановки';
COMMENT ON COLUMN stops.location IS 'Местоположение остановки (адрес или координаты)';
COMMENT ON COLUMN stops.route_id IS 'Идентификатор маршрута, к которому относится остановка';

-- Создание таблицы расписания
CREATE TABLE schedules (
    schedule_id SERIAL PRIMARY KEY,
    route_id INT REFERENCES routes(route_id) ON DELETE CASCADE,
    departure_time TIMESTAMP NOT NULL,
    arrival_time TIMESTAMP NOT NULL
);

COMMENT ON TABLE schedules IS 'Расписание движения по маршруту';
COMMENT ON COLUMN schedules.schedule_id IS 'Уникальный идентификатор записи расписания';
COMMENT ON COLUMN schedules.route_id IS 'Идентификатор маршрута';
COMMENT ON COLUMN schedules.departure_time IS 'Время отправления';
COMMENT ON COLUMN schedules.arrival_time IS 'Время прибытия';

-- Создание таблицы билетов
CREATE TABLE tickets (
    ticket_id SERIAL PRIMARY KEY,
    route_id INT REFERENCES routes(route_id) ON DELETE CASCADE,
    price DECIMAL(10,2) NOT NULL,
    purchase_date TIMESTAMP NOT NULL,
    passenger_name VARCHAR(100) NOT NULL
);

COMMENT ON TABLE tickets IS 'Информация о билетах';
COMMENT ON COLUMN tickets.ticket_id IS 'Уникальный идентификатор билета';
COMMENT ON COLUMN tickets.route_id IS 'Идентификатор маршрута, для которого приобретен билет';
COMMENT ON COLUMN tickets.price IS 'Цена билета';
COMMENT ON COLUMN tickets.purchase_date IS 'Дата и время покупки билета';
COMMENT ON COLUMN tickets.passenger_name IS 'Имя пассажира, на которого оформлен билет';

-- Создание таблицы смен (шаблоны работы водителей)
CREATE TABLE shifts (
    shift_id SERIAL PRIMARY KEY,
    driver_id INT REFERENCES drivers(driver_id) ON DELETE CASCADE,
    route_id INT REFERENCES routes(route_id) ON DELETE CASCADE,
    shift_start TIMESTAMP NOT NULL,
    shift_end TIMESTAMP NOT NULL
);

COMMENT ON TABLE shifts IS 'Смены водителей';
COMMENT ON COLUMN shifts.shift_id IS 'Уникальный идентификатор смены';
COMMENT ON COLUMN shifts.driver_id IS 'Идентификатор водителя';
COMMENT ON COLUMN shifts.route_id IS 'Идентификатор маршрута';
COMMENT ON COLUMN shifts.shift_start IS 'Начало смены';
COMMENT ON COLUMN shifts.shift_end IS 'Окончание смены';



-- Процедура автоматически назначает водителей на маршруты на основе их опыта и времени смен

CREATE TABLE assignment_logs (
    log_id SERIAL PRIMARY KEY,
    route_id INT NOT NULL,
    log_message TEXT NOT NULL,
    log_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE PROCEDURE assign_drivers()
LANGUAGE plpgsql
AS $$
DECLARE
    route RECORD;
    driver RECORD;
BEGIN
    -- Проход по всем маршрутам без назначения
    FOR route IN 
        SELECT r.route_id, r.distance, s.departure_time, s.arrival_time
        FROM routes r
        JOIN schedules s ON r.route_id = s.route_id
        LEFT JOIN shifts sh ON r.route_id = sh.route_id
        WHERE sh.driver_id IS NULL
    LOOP
        -- Поиск водителя, подходящего по времени и опыту
        SELECT * INTO driver
        FROM drivers d
        WHERE d.experience_years >= route.distance / 10
          AND NOT EXISTS (
              SELECT 1 FROM shifts sh
              WHERE sh.driver_id = d.driver_id
                AND (
                    (sh.shift_start, sh.shift_end) OVERLAPS (route.departure_time, route.arrival_time)
                )
          )
        LIMIT 1;
        
        IF FOUND THEN
            -- Назначение водителя
            INSERT INTO shifts (driver_id, route_id, shift_start, shift_end)
            VALUES (driver.driver_id, route.route_id, route.departure_time, route.arrival_time);
        ELSE
            -- Логирование ошибки
            INSERT INTO assignment_logs (route_id, log_message)
            VALUES (route.route_id, 'Не найден подходящий водитель');
        END IF;
    END LOOP;
END;
$$;
