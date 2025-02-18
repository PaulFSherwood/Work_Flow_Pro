-- Insert Users
INSERT INTO Users (username, password, is_manager, is_mantenance, is_logistics)
VALUES
    ('manager', 'password', TRUE, FALSE, FALSE),
    ('maintenance', 'password', FALSE, TRUE, FALSE),
    ('logistics', 'password', FALSE, FALSE, TRUE);

-- Insert Simulators
INSERT INTO Simulators (model, date_installed, last_maintenance_date, status)
VALUES
    ('737', CURDATE(), CURDATE(), 'Active'),
    ('747', CURDATE(), CURDATE(), 'Active');

-- Insert Subsystems
INSERT INTO Subsystems (name)
VALUES
    ('Hydraulics'),
    ('Electrical');

-- Insert Simulator_Subsystems
INSERT INTO Simulator_Subsystems (simulator_id, subsystem_id, status)
VALUES
    (1, 1, 'Active'),
    (1, 2, 'Active'),
    (2, 1, 'Active'),
    (2, 2, 'Active');

-- Insert Missions
INSERT INTO Missions (name)
VALUES
    ('Training Flight'),
    ('Test Flight');

-- Insert Parts
INSERT INTO Parts (name, cost, stock_number)
VALUES
    ('Part1', 100.00, 123456),
    ('Part2', 200.00, 123457);

-- Insert Logistics
INSERT INTO Logistics (item_name, minimum_stock_number, stock_location, cost_per_item, entered_by, unique_identifier, notes, repair_cost, vendor, original_part_number, serial_number, national_stock_number, location_type, preferred_repair_vendor, due_date, priority)
VALUES
    ('Item1', 10, 'Location1', 50.00, 3, '123-ABC', 'Sample Note', 5.00, 'Vendor1', '123', '456', '789', 'Electrical', 'Vendor1', CURDATE(), 1);

-- Insert Inventory_Audit
INSERT INTO Inventory_Audit (stock_number, date, type)
VALUES
    (1, CURDATE(), 'Wall to Wall');

-- Insert Maintenance_Schedule
INSERT INTO Maintenance_Schedule (simulator_id, next_maintenance_date)
VALUES
    (1, DATE_ADD(CURDATE(), INTERVAL 1 WEEK));

-- Insert Preflight_Schedule
INSERT INTO Preflight_Schedule (simulator_id, preflight_date)
VALUES
    (1, DATE_ADD(CURDATE(), INTERVAL 1 DAY));

-- Insert Write_Up_Templates
INSERT INTO Write_Up_Templates (description)
VALUES
    ('Template1'),
    ('Template2');

-- Insert WorkOrders
INSERT INTO WorkOrders (simulator_id, subsystem_id, creation_date, update_date, total_time, creation_reason, correction_note, parts_added_removed, sign_off_date, signed_off_by, priority, reported_by_name, notes, hours, disposition)
VALUES
    (1, 1, CURDATE(), CURDATE(), 1.00, 'Initial work order', 'Work order completed', 'Part1', CURDATE(), 2, 1, 'maintenance', 'No additional notes', 1.00, 'AWM');

-- Insert WorkOrder_Missions
INSERT INTO WorkOrder_Missions (jcn, mission_id)
VALUES
    (1, 1);

-- Insert WorkOrder_Parts
INSERT INTO WorkOrder_Parts (jcn, part_id, quantity)
VALUES
    (1, 1, 1);
