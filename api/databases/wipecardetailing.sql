-- MySQL dump 10.14  Distrib 5.5.65-MariaDB, for Linux (x86_64)
--
-- Host: 192.168.178.25    Database: Wipecardetailing
-- ------------------------------------------------------
-- Server version	8.0.21

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `FormSubmits`
--

DROP TABLE IF EXISTS `FormSubmits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `FormSubmits` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `FormName` varchar(45) NOT NULL,
  `CompanyName` varchar(45) DEFAULT NULL,
  `CustomerName` varchar(45) DEFAULT NULL,
  `Email` varchar(45) DEFAULT NULL,
  `PhoneNr` varchar(45) DEFAULT NULL,
  `Street` varchar(45) DEFAULT NULL,
  `HouseNr` varchar(45) DEFAULT NULL,
  `Postcode` varchar(45) DEFAULT NULL,
  `City` varchar(45) DEFAULT NULL,
  `Message` longtext,
  `Submitted` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Status` enum('SUCCESS','ERROR','PENDING') NOT NULL DEFAULT 'PENDING',
  PRIMARY KEY (`Id`),
  KEY `formname_idx` (`Status`),
  KEY `status_idx` (`Status`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Multimedia`
--

DROP TABLE IF EXISTS `Multimedia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Multimedia` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Title` varchar(45) NOT NULL,
  `Type` enum('Image','Video','SocialMediaLink') NOT NULL,
  `AddedByUser` smallint unsigned NOT NULL,
  `Added` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `SocialMediaLink` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `SocialMediaName` varchar(45) DEFAULT NULL,
  `file` varchar(254) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `title_type` (`Title`,`Type`),
  UNIQUE KEY `link_uq` (`SocialMediaLink`),
  KEY `added_idx` (`Added`),
  KEY `socialmedia_idx` (`SocialMediaName`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-09-22 20:06:35
