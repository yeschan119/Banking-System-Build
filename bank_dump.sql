-- MySQL dump 10.13  Distrib 8.0.27, for macos11.6 (arm64)
--
-- Host: localhost    Database: HBank
-- ------------------------------------------------------
-- Server version	8.0.27

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Account`
--

DROP TABLE IF EXISTS `Account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Account` (
  `AccNum` int NOT NULL,
  `Balance` int DEFAULT '1',
  `Ussn` int DEFAULT NULL,
  `PassWord` int DEFAULT '1234',
  PRIMARY KEY (`AccNum`),
  KEY `FK` (`Ussn`),
  CONSTRAINT `FK` FOREIGN KEY (`Ussn`) REFERENCES `User` (`SSN`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Account`
--

LOCK TABLES `Account` WRITE;
/*!40000 ALTER TABLE `Account` DISABLE KEYS */;
INSERT INTO `Account` VALUES (1212,50000,7890,1234),(1232,88000,202100,1234),(3454,190000,890890,1234),(6787,15000,34567,1234),(8989,11000,456456,1234),(9090,15000,8899,1234),(123123,100000,1234,2345),(222333,100000,34567,1109),(404040,140000,456456,1234);
/*!40000 ALTER TABLE `Account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Admin`
--

DROP TABLE IF EXISTS `Admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Admin` (
  `Admin_ID` varchar(30) NOT NULL,
  `PassWord` int DEFAULT '1234',
  PRIMARY KEY (`Admin_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Admin`
--

LOCK TABLES `Admin` WRITE;
/*!40000 ALTER TABLE `Admin` DISABLE KEYS */;
INSERT INTO `Admin` VALUES ('abc@naver.com',1234),('eungchan@hanyang.com',5097),('hanyang@abc.com',1234),('test@test.com',1234);
/*!40000 ALTER TABLE `Admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Log`
--

DROP TABLE IF EXISTS `Log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Log` (
  `LogID` int NOT NULL AUTO_INCREMENT,
  `Account` int DEFAULT NULL,
  `Name` varchar(20) DEFAULT NULL,
  `Withdraw` int DEFAULT '0',
  `Deposit` int DEFAULT '0',
  `LogDate` char(10) NOT NULL,
  PRIMARY KEY (`LogID`),
  KEY `LFK` (`Account`),
  KEY `LFK2` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Log`
--

LOCK TABLES `Log` WRITE;
/*!40000 ALTER TABLE `Log` DISABLE KEYS */;
INSERT INTO `Log` VALUES (2,222333,'Henry Kim',50000,0,'2021-11-27'),(3,3334444,'eungchan Kang',100000,0,'2021-11-27'),(4,5559999,'eungchan kang',0,50000,'2021-11-27'),(5,505050,'eungchan kang',50000,0,'2021-11-27'),(6,9876500,'beranar berber',0,9000,'2021-11-27'),(7,123321,'cosmos kim',0,100000,'2021-11-28'),(8,123321,'cosmos kim',0,500000,'2021-11-28'),(9,123321,'cosmos kim',200000,0,'2021-11-28'),(10,404040,'Jack Black',10000,0,'2021-12-02'),(11,404040,'Jack Black',0,100000,'2021-12-02'),(12,102804,'hanyang kim',0,5000,'2021-12-02'),(13,5559999,'eungchan kang',50000,0,'2021-12-02'),(14,9090,'Miffy Kang',0,5000,'2021-12-02'),(15,5559999,'eungchan kang',20000,0,'2021-12-02'),(16,12321,'Hong kildong',0,60000,'2021-12-03'),(17,1232,'beranar berber',2000,0,'2021-12-03'),(18,1232,'beranar berber',2000,0,'2021-12-03'),(19,1232,'beranar berber',0,2000,'2021-12-03'),(21,1212,'hanyang kim',0,50000,'2021-12-03'),(22,1212,'hanyang kim',2000,0,'2021-12-03'),(23,6787,'Henry Kim',0,10000,'2021-12-03'),(24,123123,'bobby Kim',0,90000,'2021-12-03');
/*!40000 ALTER TABLE `Log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `User` (
  `SSN` int NOT NULL,
  `Lname` varchar(10) NOT NULL,
  `Fname` varchar(10) NOT NULL,
  `Bdate` date NOT NULL,
  `NickName` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`SSN`),
  UNIQUE KEY `NickName` (`NickName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
INSERT INTO `User` VALUES (1122,'mola','kang','1991-10-10','nick0'),(1234,'bobby','Kim','1989-11-09','chan'),(7890,'hanyang','kim','1939-01-01','nick1'),(8899,'Miffy','Kang','2000-02-02','nick2'),(34567,'Henry','Kim','1990-10-05','nick3'),(202100,'beranar','berber','1995-01-01','nick4'),(456456,'Jack','Black','1960-05-05','nick5'),(890890,'cosmos','kim','1995-01-19','nick6');
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-12-03 14:27:05
