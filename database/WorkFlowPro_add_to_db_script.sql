-- Insert Users
INSERT INTO Users (username, password, is_manager, is_mantenance, is_logistics)
VALUES
    ('Anderson', '1234', TRUE, FALSE, FALSE),
    ('Bailey', '1234', FALSE, TRUE, FALSE),
    ('Carter', '1234', FALSE, FALSE, TRUE),
    ('Davis', '1234', TRUE, FALSE, FALSE),
    ('Edwards', '1234', FALSE, TRUE, FALSE),
    ('Foster', '1234', FALSE, FALSE, TRUE),
    ('Gray', '1234', TRUE, FALSE, FALSE),
    ('Hughes', '1234', FALSE, TRUE, FALSE),
    ('Jenkins', '1234', FALSE, FALSE, TRUE),
    ('King', '1234', TRUE, FALSE, FALSE);

-- Insert Simulators
INSERT INTO Simulators (model, date_installed, last_maintenance_date, status)
VALUES
    ('737', CURDATE(), CURDATE(), 'Active'),
    ('747', CURDATE(), CURDATE(), 'Active');

-- Insert Subsystems
INSERT INTO Subsystems (name)
VALUES
    ('Hydraulics'),
    ('Electrical'),
    ('Avionics'),
    ('Fuel Systems'),
    ('Propulsion'),
    ('Air Conditioning'),
    ('Environmental Control Systems'),
    ('Landing Gear'),
    ('Navigation Systems'),
    ('Communication Systems');

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
    ('Test Flight'),
    ('Search and Rescue'),
    ('Aerial Survey'),
    ('Medical Evacuation'),
    ('Cargo Transport'),
    ('Aerial Firefighting'),
    ('Passenger Transport'),
    ('Photography and Filming'),
    ('Scientific Research');

-- Insert Parts
INSERT INTO Parts (name, cost, stock_number)
VALUES
    ('ADI', 100.00, 123456),
    ('MFD', 200.00, 123457),
    ('ECU', 150.00, 123458),
    ('APU', 300.00, 123459),
    ('EFIS', 250.00, 123460),
    ('FMS', 180.00, 123461),
    ('TCAS', 220.00, 123462),
    ('RADAR', 280.00, 123463),
    ('TCM', 190.00, 123464),
    ('EGPWS', 230.00, 123465);


-- Insert Logistics
INSERT INTO Logistics 
    (item_name, minimum_stock_number, stock_location, cost_per_item, entered_by, unique_identifier, notes, repair_cost, vendor, original_part_number, serial_number, national_stock_number, location_type, preferred_repair_vendor, due_date, priority)
VALUES
    ('ADI', 10, '51c', 200.00, 3, '123-ABC', 'Sample Note 1', 20.00, 'Vendor1', '123', '456', '789', 'Electrical', 'Vendor1', '2023-01-01', 1),
    ('MFD', 10, '55a', 250.00, 3, '456-DEF', 'Sample Note 2', 30.00, 'Vendor2', '456', '789', '012', 'Electrical', 'Vendor2', '2023-01-02', 2),
    ('HSI', 10, '53c', 150.00, 3, '789-GHI', 'Sample Note 3', 15.00, 'Vendor3', '789', '012', '345', 'Electrical', 'Vendor3', '2023-01-03', 3),
    ('Windscreen', 10, '54b', 300.00, 3, '012-JKL', 'Sample Note 4', 25.00, 'Vendor4', '012', '345', '678', 'Electrical', 'Vendor4', '2023-01-04', 4),
    ('Battery', 100, '100a', 20.00, 3, '123-ABC', 'Sample Note 5', 2.00, 'Vendor1', '123', '456', '789', 'Electrical', 'Vendor1', '2023-01-05', 1),
    ('Bandaids', 100, '101b', 5.00, 3, '456-DEF', 'Sample Note 6', 1.00, 'Vendor2', '456', '789', '012', 'Hydraulic', 'Vendor2', '2023-01-06', 2),
    ('Screws', 100, '102c', 10.00, 3, '789-GHI', 'Sample Note 7', 1.50, 'Vendor3', '789', '012', '345', 'Hydraulic', 'Vendor3', '2023-01-07', 3),
    ('Tire', 50, '1d', 400.00, 3, '012-JKL', 'Sample Note 8', 40.00, 'Vendor4', '012', '345', '678', 'Hydraulic', 'Vendor4', '2023-01-08', 4),
    ('Landing Gear', 50, '2a', 1000.00, 3, '123-ABC', 'Sample Note 9', 100.00, 'Vendor1', '123', '456', '789', 'Hydraulic', 'Vendor1', '2023-01-09', 1),
    ('Aircraft Shell', 50, '3d', 5000.00, 3, '456-DEF', 'Sample Note 10', 500.00, 'Vendor2', '456', '789', '012', 'Hydraulic', 'Vendor2', '2023-01-10', 2);


-- Insert Inventory_Audit
INSERT INTO Inventory_Audit (stock_number, date, type)
VALUES
    (1, '2023-01-09', 'Wall to Wall');

-- Insert Maintenance_Schedule
INSERT INTO Maintenance_Schedule (simulator_id, next_maintenance_date)
VALUES
    (1, DATE_ADD(CURDATE(), INTERVAL 1 WEEK));

-- Insert Preflight_Schedule
INSERT INTO PrefWrite_Up_Templateslight_Schedule (simulator_id, preflight_date)
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
    (1, 1, '2023-01-01', '2023-01-02', 1.00, 'Initial work order', 'Work order completed', 'Part1', '2023-01-02', 2, 1, 'maintenance', 'No additional notes', 1.00, 'AWM'),
    (2, 2, '2023-01-03', '2023-01-04', 3.00, 'Reported issue with subsystem', 'Subsystem repaired', 'Part2 added', '2023-01-04', 1, 3, 'instructor2', 'Subsystem repaired', 3.00, 'AWM'),
    (3, 3, '2023-01-05', '2023-01-06', 4.00, 'Simulator failed preflight check', 'Issue fixed', 'Part3 removed', '2023-01-06', 2, 1, 'instructor3', 'Simulator passed preflight check after fix', 4.00, 'AWE'),
    (4, 4, '2023-01-07', '2023-01-08', 1.50, 'Routine maintenance', 'Maintenance completed', 'No parts added or removed', '2023-01-08', 2, 1, 'instructor4', 'No additional notes', 1.50, 'AWM');

-- Insert WorkOrder_Missions
INSERT INTO WorkOrder_Missions (jcn, mission_id)
VALUES
    (1, 1);

-- Insert WorkOrder_Parts
INSERT INTO WorkOrder_Parts (jcn, part_id, quantity)
VALUES
    (1, 1, 1);