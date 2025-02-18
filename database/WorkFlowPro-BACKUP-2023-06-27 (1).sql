-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: flight_simulator_db
-- ------------------------------------------------------
-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `inventory_audit`
--

DROP TABLE IF EXISTS `inventory_audit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_audit` (
  `audit_id` int NOT NULL AUTO_INCREMENT,
  `stock_number` int DEFAULT NULL,
  `date` date DEFAULT NULL,
  `type` enum('Wall to Wall','Cycle','Spot') DEFAULT NULL,
  PRIMARY KEY (`audit_id`),
  KEY `stock_number` (`stock_number`),
  CONSTRAINT `Inventory_Audit_ibfk_1` FOREIGN KEY (`stock_number`) REFERENCES `logistics` (`stock_number`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_audit`
--

LOCK TABLES `inventory_audit` WRITE;
/*!40000 ALTER TABLE `inventory_audit` DISABLE KEYS */;
/*!40000 ALTER TABLE `inventory_audit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logistics`
--

DROP TABLE IF EXISTS `logistics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logistics` (
  `stock_number` int NOT NULL AUTO_INCREMENT,
  `item_name` varchar(255) DEFAULT NULL,
  `minimum_stock_number` int DEFAULT NULL,
  `stock_location` varchar(255) DEFAULT NULL,
  `cost_per_item` float DEFAULT NULL,
  `entered_by` int DEFAULT NULL,
  `unique_identifier` varchar(255) DEFAULT NULL,
  `notes` text,
  `repair_cost` float DEFAULT NULL,
  `vendor` varchar(255) DEFAULT NULL,
  `original_part_number` varchar(255) DEFAULT NULL,
  `serial_number` varchar(255) DEFAULT NULL,
  `national_stock_number` varchar(255) DEFAULT NULL,
  `location_type` enum('Electrical','Hydraulic') DEFAULT NULL,
  `preferred_repair_vendor` varchar(255) DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `priority` int DEFAULT NULL,
  `stock_on_hand` int DEFAULT NULL,
  PRIMARY KEY (`stock_number`),
  KEY `entered_by` (`entered_by`),
  CONSTRAINT `Logistics_ibfk_1` FOREIGN KEY (`entered_by`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logistics`
--

LOCK TABLES `logistics` WRITE;
/*!40000 ALTER TABLE `logistics` DISABLE KEYS */;
INSERT INTO `logistics` VALUES (11,'ADI',10,'51c',200,3,'123-ABC','Sample Note 1',20,'Vendor1','1','456','789','Electrical','Vendor1','2023-01-01',1,30),(12,'MFD',10,'55a',250,3,'456-DEF','Sample Note 2',30,'Vendor2','2','789','012','Electrical','Vendor2','2023-01-02',2,20),(13,'HSI',10,'53c',150,3,'789-GHI','Sample Note 3',15,'Vendor3','3','012','345','Electrical','Vendor3','2023-01-03',3,50),(14,'Windscreen',10,'54b',300,3,'012-JKL','Sample Note 4',25,'Vendor4','4','345','678','Electrical','Vendor4','2023-01-04',4,30),(15,'Battery',100,'100a',20,3,'123-ABC','Sample Note 5',2,'Vendor1','5','456','789','Electrical','Vendor1','2023-01-05',1,50),(16,'Bandaids',100,'101b',5,3,'456-DEF','Sample Note 6',1,'Vendor2','6','789','012','Hydraulic','Vendor2','2023-01-06',2,30),(17,'Screws',100,'102c',10,3,'789-GHI','Sample Note 7',1.5,'Vendor3','7','012','345','Hydraulic','Vendor3','2023-01-07',3,1),(18,'Tire',4,'1d',400,3,'012-JKL','Sample Note 8',40,'Vendor4','8','345','678','Hydraulic','Vendor4','2023-01-08',4,5),(19,'Landing Gear',2,'2a',1000,3,'123-ABC','Sample Note 9',100,'Vendor1','9','456','789','Hydraulic','Vendor1','2023-01-09',1,2),(20,'Aircraft Shell',1,'3d',5000,3,'456-DEF','Sample Note 10',500,'Vendor2','10','789','012','Hydraulic','Vendor2','2023-01-10',2,1),(21,'ADI',10,'51c',200,3,'123-ABC','Sample Note 1',20,'Vendor1','123','456','789','Electrical','Vendor1','2023-01-01',1,22),(22,'MFD',10,'55a',250,3,'456-DEF','Sample Note 2',30,'Vendor2','456','789','012','Electrical','Vendor2','2023-01-02',2,22),(23,'HSI',10,'53c',150,3,'789-GHI','Sample Note 3',15,'Vendor3','789','012','345','Electrical','Vendor3','2023-01-03',3,23),(24,'Windscreen',10,'54b',300,3,'012-JKL','Sample Note 4',25,'Vendor4','012','345','678','Electrical','Vendor4','2023-01-04',4,10),(25,'Battery',100,'100a',20,3,'123-ABC','Sample Note 5',2,'Vendor1','123','456','789','Electrical','Vendor1','2023-01-05',1,101),(26,'Bandaids',100,'101b',5,3,'456-DEF','Sample Note 6',1,'Vendor2','456','789','012','Hydraulic','Vendor2','2023-01-06',2,101),(27,'Screws',100,'102c',10,3,'789-GHI','Sample Note 7',1.5,'Vendor3','789','012','345','Hydraulic','Vendor3','2023-01-07',3,101),(28,'Tire',50,'1d',400,3,'012-JKL','Sample Note 8',40,'Vendor4','012','345','678','Hydraulic','Vendor4','2023-01-08',4,50),(29,'Landing Gear',50,'2a',1000,3,'123-ABC','Sample Note 9',100,'Vendor1','123','456','789','Hydraulic','Vendor1','2023-01-09',1,50),(30,'Aircraft Shell',50,'3d',5000,3,'456-DEF','Sample Note 10',500,'Vendor2','456','789','012','Hydraulic','Vendor2','2023-01-10',2,50);
/*!40000 ALTER TABLE `logistics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `maintenance_schedule`
--

DROP TABLE IF EXISTS `maintenance_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maintenance_schedule` (
  `schedule_id` int NOT NULL AUTO_INCREMENT,
  `simulator_id` int DEFAULT NULL,
  `next_maintenance_date` date DEFAULT NULL,
  PRIMARY KEY (`schedule_id`),
  KEY `simulator_id` (`simulator_id`),
  CONSTRAINT `Maintenance_Schedule_ibfk_1` FOREIGN KEY (`simulator_id`) REFERENCES `simulators` (`simulator_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maintenance_schedule`
--

LOCK TABLES `maintenance_schedule` WRITE;
/*!40000 ALTER TABLE `maintenance_schedule` DISABLE KEYS */;
INSERT INTO `maintenance_schedule` VALUES (1,1,'2023-06-19'),(2,2,'2026-06-09');
/*!40000 ALTER TABLE `maintenance_schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `missions`
--

DROP TABLE IF EXISTS `missions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `missions` (
  `mission_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`mission_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `missions`
--

LOCK TABLES `missions` WRITE;
/*!40000 ALTER TABLE `missions` DISABLE KEYS */;
INSERT INTO `missions` VALUES (1,'Training Flight'),(2,'Test Flight'),(3,'Search and Rescue'),(4,'Aerial Survey'),(5,'Medical Evacuation'),(6,'Cargo Transport'),(7,'Aerial Firefighting'),(8,'Passenger Transport'),(9,'Photography and Filming'),(10,'Scientific Research');
/*!40000 ALTER TABLE `missions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parts`
--

DROP TABLE IF EXISTS `parts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parts` (
  `part_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `cost` float DEFAULT NULL,
  `stock_number` int DEFAULT NULL,
  PRIMARY KEY (`part_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parts`
--

LOCK TABLES `parts` WRITE;
/*!40000 ALTER TABLE `parts` DISABLE KEYS */;
INSERT INTO `parts` VALUES (1,'ADI',100,123456),(2,'MFD',200,123457),(3,'ECU',150,123458),(4,'APU',300,123459),(5,'EFIS',250,123460),(6,'FMS',180,123461),(7,'TCAS',220,123462),(8,'RADAR',280,123463),(9,'TCM',190,123464),(10,'EGPWS',230,123465);
/*!40000 ALTER TABLE `parts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `preflight_schedule`
--

DROP TABLE IF EXISTS `preflight_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `preflight_schedule` (
  `schedule_id` int NOT NULL AUTO_INCREMENT,
  `simulator_id` int DEFAULT NULL,
  `preflight_date` date DEFAULT NULL,
  PRIMARY KEY (`schedule_id`),
  KEY `simulator_id` (`simulator_id`),
  CONSTRAINT `Preflight_Schedule_ibfk_1` FOREIGN KEY (`simulator_id`) REFERENCES `simulators` (`simulator_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `preflight_schedule`
--

LOCK TABLES `preflight_schedule` WRITE;
/*!40000 ALTER TABLE `preflight_schedule` DISABLE KEYS */;
INSERT INTO `preflight_schedule` VALUES (1,1,'2023-06-13');
/*!40000 ALTER TABLE `preflight_schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `simulator_subsystems`
--

DROP TABLE IF EXISTS `simulator_subsystems`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `simulator_subsystems` (
  `id` int NOT NULL AUTO_INCREMENT,
  `simulator_id` int DEFAULT NULL,
  `subsystem_id` int DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `simulator_id` (`simulator_id`),
  KEY `subsystem_id` (`subsystem_id`),
  CONSTRAINT `Simulator_Subsystems_ibfk_1` FOREIGN KEY (`simulator_id`) REFERENCES `simulators` (`simulator_id`),
  CONSTRAINT `Simulator_Subsystems_ibfk_2` FOREIGN KEY (`subsystem_id`) REFERENCES `subsystems` (`subsystem_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `simulator_subsystems`
--

LOCK TABLES `simulator_subsystems` WRITE;
/*!40000 ALTER TABLE `simulator_subsystems` DISABLE KEYS */;
INSERT INTO `simulator_subsystems` VALUES (1,1,1,'Active'),(2,1,2,'Active'),(3,2,1,'Active'),(4,2,2,'Active');
/*!40000 ALTER TABLE `simulator_subsystems` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `simulators`
--

DROP TABLE IF EXISTS `simulators`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `simulators` (
  `simulator_id` int NOT NULL AUTO_INCREMENT,
  `model` varchar(255) DEFAULT NULL,
  `date_installed` date DEFAULT NULL,
  `last_maintenance_date` date DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`simulator_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `simulators`
--

LOCK TABLES `simulators` WRITE;
/*!40000 ALTER TABLE `simulators` DISABLE KEYS */;
INSERT INTO `simulators` VALUES (1,'737-300','2023-06-12','2023-06-12','Active'),(2,'747-400','2023-06-12','2023-06-12','Active'),(3,'Cessna 550','2023-01-01','2023-01-01','Active'),(4,'EC1300','2023-02-01','2023-02-01','Active'),(5,'Cessna 337G','2023-03-01','2023-03-01','Active'),(6,'DHC 3','2023-04-01','2023-04-01','Active'),(7,'Falcon 50','2023-05-01','2023-05-01','Active'),(8,'G115','2023-06-01','2023-06-01','Active');
/*!40000 ALTER TABLE `simulators` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subsystems`
--

DROP TABLE IF EXISTS `subsystems`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subsystems` (
  `subsystem_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`subsystem_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subsystems`
--

LOCK TABLES `subsystems` WRITE;
/*!40000 ALTER TABLE `subsystems` DISABLE KEYS */;
INSERT INTO `subsystems` VALUES (1,'Hydraulics'),(2,'Electrical'),(3,'Avionics'),(4,'Fuel Systems'),(5,'Propulsion'),(6,'Air Conditioning'),(7,'Environmental Control Systems'),(8,'Landing Gear'),(9,'Navigation Systems'),(10,'Communication Systems'),(11,'Visual'),(12,'Host'),(13,'Lighting'),(14,'Controls'),(15,'Motion'),(16,'Software(engineering)');
/*!40000 ALTER TABLE `subsystems` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `timeentries`
--

DROP TABLE IF EXISTS `timeentries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `timeentries` (
  `entry_id` int NOT NULL AUTO_INCREMENT,
  `work_order_jcn` bigint DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `date` date DEFAULT NULL,
  `hours_worked` decimal(5,2) DEFAULT NULL,
  `notes` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`entry_id`),
  KEY `work_order_jcn` (`work_order_jcn`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `TimeEntries_ibfk_1` FOREIGN KEY (`work_order_jcn`) REFERENCES `workorders` (`jcn`),
  CONSTRAINT `TimeEntries_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `timeentries`
--

LOCK TABLES `timeentries` WRITE;
/*!40000 ALTER TABLE `timeentries` DISABLE KEYS */;
INSERT INTO `timeentries` VALUES (1,20230315001,3,'2023-01-04',2.00,'Time entry for work order 20230315001'),(2,20230315001,2,'2023-01-04',1.50,'Time entry for work order 20230315001'),(3,20230315002,1,'2023-02-04',3.00,'Time entry for work order 20230315002'),(4,20230315002,2,'2023-02-05',2.00,'Time entry for work order 20230315002'),(5,20230401001,3,'2023-03-05',4.00,'Time entry for work order 20230401001'),(6,20230401001,1,'2023-03-05',1.00,'Time entry for work order 20230401001'),(7,20230409001,2,'2023-04-04',1.50,'Time entry for work order 20230409001'),(8,20230525001,3,'2023-05-05',2.50,'Time entry for work order 20230525001'),(9,20230525002,1,'2023-05-06',3.50,'Time entry for work order 20230525002'),(10,20230613003,2,'2023-06-14',3.75,'Time entry for work order 20230613003'),(11,20230213001,3,'2023-06-15',1.00,'Time entry for work order 20230213001'),(12,20230525003,2,'2023-07-05',4.50,'Time entry for work order 20230525003'),(13,20230613002,3,'2023-08-04',2.75,'Time entry for work order 20230613002'),(14,20230613002,6,'2023-08-04',1.00,'Time entry for work order 20230613002'),(15,20230613001,5,'2023-08-05',1.75,'Time entry for work order 20230613001');
/*!40000 ALTER TABLE `timeentries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `is_manager` tinyint(1) DEFAULT '0',
  `is_mantenance` tinyint(1) DEFAULT '0',
  `is_logistics` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Anderson','1234',1,0,0),(2,'Bailey','1234',0,1,0),(3,'Carter','1234',0,0,1),(4,'Davis','1234',1,0,0),(5,'Edwards','1234',0,1,0),(6,'Foster','1234',0,0,1),(7,'Gray','1234',1,0,0),(8,'Hughes','1234',0,1,0),(9,'Jenkins','1234',0,0,1),(10,'King','1234',1,0,0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workorder_missions`
--

DROP TABLE IF EXISTS `workorder_missions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workorder_missions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `jcn` int DEFAULT NULL,
  `mission_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `mission_id` (`mission_id`),
  CONSTRAINT `WorkOrder_Missions_ibfk_2` FOREIGN KEY (`mission_id`) REFERENCES `missions` (`mission_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workorder_missions`
--

LOCK TABLES `workorder_missions` WRITE;
/*!40000 ALTER TABLE `workorder_missions` DISABLE KEYS */;
/*!40000 ALTER TABLE `workorder_missions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workorder_parts`
--

DROP TABLE IF EXISTS `workorder_parts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workorder_parts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `jcn` bigint DEFAULT NULL,
  `part_id` int DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `action` enum('added','removed') NOT NULL,
  `action_date` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `jcn` (`jcn`),
  KEY `part_id` (`part_id`),
  CONSTRAINT `WorkOrder_Parts_ibfk_2` FOREIGN KEY (`part_id`) REFERENCES `parts` (`part_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workorder_parts`
--

LOCK TABLES `workorder_parts` WRITE;
/*!40000 ALTER TABLE `workorder_parts` DISABLE KEYS */;
INSERT INTO `workorder_parts` VALUES (1,20230613003,1,10,'added','2023-06-23'),(2,20230525003,2,5,'added','2023-06-23'),(3,20230315001,3,8,'added','2023-06-22');
/*!40000 ALTER TABLE `workorder_parts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workorders`
--

DROP TABLE IF EXISTS `workorders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workorders` (
  `jcn` bigint NOT NULL,
  `simulator_id` int DEFAULT NULL,
  `subsystem_id` int DEFAULT NULL,
  `creation_date` date DEFAULT NULL,
  `update_date` date DEFAULT NULL,
  `total_time` float DEFAULT NULL,
  `creation_reason` text,
  `correction_note` text,
  `parts_added_removed` text,
  `sign_off_date` date DEFAULT NULL,
  `signed_off_by` int DEFAULT NULL,
  `priority` int DEFAULT NULL,
  `reported_by_name` varchar(255) DEFAULT NULL,
  `notes` text,
  `hours` float DEFAULT NULL,
  `disposition` enum('AWM','AWT','AWE') DEFAULT 'AWM',
  PRIMARY KEY (`jcn`),
  KEY `simulator_id` (`simulator_id`),
  KEY `subsystem_id` (`subsystem_id`),
  KEY `signed_off_by` (`signed_off_by`),
  CONSTRAINT `WorkOrders_ibfk_1` FOREIGN KEY (`simulator_id`) REFERENCES `simulators` (`simulator_id`),
  CONSTRAINT `WorkOrders_ibfk_2` FOREIGN KEY (`subsystem_id`) REFERENCES `simulator_subsystems` (`id`),
  CONSTRAINT `WorkOrders_ibfk_3` FOREIGN KEY (`signed_off_by`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workorders`
--

LOCK TABLES `workorders` WRITE;
/*!40000 ALTER TABLE `workorders` DISABLE KEYS */;
INSERT INTO `workorders` VALUES (20230213001,1,1,'2023-06-23','2023-06-12',1,'Initial work order','Test was completed','Part1','2023-06-12',2,3,'bob','note 1',1,'AWM'),(20230315001,2,2,'2023-01-01','2023-01-02',2,'Scheduled work order','Work order completed','Part2','2023-01-03',3,2,'cory','No additional notes',2,'AWM'),(20230315002,3,3,'2023-02-01','2023-02-02',3,'Emergency work order','Work order completed','Part3','2023-02-03',4,1,'daisy','replaced emergency',3,'AWT'),(20230401001,4,4,'2023-03-01','2023-03-02',4,'Regular work order','Work order completed','Part4','2023-03-03',5,3,'emma','No additional notes',4,'AWE'),(20230409001,5,1,'2023-04-01','2023-04-02',1.5,'Unscheduled work order','Work order completed','Part5','2023-04-03',6,2,'frank','No additional notes',1.5,'AWM'),(20230525001,6,2,'2023-05-01','2023-05-02',2.5,'Scheduled work order','Work order completed','Part6','2023-05-03',2,3,'gene','No additional notes',2.5,'AWT'),(20230525002,1,3,'2023-06-01','2023-06-02',3.5,'Emergency work order','Work order completed','Part7','2023-06-03',3,1,'john','No additional notes',3.5,'AWE'),(20230525003,2,4,'2023-07-01','2023-07-02',4.5,'Regular work order','Work order completed','Part8','2023-07-03',4,2,'kyle','No additional notes',4.5,'AWM'),(20230613001,3,1,'2023-08-01','2023-08-02',1.75,'Unscheduled work order','Work order completed','Part9','2023-08-03',5,3,'lucy','No additional notes',1.75,'AWT'),(20230613002,4,2,'2023-08-01','2023-08-02',2.75,'Scheduled work order','Work order completed','Part10','2023-08-03',6,3,'jean','No additional notes',2.75,'AWE'),(20230613003,5,3,'2023-06-12','2023-06-12',3.75,'Emergency work order','Work order completed','Part11','2023-10-03',2,2,'daisy','No additional notes',3.75,'AWM'),(20230625001,7,2,'2023-06-25',NULL,NULL,'Removed Panel','Montly battery test.',NULL,NULL,NULL,3,NULL,NULL,NULL,'AWM'),(20230625002,1,1,'2023-06-25',NULL,NULL,'sdfs','sdfsd',NULL,NULL,NULL,3,NULL,NULL,NULL,'AWM'),(20230627001,1,1,'2023-06-27',NULL,NULL,'IOS is slow to respond','IOS has low memor',NULL,NULL,NULL,3,'emma',NULL,NULL,'AWM'),(20230627002,1,1,'2023-06-27',NULL,NULL,'During flight sim locked up','Hard drive failed',NULL,NULL,NULL,3,'emma',NULL,NULL,'AWM'),(20230627003,2,3,'2023-06-27',NULL,NULL,'Preflight required','Daily preflight required by SOP.',NULL,NULL,NULL,3,'emma',NULL,NULL,'AWM');
/*!40000 ALTER TABLE `workorders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `write_up_templates`
--

DROP TABLE IF EXISTS `write_up_templates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `write_up_templates` (
  `template_id` int NOT NULL AUTO_INCREMENT,
  `description` text,
  PRIMARY KEY (`template_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `write_up_templates`
--

LOCK TABLES `write_up_templates` WRITE;
/*!40000 ALTER TABLE `write_up_templates` DISABLE KEYS */;
INSERT INTO `write_up_templates` VALUES (1,'Template1'),(2,'Template2');
/*!40000 ALTER TABLE `write_up_templates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'flight_simulator_db'
--

--
-- Dumping routines for database 'flight_simulator_db'
--
/*!50003 DROP PROCEDURE IF EXISTS `GetHoursWorkedPerPerson` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`sherwood`@`localhost` PROCEDURE `GetHoursWorkedPerPerson`()
BEGIN
    SELECT u.username, SUM(te.hours_worked) AS total_hours
    FROM Users u
    JOIN TimeEntries te ON u.user_id = te.user_id
    WHERE te.date >= CURDATE() - INTERVAL 7 DAY
    GROUP BY u.user_id, u.username;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetInventoryData` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`sherwood`@`localhost` PROCEDURE `GetInventoryData`()
BEGIN
    SELECT l.stock_on_hand, l.item_name, l.minimum_stock_number, l.stock_location, l.cost_per_item, u.username
    FROM Logistics l
    JOIN Users u ON l.entered_by = u.user_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetTechSummary` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`sherwood`@`localhost` PROCEDURE `GetTechSummary`()
BEGIN
    SELECT 
        Users.username as tech,
        SUM(WorkOrders.hours) as total_hours,
        SUM(Logistics.cost_per_item * WorkOrder_Parts.quantity) as total_cost
    FROM 
        WorkOrder_Parts
    JOIN
        WorkOrders ON WorkOrder_Parts.jcn = WorkOrders.jcn
    JOIN
        Logistics ON WorkOrder_Parts.part_id = Logistics.original_part_number
    JOIN
        Users ON WorkOrders.signed_off_by = Users.user_id
    WHERE 
        WorkOrder_Parts.action_date >= CURDATE() - INTERVAL 7 DAY
        AND WorkOrder_Parts.action = 'added'
    GROUP BY 
        Users.username;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetWorkOrderCountPerDay` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`sherwood`@`localhost` PROCEDURE `GetWorkOrderCountPerDay`()
BEGIN
    SELECT DATE(creation_date) AS order_date, COUNT(*) AS order_count
    FROM WorkOrders
    WHERE creation_date >= CURDATE() - INTERVAL 7 DAY
    GROUP BY order_date
    ORDER BY order_date;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `show_parts_data` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`sherwood`@`localhost` PROCEDURE `show_parts_data`()
BEGIN
    SELECT item_name, cost_per_item, due_date, priority 
    FROM Logistics 
    ORDER BY due_date DESC 
    LIMIT 5;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-27 13:57:31
