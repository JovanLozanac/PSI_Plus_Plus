-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: psi_db_model
-- ------------------------------------------------------
-- Server version	8.0.44

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
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `KorID` int NOT NULL,
  PRIMARY KEY (`KorID`),
  CONSTRAINT `admin_KorID_ca16d9d0_fk_korisnik_KorID` FOREIGN KEY (`KorID`) REFERENCES `korisnik` (`KorID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1);
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `asistent`
--

DROP TABLE IF EXISTS `asistent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `asistent` (
  `KorID` int NOT NULL,
  PRIMARY KEY (`KorID`),
  CONSTRAINT `asistent_KorID_f18dc861_fk_korisnik_KorID` FOREIGN KEY (`KorID`) REFERENCES `korisnik` (`KorID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `asistent`
--

LOCK TABLES `asistent` WRITE;
/*!40000 ALTER TABLE `asistent` DISABLE KEYS */;
INSERT INTO `asistent` VALUES (2);
/*!40000 ALTER TABLE `asistent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add korisnik',3,'add_korisnik'),(2,'Can change korisnik',3,'change_korisnik'),(3,'Can delete korisnik',3,'delete_korisnik'),(4,'Can view korisnik',3,'view_korisnik'),(5,'Can add tim',9,'add_tim'),(6,'Can change tim',9,'change_tim'),(7,'Can delete tim',9,'delete_tim'),(8,'Can view tim',9,'view_tim'),(9,'Can add admin',1,'add_admin'),(10,'Can change admin',1,'change_admin'),(11,'Can delete admin',1,'delete_admin'),(12,'Can view admin',1,'view_admin'),(13,'Can add asistent',2,'add_asistent'),(14,'Can change asistent',2,'change_asistent'),(15,'Can delete asistent',2,'delete_asistent'),(16,'Can view asistent',2,'view_asistent'),(17,'Can add student',8,'add_student'),(18,'Can change student',8,'change_student'),(19,'Can delete student',8,'delete_student'),(20,'Can view student',8,'view_student'),(21,'Can add obavestenje',4,'add_obavestenje'),(22,'Can change obavestenje',4,'change_obavestenje'),(23,'Can delete obavestenje',4,'delete_obavestenje'),(24,'Can view obavestenje',4,'view_obavestenje'),(25,'Can add primio',6,'add_primio'),(26,'Can change primio',6,'change_primio'),(27,'Can delete primio',6,'delete_primio'),(28,'Can view primio',6,'view_primio'),(29,'Can add projekat',7,'add_projekat'),(30,'Can change projekat',7,'change_projekat'),(31,'Can delete projekat',7,'delete_projekat'),(32,'Can view projekat',7,'view_projekat'),(33,'Can add zadatak',11,'add_zadatak'),(34,'Can change zadatak',11,'change_zadatak'),(35,'Can delete zadatak',11,'delete_zadatak'),(36,'Can view zadatak',11,'view_zadatak'),(37,'Can add ocena',5,'add_ocena'),(38,'Can change ocena',5,'change_ocena'),(39,'Can delete ocena',5,'delete_ocena'),(40,'Can view ocena',5,'view_ocena'),(41,'Can add zahteva',12,'add_zahteva'),(42,'Can change zahteva',12,'change_zahteva'),(43,'Can delete zahteva',12,'delete_zahteva'),(44,'Can view zahteva',12,'view_zahteva'),(45,'Can add u timu',10,'add_utimu'),(46,'Can change u timu',10,'change_utimu'),(47,'Can delete u timu',10,'delete_utimu'),(48,'Can view u timu',10,'view_utimu'),(49,'Can add log entry',13,'add_logentry'),(50,'Can change log entry',13,'change_logentry'),(51,'Can delete log entry',13,'delete_logentry'),(52,'Can view log entry',13,'view_logentry'),(53,'Can add permission',15,'add_permission'),(54,'Can change permission',15,'change_permission'),(55,'Can delete permission',15,'delete_permission'),(56,'Can view permission',15,'view_permission'),(57,'Can add group',14,'add_group'),(58,'Can change group',14,'change_group'),(59,'Can delete group',14,'delete_group'),(60,'Can view group',14,'view_group'),(61,'Can add content type',16,'add_contenttype'),(62,'Can change content type',16,'change_contenttype'),(63,'Can delete content type',16,'delete_contenttype'),(64,'Can view content type',16,'view_contenttype'),(65,'Can add session',17,'add_session'),(66,'Can change session',17,'change_session'),(67,'Can delete session',17,'delete_session'),(68,'Can view session',17,'view_session');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_korisnik_KorID` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_korisnik_KorID` FOREIGN KEY (`user_id`) REFERENCES `korisnik` (`KorID`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2026-07-09 10:41:49.013200','2','  (ID=2)',1,'[{\"added\": {}}]',3,1),(2,'2026-07-09 10:42:25.372948','2','Asistent object (2)',1,'[{\"added\": {}}]',2,1),(3,'2026-07-09 10:42:47.639769','3','  (ID=3)',1,'[{\"added\": {}}]',3,1),(4,'2026-07-09 10:42:59.221826','3','Pera Peric (ID=3)',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\"]}}]',3,1),(5,'2026-07-09 10:43:18.025157','2','Asistent Asistentic (ID=2)',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\"]}}]',3,1),(6,'2026-07-09 10:43:53.511248','3','2022/0182',1,'[{\"added\": {}}]',8,1),(7,'2026-07-09 10:54:18.048011','1','Admin object (1)',1,'[{\"added\": {}}]',1,1),(8,'2026-07-09 11:01:48.741701','4','  (ID=4)',1,'[{\"added\": {}}]',3,1),(9,'2026-07-09 11:01:58.852166','4','Milos Milosevic (ID=4)',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\"]}}]',3,1),(10,'2026-07-09 11:02:10.017962','4','2019/0234',1,'[{\"added\": {}}]',8,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (13,'admin','logentry'),(1,'app','admin'),(2,'app','asistent'),(3,'app','korisnik'),(4,'app','obavestenje'),(5,'app','ocena'),(6,'app','primio'),(7,'app','projekat'),(8,'app','student'),(9,'app','tim'),(10,'app','utimu'),(11,'app','zadatak'),(12,'app','zahteva'),(14,'auth','group'),(15,'auth','permission'),(16,'contenttypes','contenttype'),(17,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-07-09 10:00:05.538820'),(2,'contenttypes','0002_remove_content_type_name','2026-07-09 10:00:05.621986'),(3,'auth','0001_initial','2026-07-09 10:00:05.833982'),(4,'auth','0002_alter_permission_name_max_length','2026-07-09 10:00:05.885785'),(5,'auth','0003_alter_user_email_max_length','2026-07-09 10:00:05.890001'),(6,'auth','0004_alter_user_username_opts','2026-07-09 10:00:05.894033'),(7,'auth','0005_alter_user_last_login_null','2026-07-09 10:00:05.897896'),(8,'auth','0006_require_contenttypes_0002','2026-07-09 10:00:05.899811'),(9,'auth','0007_alter_validators_add_error_messages','2026-07-09 10:00:05.903499'),(10,'auth','0008_alter_user_username_max_length','2026-07-09 10:00:05.907501'),(11,'auth','0009_alter_user_last_name_max_length','2026-07-09 10:00:05.913345'),(12,'auth','0010_alter_group_name_max_length','2026-07-09 10:00:05.924328'),(13,'auth','0011_update_proxy_permissions','2026-07-09 10:00:05.929159'),(14,'auth','0012_alter_user_first_name_max_length','2026-07-09 10:00:05.933265'),(15,'app','0001_initial','2026-07-09 10:00:06.973071'),(16,'admin','0001_initial','2026-07-09 10:00:07.088336'),(17,'admin','0002_logentry_remove_auto_add','2026-07-09 10:00:07.094854'),(18,'admin','0003_logentry_add_action_flag_choices','2026-07-09 10:00:07.102185'),(19,'app','0002_remove_projekat_fajl_projekat_folder','2026-07-09 10:00:07.197427'),(20,'sessions','0001_initial','2026-07-09 10:00:07.219423'),(21,'app','0003_primio_procitano_alter_student_indeks','2026-07-12 19:27:41.505523'),(22,'app','0004_remove_ocena_prid_ocena_timid','2026-07-13 09:26:31.465842');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('dm71gwqq26nyy1frz57dtzb1cf5r5njo','.eJxVjMsOwiAQAP9lz4aU8twevfsNBHZBqoYmpT0Z_9006UGvM5N5Q4j7VsPe8xpmhglGuPyyFOmZ2yH4Edt9EbS0bZ2TOBJx2i5uC-fX9Wz_BjX2ChMo5GS0k2pUniQzSqOQvVHsWDMhWcexYDY2FdRUZJa2eGWJPQ2Ds_D5AtxjN_Q:1wjJXs:O2mFn8IHnK2o4HWixt5Vq_qRaCkdmURBfikgQTpyA34','2026-07-27 16:30:16.472664');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `korisnik`
--

DROP TABLE IF EXISTS `korisnik`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `korisnik` (
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `KorID` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`KorID`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `korisnik`
--

LOCK TABLES `korisnik` WRITE;
/*!40000 ALTER TABLE `korisnik` DISABLE KEYS */;
INSERT INTO `korisnik` VALUES ('pbkdf2_sha256$1200000$37X7wmKnhFu80Ye7U3LPZz$kV4sgBmQ7Ic/B4wfip/vkXvaWds1H+d7OEi7TKFO3LU=','2026-07-13 15:21:50.718122',1,'admin','','','nekimejl@gmail.com',1,1,'2026-07-09 10:40:40.566017',1),('pbkdf2_sha256$1200000$zcUUPKPa0eUXaG4WjwKg9x$EqIzrg4fUdzW7HHd71x5qv7PbdMtWCVIa7F4txylcms=','2026-07-13 16:30:16.468342',0,'asistent','Asistent','Asistentic','nekimejl@gmail.com',0,1,'2026-07-09 10:41:48.000000',2),('pbkdf2_sha256$1200000$SJW3F6QhcxYZUzOj9jo5Do$IiEHLkvceVMy+qoBnaVWBxpjRswGRFlKA9XONJK+0WM=','2026-07-13 16:12:11.685568',0,'pera','Pera','Peric','nekimejl@gmail.com',0,1,'2026-07-09 10:42:47.000000',3),('pbkdf2_sha256$1200000$7pmUGn4ttOpm6WkoBOlPpc$GRLm34bIWwkC6IEHGVnUjaqaqZUczDWo8bdr9tdbLHo=','2026-07-13 15:49:04.905490',0,'milos','Milos','Milosevic','nekimejl@gmail.com',0,1,'2026-07-09 11:01:48.000000',4),('pbkdf2_sha256$1200000$UcAatHkZBRY8VwCwCjrHaD$TEsDt/1lDQOdSrEGAeTTFckJ4nk8XmC/rSIDlPfp14Q=','2026-07-13 15:42:32.300806',0,'mika','Mika','Mikic','nekimejl@gmail.com',0,1,'2026-07-10 17:54:03.916700',5),('pbkdf2_sha256$1200000$t9AnpOBhDHRuXDeLcYB8Vy$Sqs2Qn+bsr2983BSDYE1N772y+RPimoZhhL6DCww9R0=','2026-07-13 15:43:43.066270',0,'luka','Luka','Lukic','nekimejl@gmail.com',0,1,'2026-07-13 15:22:40.613551',6),('pbkdf2_sha256$1200000$BIRkKKGLmXZmHmntD5ewZQ$8mvI6bIx7NsPbJfK+pogd+X29DnKRVCQaHG6qXVqegA=','2026-07-13 15:44:23.901142',0,'marko','Marko','Markovic','nekimejl@gmail.com',0,1,'2026-07-13 15:24:16.114288',7);
/*!40000 ALTER TABLE `korisnik` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `korisnik_groups`
--

DROP TABLE IF EXISTS `korisnik_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `korisnik_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `korisnik_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `korisnik_groups_korisnik_id_group_id_8c5ba7f0_uniq` (`korisnik_id`,`group_id`),
  KEY `korisnik_groups_group_id_639f924a_fk_auth_group_id` (`group_id`),
  CONSTRAINT `korisnik_groups_group_id_639f924a_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `korisnik_groups_korisnik_id_b99df0b8_fk_korisnik_KorID` FOREIGN KEY (`korisnik_id`) REFERENCES `korisnik` (`KorID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `korisnik_groups`
--

LOCK TABLES `korisnik_groups` WRITE;
/*!40000 ALTER TABLE `korisnik_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `korisnik_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `korisnik_user_permissions`
--

DROP TABLE IF EXISTS `korisnik_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `korisnik_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `korisnik_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `korisnik_user_permission_korisnik_id_permission_i_f0bb31ce_uniq` (`korisnik_id`,`permission_id`),
  KEY `korisnik_user_permis_permission_id_ed48e217_fk_auth_perm` (`permission_id`),
  CONSTRAINT `korisnik_user_permis_permission_id_ed48e217_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `korisnik_user_permissions_korisnik_id_420accdf_fk_korisnik_KorID` FOREIGN KEY (`korisnik_id`) REFERENCES `korisnik` (`KorID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `korisnik_user_permissions`
--

LOCK TABLES `korisnik_user_permissions` WRITE;
/*!40000 ALTER TABLE `korisnik_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `korisnik_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `obavestenje`
--

DROP TABLE IF EXISTS `obavestenje`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `obavestenje` (
  `ObID` int NOT NULL AUTO_INCREMENT,
  `Naslov` varchar(100) NOT NULL,
  `Tekst` varchar(300) NOT NULL,
  `KorID` int DEFAULT NULL,
  PRIMARY KEY (`ObID`),
  KEY `obavestenje_KorID_cdf02638_fk_korisnik_KorID` (`KorID`),
  CONSTRAINT `obavestenje_KorID_cdf02638_fk_korisnik_KorID` FOREIGN KEY (`KorID`) REFERENCES `korisnik` (`KorID`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `obavestenje`
--

LOCK TABLES `obavestenje` WRITE;
/*!40000 ALTER TABLE `obavestenje` DISABLE KEYS */;
INSERT INTO `obavestenje` VALUES (21,'Formiranje timova','Potrevno je da studenti formiraju timove od 2-4 clanova. Do kraja roka timovi moraju imati da imenuju svoj tim, projekat i da osmisle kratak opis projekta. Studenti koji nisu u timu do kraja roka ce se nasumicno rasporediti.',2),(22,'Zahtev za učlanjenje','Student Mika Mikic želi da bude deo vašeg tima.',5),(23,'Zahtev za učlanjenje','Student Luka Lukic želi da bude deo vašeg tima.',6),(24,'Zahtev za učlanjenje','Student Marko Markovic želi da bude deo vašeg tima.',7),(25,'Zahtev je prihvacen','Kapiten tima PSIholozi je prihvatio vaš zahtev za članstvo.',3),(26,'Zahtev je odbijen','Kapiten tima PSIholozi je odbio vaš zahtev za članstvo.',3),(27,'Projektni zadatak','Napraviti word dokument projektnog zadatka i ubaciti ga u repozitorijum.',2),(28,'Srecno!','Dobrodosli na PSI++',2),(29,'Zadatak ocenjen','Vaša ocena je: 95 od 100',2),(30,'SSU dokument i prototip aplikacije','Napraviti SSU dokument za svaki funkcionalni zahtev iz Projektnog zadatka, kao i prototip aplikacije.',2);
/*!40000 ALTER TABLE `obavestenje` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ocena`
--

DROP TABLE IF EXISTS `ocena`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ocena` (
  `OcID` int NOT NULL AUTO_INCREMENT,
  `Bodovi` decimal(4,2) NOT NULL,
  `Komentar` varchar(100) DEFAULT NULL,
  `ZadID` int NOT NULL,
  `KorID` int NOT NULL,
  `TimID` int NOT NULL,
  PRIMARY KEY (`OcID`),
  KEY `ocena_ZadID_2f80727e_fk_zadatak_ZadID` (`ZadID`),
  KEY `ocena_KorID_f2e6077c_fk_asistent_KorID` (`KorID`),
  KEY `ocena_TimID_c6d41c48_fk_tim_TimID` (`TimID`),
  CONSTRAINT `ocena_KorID_f2e6077c_fk_asistent_KorID` FOREIGN KEY (`KorID`) REFERENCES `asistent` (`KorID`),
  CONSTRAINT `ocena_TimID_c6d41c48_fk_tim_TimID` FOREIGN KEY (`TimID`) REFERENCES `tim` (`TimID`),
  CONSTRAINT `ocena_ZadID_2f80727e_fk_zadatak_ZadID` FOREIGN KEY (`ZadID`) REFERENCES `zadatak` (`ZadID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ocena`
--

LOCK TABLES `ocena` WRITE;
/*!40000 ALTER TABLE `ocena` DISABLE KEYS */;
INSERT INTO `ocena` VALUES (2,95.00,'Moglo je bolje...',4,2,3);
/*!40000 ALTER TABLE `ocena` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `primio`
--

DROP TABLE IF EXISTS `primio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `primio` (
  `KorID` int NOT NULL,
  `ObID` int NOT NULL,
  `procitano` tinyint(1) NOT NULL,
  PRIMARY KEY (`KorID`,`ObID`),
  KEY `primio_ObID_efd2ac91_fk_obavestenje_ObID` (`ObID`),
  CONSTRAINT `primio_KorID_37c08cdc_fk_korisnik_KorID` FOREIGN KEY (`KorID`) REFERENCES `korisnik` (`KorID`),
  CONSTRAINT `primio_ObID_efd2ac91_fk_obavestenje_ObID` FOREIGN KEY (`ObID`) REFERENCES `obavestenje` (`ObID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `primio`
--

LOCK TABLES `primio` WRITE;
/*!40000 ALTER TABLE `primio` DISABLE KEYS */;
INSERT INTO `primio` VALUES (1,28,0),(2,28,1),(3,21,1),(3,22,1),(3,24,1),(3,27,1),(3,28,1),(3,29,1),(3,30,0),(4,21,1),(4,23,1),(4,27,0),(4,28,0),(4,30,0),(5,21,1),(5,25,0),(5,27,0),(5,28,0),(5,29,0),(5,30,0),(6,21,0),(6,27,0),(6,28,0),(6,30,0),(7,21,1),(7,26,0),(7,27,0),(7,28,0),(7,30,0);
/*!40000 ALTER TABLE `primio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projekat`
--

DROP TABLE IF EXISTS `projekat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projekat` (
  `PrID` int NOT NULL AUTO_INCREMENT,
  `UpDatum` datetime(6) NOT NULL,
  `TimID` int NOT NULL,
  `Folder` varchar(100) NOT NULL,
  PRIMARY KEY (`PrID`),
  KEY `projekat_TimID_4e360042_fk_tim_TimID` (`TimID`),
  CONSTRAINT `projekat_TimID_4e360042_fk_tim_TimID` FOREIGN KEY (`TimID`) REFERENCES `tim` (`TimID`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projekat`
--

LOCK TABLES `projekat` WRITE;
/*!40000 ALTER TABLE `projekat` DISABLE KEYS */;
INSERT INTO `projekat` VALUES (16,'2026-07-13 15:57:03.616285',3,'projekti/zadatak_4/tim_3'),(17,'2026-07-13 15:57:03.624008',3,'projekti/latest/tim_3');
/*!40000 ALTER TABLE `projekat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student` (
  `KorID` int NOT NULL,
  `JeKapiten` int DEFAULT NULL,
  `Indeks` varchar(9) NOT NULL,
  PRIMARY KEY (`KorID`),
  UNIQUE KEY `Indeks` (`Indeks`),
  CONSTRAINT `student_KorID_c1fb06ba_fk_korisnik_KorID` FOREIGN KEY (`KorID`) REFERENCES `korisnik` (`KorID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES (3,1,'2022/0182'),(4,1,'2019/0234'),(5,0,'2021/0111'),(6,0,'2022/0137'),(7,0,'2020/0379');
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tim`
--

DROP TABLE IF EXISTS `tim`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tim` (
  `TimID` int NOT NULL AUTO_INCREMENT,
  `NazivTima` varchar(45) DEFAULT NULL,
  `ImeProjekta` varchar(100) DEFAULT NULL,
  `OpisProjekta` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`TimID`),
  UNIQUE KEY `NazivTima` (`NazivTima`),
  UNIQUE KEY `ImeProjekta` (`ImeProjekta`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tim`
--

LOCK TABLES `tim` WRITE;
/*!40000 ALTER TABLE `tim` DISABLE KEYS */;
INSERT INTO `tim` VALUES (3,'PSIholozi','PSI++','Projekat PSI++ je deo praktične nastave na predmetu Principi softverskog inženjerstva, sa idejom da se ilustruje rad na kompleksnijem softveru u realnim uslovima. PSI++ je zamišljen prvenstveno kao program koji bi olakšao rad nastavnom osoblju i studentima na ovom predmetu.'),(4,'Genericni naziv',NULL,NULL);
/*!40000 ALTER TABLE `tim` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `u_timu`
--

DROP TABLE IF EXISTS `u_timu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `u_timu` (
  `KorID` int NOT NULL,
  `TimID` int NOT NULL,
  PRIMARY KEY (`KorID`),
  KEY `u_timu_TimID_887d5627_fk_tim_TimID` (`TimID`),
  CONSTRAINT `u_timu_KorID_8df8bad3_fk_student_KorID` FOREIGN KEY (`KorID`) REFERENCES `student` (`KorID`),
  CONSTRAINT `u_timu_TimID_887d5627_fk_tim_TimID` FOREIGN KEY (`TimID`) REFERENCES `tim` (`TimID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `u_timu`
--

LOCK TABLES `u_timu` WRITE;
/*!40000 ALTER TABLE `u_timu` DISABLE KEYS */;
INSERT INTO `u_timu` VALUES (3,3),(5,3),(4,4);
/*!40000 ALTER TABLE `u_timu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `zadatak`
--

DROP TABLE IF EXISTS `zadatak`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `zadatak` (
  `ZadID` int NOT NULL AUTO_INCREMENT,
  `Rok` datetime(6) NOT NULL,
  `Naslov` varchar(45) NOT NULL,
  `Tekst` varchar(300) NOT NULL,
  `BrFaze` int NOT NULL,
  `KorID` int NOT NULL,
  PRIMARY KEY (`ZadID`),
  KEY `zadatak_KorID_94127739_fk_asistent_KorID` (`KorID`),
  CONSTRAINT `zadatak_KorID_94127739_fk_asistent_KorID` FOREIGN KEY (`KorID`) REFERENCES `asistent` (`KorID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zadatak`
--

LOCK TABLES `zadatak` WRITE;
/*!40000 ALTER TABLE `zadatak` DISABLE KEYS */;
INSERT INTO `zadatak` VALUES (3,'2026-07-31 00:00:00.000000','Formiranje timova','Potrevno je da studenti formiraju timove od 2-4 clanova. Do kraja roka timovi moraju imati da imenuju svoj tim, projekat i da osmisle kratak opis projekta. Studenti koji nisu u timu do kraja roka ce se nasumicno rasporediti.',0,2),(4,'2026-07-13 15:06:00.000000','Projektni zadatak','Napraviti word dokument projektnog zadatka i ubaciti ga u repozitorijum.',1,2),(5,'2026-07-23 18:30:00.000000','SSU dokument i prototip aplikacije','Napraviti SSU dokument za svaki funkcionalni zahtev iz Projektnog zadatka, kao i prototip aplikacije.',2,2);
/*!40000 ALTER TABLE `zadatak` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `zahteva`
--

DROP TABLE IF EXISTS `zahteva`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `zahteva` (
  `TimID` int NOT NULL,
  `KorID` int NOT NULL,
  PRIMARY KEY (`KorID`,`TimID`),
  KEY `zahteva_TimID_73f53c05_fk_tim_TimID` (`TimID`),
  CONSTRAINT `zahteva_KorID_8f284420_fk_student_KorID` FOREIGN KEY (`KorID`) REFERENCES `student` (`KorID`),
  CONSTRAINT `zahteva_TimID_73f53c05_fk_tim_TimID` FOREIGN KEY (`TimID`) REFERENCES `tim` (`TimID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zahteva`
--

LOCK TABLES `zahteva` WRITE;
/*!40000 ALTER TABLE `zahteva` DISABLE KEYS */;
INSERT INTO `zahteva` VALUES (4,6);
/*!40000 ALTER TABLE `zahteva` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-13 18:41:31
