USE flight_simulator_db;

CREATE TABLE Users (
    user_id INT AUTO_INCREMENT,
    username VARCHAR(255),
    password VARCHAR(255),
    is_manager BOOLEAN DEFAULT FALSE,
    is_mantenance BOOLEAN DEFAULT FALSE,
    is_logistics BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (user_id)
);

CREATE TABLE Simulators (
    simulator_id INT AUTO_INCREMENT,
    model VARCHAR(255),
    date_installed DATE,
    last_maintenance_date DATE,
    status VARCHAR(255),
    PRIMARY KEY (simulator_id)
);

CREATE TABLE Subsystems (
    subsystem_id INT AUTO_INCREMENT,
    name VARCHAR(255),
    PRIMARY KEY (subsystem_id)
);

CREATE TABLE Parts (
    part_id INT AUTO_INCREMENT,
    name VARCHAR(255),
    cost FLOAT,
    stock_number INT,
    PRIMARY KEY (part_id)
);

CREATE TABLE Logistics (
    stock_number INT AUTO_INCREMENT,
    item_name VARCHAR(255),
    minimum_stock_number INT,
    stock_location VARCHAR(255),
    cost_per_item FLOAT,
    entered_by INT,
    unique_identifier VARCHAR(255),
    notes TEXT,
    repair_cost FLOAT,
    vendor VARCHAR(255),
    original_part_number VARCHAR(255),
    serial_number VARCHAR(255),
    national_stock_number VARCHAR(255),
    location_type ENUM('Electrical', 'Hydraulic'),
    preferred_repair_vendor VARCHAR(255),
    due_date DATE,
    priority INT,
    PRIMARY KEY (stock_number),
    FOREIGN KEY (entered_by) REFERENCES Users(user_id)
);

CREATE TABLE Inventory_Audit (
    audit_id INT AUTO_INCREMENT,
    stock_number INT,
    date DATE,
    type ENUM('Wall to Wall', 'Cycle', 'Spot'),
    PRIMARY KEY (audit_id),
    FOREIGN KEY (stock_number) REFERENCES Logistics(stock_number)
);

CREATE TABLE Missions (
    mission_id INT AUTO_INCREMENT,
    name VARCHAR(255),
    PRIMARY KEY (mission_id)
);

CREATE TABLE Maintenance_Schedule (
    schedule_id INT AUTO_INCREMENT,
    simulator_id INT,
    next_maintenance_date DATE,
    PRIMARY KEY (schedule_id),
    FOREIGN KEY (simulator_id) REFERENCES Simulators(simulator_id)
);

CREATE TABLE Preflight_Schedule (
    schedule_id INT AUTO_INCREMENT,
    simulator_id INT,
    preflight_date DATE,
    PRIMARY KEY (schedule_id),
    FOREIGN KEY (simulator_id) REFERENCES Simulators(simulator_id)
);

CREATE TABLE Write_Up_Templates (
    template_id INT AUTO_INCREMENT,
    description TEXT,
    PRIMARY KEY (template_id)
);

CREATE TABLE Simulator_Subsystems (
    id INT AUTO_INCREMENT,
    simulator_id INT,
    subsystem_id INT,
    status VARCHAR(255),
    PRIMARY KEY (id),
    FOREIGN KEY (simulator_id) REFERENCES Simulators(simulator_id),
    FOREIGN KEY (subsystem_id) REFERENCES Subsystems(subsystem_id)
);

CREATE TABLE WorkOrders (
    jcn INT AUTO_INCREMENT,
    simulator_id INT,
    subsystem_id INT,
    creation_date DATE,
    update_date DATE,
    total_time FLOAT,
    creation_reason TEXT,
    correction_note TEXT,
    parts_added_removed TEXT,
    sign_off_date DATE,
    signed_off_by INT,
    priority INT,
    reported_by_name VARCHAR(255),
    notes TEXT,
    hours FLOAT,
    disposition ENUM('AWM', 'AWT', 'AWE') DEFAULT 'AWM',
    PRIMARY KEY (jcn),
    FOREIGN KEY (simulator_id) REFERENCES Simulators(simulator_id),
    FOREIGN KEY (subsystem_id) REFERENCES Simulator_Subsystems(id),
    FOREIGN KEY (signed_off_by) REFERENCES Users(user_id)
);

CREATE TABLE WorkOrder_Missions (
    id INT AUTO_INCREMENT,
    jcn INT,
    mission_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (jcn) REFERENCES WorkOrders(jcn),
    FOREIGN KEY (mission_id) REFERENCES Missions(mission_id)
);

CREATE TABLE WorkOrder_Parts (
    id INT AUTO_INCREMENT,
    jcn INT,
    part_id INT,
    quantity INT,
    PRIMARY KEY (id),
    FOREIGN KEY (jcn) REFERENCES WorkOrders(jcn),
    FOREIGN KEY (part_id) REFERENCES Parts(part_id)
);


