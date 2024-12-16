# Платформа для управления общественным транспортом

---

### **Модели предметной области**

1. **Маршрут (Route)**  
   - **Назначение:** Хранение информации о маршрутах общественного транспорта.  
   - **Основные атрибуты:** `route_id` (уникальный идентификатор маршрута), `start_point` (начальная точка), `end_point` (конечная точка), `distance` (длина маршрута), `stops` (перечень остановок).

2. **Водитель (Driver)**  
   - **Назначение:** Хранение данных о водителях, работающих на маршрутах.  
   - **Основные атрибуты:** `driver_id` (уникальный идентификатор), `name`, `license_number` (номер лицензии), `experience_years` (стаж работы).

3. **Транспортное средство (Vehicle)**  
   - **Назначение:** Хранение данных о транспорте, используемом для перевозок.  
   - **Основные атрибуты:** `vehicle_id` (уникальный идентификатор), `type` (тип транспорта — автобус, трамвай и т.д.), `capacity` (вместимость), `registration_number` (госномер).

4. **Билет (Ticket)**  
   - **Назначение:** Учет продажи билетов пассажирам.  
   - **Основные атрибуты:** `ticket_id`, `route_id` (маршрут), `price` (цена билета), `purchase_date` (дата покупки), `passenger_name`.

5. **Остановка (Stop)**  
   - **Назначение:** Хранение информации о остановках маршрута.  
   - **Основные атрибуты:** `stop_id`, `name`, `location` (географические координаты).

---

### **Модели уровня инфраструктуры**

1. **Расписание (Schedule)**  
   - **Назначение:** Хранение данных о расписаниях для маршрутов.  
   - **Основные атрибуты:** `schedule_id`, `route_id`, `departure_time` (время отправления), `arrival_time` (время прибытия).

2. **Смена водителей (Shift)**  
   - **Назначение:** Управление сменами водителей.  
   - **Основные атрибуты:** `shift_id`, `driver_id`, `route_id`, `shift_start`, `shift_end`.

3. **Продажи билетов (TicketSales)**  
   - **Назначение:** Хранение агрегированных данных по продажам билетов.  
   - **Основные атрибуты:** `sales_id`, `date`, `total_tickets`, `total_revenue`.

4. **Инциденты (Incidents)**  
   - **Назначение:** Регистрация инцидентов, произошедших во время перевозок.  
   - **Основные атрибуты:** `incident_id`, `route_id`, `vehicle_id`, `driver_id`, `description`, `incident_date`.

5. **Пассажиры (Passenger)**  
   - **Назначение:** Учет данных о пассажирах, если требуется персонализация.  
   - **Основные атрибуты:** `passenger_id`, `name`, `contact_info`.

---


# Setup:
1. 
``` 
docker-compose --env-file env.env up -d
```

2. 
``` 
docker exec -i coursework_postgres psql -U postgres -d postgres < migrations/ddl.sql
docker exec -i coursework_postgres psql -U postgres -d postgres < migrations/dml.sql
``` 
OR
```
python init.py
```

```
python passw.py
```

3. Run app:
```
streamlit run main.py
```