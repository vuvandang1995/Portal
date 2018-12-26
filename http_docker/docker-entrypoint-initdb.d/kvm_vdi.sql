-- MySQL dump 10.13  Distrib 5.7.24, for Linux (x86_64)
--
-- Host: localhost    Database: kvm_vdi
-- ------------------------------------------------------
-- Server version	5.7.24-0ubuntu0.16.04.1

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add snapshot',1,'add_snapshot'),(2,'Can change snapshot',1,'change_snapshot'),(3,'Can delete snapshot',1,'delete_snapshot'),(4,'Can view snapshot',1,'view_snapshot'),(5,'Can add sshkeys',2,'add_sshkeys'),(6,'Can change sshkeys',2,'change_sshkeys'),(7,'Can delete sshkeys',2,'delete_sshkeys'),(8,'Can view sshkeys',2,'view_sshkeys'),(9,'Can add flavors',3,'add_flavors'),(10,'Can change flavors',3,'change_flavors'),(11,'Can delete flavors',3,'delete_flavors'),(12,'Can view flavors',3,'view_flavors'),(13,'Can add server',4,'add_server'),(14,'Can change server',4,'change_server'),(15,'Can delete server',4,'delete_server'),(16,'Can view server',4,'view_server'),(17,'Can add ops',5,'add_ops'),(18,'Can change ops',5,'change_ops'),(19,'Can delete ops',5,'delete_ops'),(20,'Can view ops',5,'view_ops'),(21,'Can add oders',6,'add_oders'),(22,'Can change oders',6,'change_oders'),(23,'Can delete oders',6,'delete_oders'),(24,'Can view oders',6,'view_oders'),(25,'Can add my user',7,'add_myuser'),(26,'Can change my user',7,'change_myuser'),(27,'Can delete my user',7,'delete_myuser'),(28,'Can view my user',7,'view_myuser'),(29,'Can add networks',8,'add_networks'),(30,'Can change networks',8,'change_networks'),(31,'Can delete networks',8,'delete_networks'),(32,'Can view networks',8,'view_networks'),(33,'Can add images',9,'add_images'),(34,'Can change images',9,'change_images'),(35,'Can delete images',9,'delete_images'),(36,'Can view images',9,'view_images'),(37,'Can add log entry',10,'add_logentry'),(38,'Can change log entry',10,'change_logentry'),(39,'Can delete log entry',10,'delete_logentry'),(40,'Can view log entry',10,'view_logentry'),(41,'Can add permission',11,'add_permission'),(42,'Can change permission',11,'change_permission'),(43,'Can delete permission',11,'delete_permission'),(44,'Can view permission',11,'view_permission'),(45,'Can add group',12,'add_group'),(46,'Can change group',12,'change_group'),(47,'Can delete group',12,'delete_group'),(48,'Can view group',12,'view_group'),(49,'Can add content type',13,'add_contenttype'),(50,'Can change content type',13,'change_contenttype'),(51,'Can delete content type',13,'delete_contenttype'),(52,'Can view content type',13,'view_contenttype'),(53,'Can add session',14,'add_session'),(54,'Can change session',14,'change_session'),(55,'Can delete session',14,'delete_session'),(56,'Can view session',14,'view_session');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `client_networks`
--

DROP TABLE IF EXISTS `client_networks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `client_networks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `subnets_associated` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `shared` int(11) NOT NULL,
  `external` int(11) NOT NULL,
  `status` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `admin_state_up` int(11) NOT NULL,
  `owner` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `client_networks_owner_96699445_fk_superadmin_myuser_id` (`owner`),
  CONSTRAINT `client_networks_owner_96699445_fk_superadmin_myuser_id` FOREIGN KEY (`owner`) REFERENCES `superadmin_myuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client_networks`
--

LOCK TABLES `client_networks` WRITE;
/*!40000 ALTER TABLE `client_networks` DISABLE KEYS */;
INSERT INTO `client_networks` VALUES (1,'private_network_1','192.168.0.0/24',0,0,'ACTIVE',1,2),(2,'private_network_1','192.168.0.0/24',0,0,'ACTIVE',1,3);
/*!40000 ALTER TABLE `client_networks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_superadmin_myuser_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_superadmin_myuser_id` FOREIGN KEY (`user_id`) REFERENCES `superadmin_myuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (10,'admin','logentry'),(12,'auth','group'),(11,'auth','permission'),(13,'contenttypes','contenttype'),(14,'sessions','session'),(3,'superadmin','flavors'),(9,'superadmin','images'),(7,'superadmin','myuser'),(8,'superadmin','networks'),(6,'superadmin','oders'),(5,'superadmin','ops'),(4,'superadmin','server'),(1,'superadmin','snapshot'),(2,'superadmin','sshkeys');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'superadmin','0001_initial','2018-12-12 02:07:17.592225'),(2,'contenttypes','0001_initial','2018-12-12 02:07:17.998522'),(3,'admin','0001_initial','2018-12-12 02:07:18.979109'),(4,'admin','0002_logentry_remove_auto_add','2018-12-12 02:07:19.010380'),(5,'admin','0003_logentry_add_action_flag_choices','2018-12-12 02:07:19.033426'),(6,'contenttypes','0002_remove_content_type_name','2018-12-12 02:07:19.589116'),(7,'auth','0001_initial','2018-12-12 02:07:24.375332'),(8,'auth','0002_alter_permission_name_max_length','2018-12-12 02:07:28.964903'),(9,'auth','0003_alter_user_email_max_length','2018-12-12 02:07:29.030245'),(10,'auth','0004_alter_user_username_opts','2018-12-12 02:07:29.124825'),(11,'auth','0005_alter_user_last_login_null','2018-12-12 02:07:29.214939'),(12,'auth','0006_require_contenttypes_0002','2018-12-12 02:07:29.236960'),(13,'auth','0007_alter_validators_add_error_messages','2018-12-12 02:07:29.286094'),(14,'auth','0008_alter_user_username_max_length','2018-12-12 02:07:29.327354'),(15,'auth','0009_alter_user_last_name_max_length','2018-12-12 02:07:29.381377'),(16,'sessions','0001_initial','2018-12-12 02:07:30.101374'),(17,'superadmin','0002_auto_20181212_0921','2018-12-12 02:21:15.122429'),(18,'superadmin','0003_remove_server_status','2018-12-12 03:35:51.650629');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('61cphyjeozugvxf34kt30tgkl8caghez','MzY3ZWUzNTk0MjU2ZTk3NjdiOWUxMzAxMTFiZjA3MjMwMzgxNjI5MDp7Il9hdXRoX3VzZXJfaGFzaCI6ImRhZmQ0N2MxYzliNjM2ZDJmMjYyYmYwZDA2ZWQ5MGMzMDRjODI4MTYiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIzIn0=','2018-12-26 11:37:07.617354'),('m441bijuhb689q34p9qpelgr1y0k1r7f','MzY3ZWUzNTk0MjU2ZTk3NjdiOWUxMzAxMTFiZjA3MjMwMzgxNjI5MDp7Il9hdXRoX3VzZXJfaGFzaCI6ImRhZmQ0N2MxYzliNjM2ZDJmMjYyYmYwZDA2ZWQ5MGMzMDRjODI4MTYiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIzIn0=','2018-12-26 10:09:38.553888'),('mvhqkh5kvsp1u4z05ae3ph1aq8rzobbq','MzY3ZWUzNTk0MjU2ZTk3NjdiOWUxMzAxMTFiZjA3MjMwMzgxNjI5MDp7Il9hdXRoX3VzZXJfaGFzaCI6ImRhZmQ0N2MxYzliNjM2ZDJmMjYyYmYwZDA2ZWQ5MGMzMDRjODI4MTYiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIzIn0=','2018-12-26 08:48:06.635832'),('qudzrizbh6f6bs5su56fm6xj33gfsyyu','MzY3ZWUzNTk0MjU2ZTk3NjdiOWUxMzAxMTFiZjA3MjMwMzgxNjI5MDp7Il9hdXRoX3VzZXJfaGFzaCI6ImRhZmQ0N2MxYzliNjM2ZDJmMjYyYmYwZDA2ZWQ5MGMzMDRjODI4MTYiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIzIn0=','2018-12-26 10:07:57.218607');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flavors`
--

DROP TABLE IF EXISTS `flavors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `flavors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ram` int(11) NOT NULL,
  `vcpus` int(11) NOT NULL,
  `disk` int(11) NOT NULL,
  `i_d` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ops` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `flavors_ops_b85fa3ea_fk_ops_id` (`ops`),
  CONSTRAINT `flavors_ops_b85fa3ea_fk_ops_id` FOREIGN KEY (`ops`) REFERENCES `ops` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flavors`
--

LOCK TABLES `flavors` WRITE;
/*!40000 ALTER TABLE `flavors` DISABLE KEYS */;
INSERT INTO `flavors` VALUES (1,'vip1',1,1,10,'35f5439c-bd05-422e-a3dc-802d9cfd9975',1),(2,'vip2',2,1,10,'709d1428-d37c-4d60-8a2a-f24d3cd6de85',1),(3,'vip3',2,1,15,'6a9a2275-0b49-4e76-a55e-6cd8433206ed',1),(4,'vip4',2,1,20,'728f4491-bb5d-4417-86c7-1dcb3f17b3b5',1),(5,'win',4,2,31,'0c6fdc1f-5605-4a28-900b-ce5f0e6e7005',1);
/*!40000 ALTER TABLE `flavors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `images`
--

DROP TABLE IF EXISTS `images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `images` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `os` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `i_d` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ops` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `images_ops_e97b7171_fk_ops_id` (`ops`),
  CONSTRAINT `images_ops_e97b7171_fk_ops_id` FOREIGN KEY (`ops`) REFERENCES `ops` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `images`
--

LOCK TABLES `images` WRITE;
/*!40000 ALTER TABLE `images` DISABLE KEYS */;
INSERT INTO `images` VALUES (1,'amphora-x64-haproxy','linux','31d05b27-fc72-4c06-8e4c-a4e79e4bf1be',1),(2,'cent7_test','other','86481d09-cdb9-4189-95e0-f9ed83b873ec',1),(3,'windows-10-Home-64bit','windows','e9fbdb23-7909-49fb-bb4e-d881bab9a880',1),(4,'windows-10-Professional-64bit','windows','824f19ea-e17d-417a-bd5c-dee6fee5b467',1),(5,'windows-7-Enterprise-64bit','windows','9966636d-b85c-48b0-906b-88c1cd03d2a8',1),(6,'windows-7-Ultimate-64bit','windows','8fec8c7a-45f9-4157-a040-905ecb17750a',1),(7,'windows-10-64bit','windows','31897cfb-eb32-4aae-8fcd-4ca542650984',1),(8,'windows-10-Enterprise-64bit','windows','4d117298-cf16-4e88-884a-bc3b9db56e64',1),(9,'windows-7-Professional-64bit','windows','16580408-6b93-46a5-bc4f-48540b0d952a',1),(10,'windows-8.1-Professional-64bit','windows','45f16ae1-fbbe-46dd-a9d7-dda0fee1fc11',1),(11,'windows-8.1-Enterprise-64bit','windows','b8e990c1-ae2b-467f-83ce-060c10417060',1),(12,'windows-2k8r2-Standrad-64bit','windows','919c722b-9fb4-4b04-81ca-5d9e6dffd6a1',1),(13,'windows-2k8r2-Datacenter-64bit','windows','32c4f552-252b-4e5c-8165-176056b01e7d',1),(14,'windows-2k12r2-Standrad-64bit','windows','6b63fa45-f402-4f31-a68c-0098c3d83345',1),(15,'windows-2k12r2-Datacenter-64bit','windows','c11efabf-448a-400c-b7ec-8dab64dde4be',1),(16,'windows-2k16-Standard-64bit','windows','0210fb22-a327-4c7e-8c51-fdf2e40e077c',1),(17,'windows-2k16-Datacenter-64bit','windows','fa6e8027-55e4-4cf7-b364-ab6934889749',1),(18,'u16-server','linux','bcfec53c-9f5e-4dbb-91c5-e2509358639d',1),(19,'centos7','other','6676d17f-bc19-4fa2-8d35-123c5e0a0fce',1),(20,'windows-2k8r2-Enterprise-64bit','windows','11caaf64-7004-4911-83ee-ee44a82133b8',1),(21,'windows-2012-64bit-2018','windows','c4be2fdd-bff5-40d9-8a1e-0608bba74ab3',1),(22,'centos66-minimal','linux','ed699aed-ca04-414f-b158-f12078f9878b',1),(23,'u14-server','linux','2a03db93-0112-42eb-8d7c-ad16b7f65e94',1),(24,'centos68-minimal','linux','a92064a7-337b-48d1-b96b-3b8bb6759299',1),(25,'centos7-minimal','linux','17b0d99e-e52e-4116-965b-7bf8cae7b557',1),(26,'cirros-0.3.5-x86_64-disk.raw','other','2db2af14-0f56-417a-b0c3-b2831f24e3f1',1);
/*!40000 ALTER TABLE `images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oders`
--

DROP TABLE IF EXISTS `oders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oders` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `service` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `server` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ip` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `price` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` int(11) NOT NULL,
  `created` datetime(6) NOT NULL,
  `owner` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `oders_owner_71c799c3_fk_superadmin_myuser_id` (`owner`),
  CONSTRAINT `oders_owner_71c799c3_fk_superadmin_myuser_id` FOREIGN KEY (`owner`) REFERENCES `superadmin_myuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oders`
--

LOCK TABLES `oders` WRITE;
/*!40000 ALTER TABLE `oders` DISABLE KEYS */;
INSERT INTO `oders` VALUES (1,'cloud','test',NULL,'205000',1,'2018-12-12 02:32:29.800794',2),(2,'cloud','test',NULL,'205000',1,'2018-12-12 02:37:28.337976',2),(3,'cloud','test',NULL,'205000',1,'2018-12-12 02:53:51.810558',2),(4,'cloud','test2',NULL,'190000',1,'2018-12-12 03:40:51.864912',2),(5,'cloud','hi',NULL,'190000',1,'2018-12-12 03:54:49.180374',2),(6,'cloud','uk',NULL,'220000',1,'2018-12-12 04:07:42.127978',2),(7,'cloud','ll',NULL,'220000',1,'2018-12-12 04:10:19.535970',2),(8,'cloud','um',NULL,'220000',1,'2018-12-12 04:13:33.866240',2),(9,'cloud','hihi',NULL,'205000',1,'2018-12-12 04:18:48.455014',2),(10,'cloud','cam',NULL,'205000',1,'2018-12-12 04:20:43.190008',2),(11,'cloud','cam_snap',NULL,'220000',1,'2018-12-12 04:21:57.570074',2),(12,'cloud','hi',NULL,'205000',1,'2018-12-12 04:24:47.168631',2),(13,'cloud','hi',NULL,'205000',1,'2018-12-12 04:27:09.711792',2),(14,'cloud','hi',NULL,'205000',1,'2018-12-12 04:28:33.120974',2),(15,'cloud','snap1',NULL,'205000',1,'2018-12-12 04:33:57.562551',2),(16,'cloud','snap1',NULL,'205000',1,'2018-12-12 04:35:45.954759',2),(17,'cloud','snap',NULL,'205000',1,'2018-12-12 04:38:25.422996',2),(18,'cloud','snap1',NULL,'220000',1,'2018-12-12 04:40:34.779799',2),(19,'cloud','snap1',NULL,'205000',1,'2018-12-12 04:44:35.875107',2),(20,'cloud','snap2',NULL,'205000',1,'2018-12-12 04:46:48.851135',2),(21,'cloud','snap2',NULL,'220000',1,'2018-12-12 07:06:33.875804',2),(22,'cloud','snap3',NULL,'205000',1,'2018-12-12 07:45:11.466155',2),(23,'cloud','snap3',NULL,'205000',1,'2018-12-12 08:11:55.025217',2),(24,'cloud','snap3',NULL,'205000',1,'2018-12-12 08:13:38.321928',2),(25,'cloud','vm2',NULL,'190000',1,'2018-12-12 08:18:49.495990',2),(26,'cloud','vm1',NULL,'190000',1,'2018-12-12 08:34:07.129468',2),(27,'cloud','thai_test',NULL,'413000',1,'2018-12-12 08:54:31.628522',3),(28,'cloud','thai',NULL,'413000',1,'2018-12-12 09:07:00.758978',3),(29,'cloud','thai_test',NULL,'413000',1,'2018-12-12 09:14:34.265455',3),(30,'cloud','test2',NULL,'205000',1,'2018-12-12 09:24:46.737087',3),(31,'cloud','113',NULL,'220000',1,'2018-12-12 09:44:12.825969',3),(32,'cloud','114',NULL,'220000',1,'2018-12-12 09:50:11.575365',3),(33,'cloud','115',NULL,'205000',1,'2018-12-12 09:54:42.731407',3),(34,'cloud','toan-test-centos68',NULL,'205000',1,'2018-12-12 10:16:32.977499',3),(35,'cloud','toan-window10-Enter-64',NULL,'413000',1,'2018-12-12 10:33:59.114350',3),(36,'cloud','dang_dien_dao',NULL,'413000',1,'2018-12-12 10:56:09.597278',3);
/*!40000 ALTER TABLE `oders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ops`
--

DROP TABLE IF EXISTS `ops`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ops` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ip` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `username` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` longblob NOT NULL,
  `project` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `userdomain` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `projectdomain` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ops`
--

LOCK TABLES `ops` WRITE;
/*!40000 ALTER TABLE `ops` DISABLE KEYS */;
INSERT INTO `ops` VALUES (1,'ITC','10.10.10.99','admin',_binary 'Ä\0\0\0\0\\o|¢ºñãsM%ôæ%v°ó≠g≠\«f\¬7é°\„t˝l˚∫◊≥¥™s>™≥[ÀÉ|Ä\”\÷Tw≤Ò\Ì\…ezOAé\–8∞˝V∏8+xa∞@=É!U˚Öê\ lT\·','admin','default','default');
/*!40000 ALTER TABLE `ops` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `serverVM`
--

DROP TABLE IF EXISTS `serverVM`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `serverVM` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `host` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ip` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ram` int(11) NOT NULL,
  `vcpus` int(11) NOT NULL,
  `disk` int(11) NOT NULL,
  `created` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `i_d` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `owner` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `serverVM_owner_c1db65ff_fk_superadmin_myuser_id` (`owner`),
  CONSTRAINT `serverVM_owner_c1db65ff_fk_superadmin_myuser_id` FOREIGN KEY (`owner`) REFERENCES `superadmin_myuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `serverVM`
--

LOCK TABLES `serverVM` WRITE;
/*!40000 ALTER TABLE `serverVM` DISABLE KEYS */;
INSERT INTO `serverVM` VALUES (28,'dangvv','test',NULL,'vm1',NULL,2,1,10,'2018-12-12T08:34:09Z','a430a857-777f-419e-a0f5-85106656900e',2),(30,'thailq','test',NULL,'thai',NULL,4,2,31,'2018-12-12T09:06:59Z','95ccff08-1688-4a5b-b6c5-0be5b30c6e76',3),(31,'thailq','test',NULL,'thai_test',NULL,4,2,31,'2018-12-12T09:14:32Z','ed37c706-e811-40ea-868b-83c3e52bc931',3),(34,'thailq','test',NULL,'113',NULL,2,1,20,'2018-12-12T09:44:11Z','836b97a6-1898-479c-8b2e-a2af49a00df2',3),(36,'thailq','test',NULL,'115',NULL,2,1,15,'2018-12-12T09:54:45Z','9c190e7b-41da-4376-b1f1-586ca511d014',3),(37,'thailq','test',NULL,'toan-test-centos68',NULL,2,1,15,'2018-12-12T10:16:32Z','486e51c3-8e87-4bd2-b40d-505491030cf8',3),(38,'thailq','test',NULL,'toan-window10-Enter-64',NULL,4,2,31,'2018-12-12T10:33:59Z','3ce1f587-1628-40dc-bc10-8425f7989c8e',3),(39,'thailq','test',NULL,'dang_dien_dao',NULL,4,2,31,'2018-12-12T10:56:11Z','a586cc17-7f44-49e0-a7d9-53f38db2329d',3);
/*!40000 ALTER TABLE `serverVM` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `snapshot`
--

DROP TABLE IF EXISTS `snapshot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `snapshot` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `i_d` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ops` int(11) NOT NULL,
  `owner` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `snapshot_ops_64eacf4e_fk_ops_id` (`ops`),
  KEY `snapshot_owner_bc5e401c_fk_superadmin_myuser_id` (`owner`),
  CONSTRAINT `snapshot_ops_64eacf4e_fk_ops_id` FOREIGN KEY (`ops`) REFERENCES `ops` (`id`),
  CONSTRAINT `snapshot_owner_bc5e401c_fk_superadmin_myuser_id` FOREIGN KEY (`owner`) REFERENCES `superadmin_myuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `snapshot`
--

LOCK TABLES `snapshot` WRITE;
/*!40000 ALTER TABLE `snapshot` DISABLE KEYS */;
INSERT INTO `snapshot` VALUES (5,'thai_test','db6d8c5a-7902-4c5f-8258-642e7eed9e4e',1,3);
/*!40000 ALTER TABLE `snapshot` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sshkeys`
--

DROP TABLE IF EXISTS `sshkeys`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sshkeys` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ops` int(11) NOT NULL,
  `owner` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sshkeys_ops_fe2df5b9_fk_ops_id` (`ops`),
  KEY `sshkeys_owner_f08d16f4_fk_superadmin_myuser_id` (`owner`),
  CONSTRAINT `sshkeys_ops_fe2df5b9_fk_ops_id` FOREIGN KEY (`ops`) REFERENCES `ops` (`id`),
  CONSTRAINT `sshkeys_owner_f08d16f4_fk_superadmin_myuser_id` FOREIGN KEY (`owner`) REFERENCES `superadmin_myuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sshkeys`
--

LOCK TABLES `sshkeys` WRITE;
/*!40000 ALTER TABLE `sshkeys` DISABLE KEYS */;
INSERT INTO `sshkeys` VALUES (2,'THAI',1,3);
/*!40000 ALTER TABLE `sshkeys` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `superadmin_myuser`
--

DROP TABLE IF EXISTS `superadmin_myuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `superadmin_myuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fullname` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `username` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `key` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_admin` tinyint(1) NOT NULL,
  `is_adminkvm` tinyint(1) NOT NULL,
  `token_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `token_expired` datetime(6) DEFAULT NULL,
  `money` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `superadmin_myuser`
--

LOCK TABLES `superadmin_myuser` WRITE;
/*!40000 ALTER TABLE `superadmin_myuser` DISABLE KEYS */;
INSERT INTO `superadmin_myuser` VALUES (1,'pbkdf2_sha256$120000$JNyLqK3OaCAR$PHPktPNQI5bsQ2EXReDsa9OPlGq/J1dyXYWNLoBbG5g=','2018-12-12 09:20:18.268598','admin@gmail.com','admin','admin','be3037e1629d0d237aec5e81b1bc1fe0889e70f0f0432724',1,0,1,'gAAAAABcEOitMKpdFRBh_IX3c8T2ytNx-fgClA278gNjtRcY58nbsNEKVI7UOlENQrdEa3gzEwW_CZg8l-DyTy9_cW69D2tuVUA431KkTft6GqLDHp8bBcRCw0uHf4PH5J2tSr0uK0WFUG7XTMGkImY69Np35ijdf7lTM8mJYdrzOYR_5VFQsMc','2018-12-12 11:18:32.460642','0'),(2,'pbkdf2_sha256$120000$jK8xeCszfcxa$F50u/AqsVwn/Jg1itYVZBT04o9DHVxMS3l9kfNiHlv8=','2018-12-12 02:46:57.019811','dangdiendao@gmail.com','V≈© VƒÉn ƒê·∫∑ng','dangvv','24df1b10348e65e7db471a7e3da481d2fd5d67ac368e3452',1,0,0,'gAAAAABcEM_Ks5nv7mG1PnTUD-ExV8u0RELhAKRHcc_M2t0U9ZrIl3KE1PZGyaqsNxF0tcw5OSnXxRSKRPuuOJ__450kpRvuYmj3rhIeIiK2Dbjg7LPEo9loNStgtxTKFD9ey712UL4SjblFflzpEdp_88u26b_oNwYsY3o_qChCpxP6Hdm8ndM','2018-12-12 09:32:22.268227','1e+24'),(3,'pbkdf2_sha256$120000$mJN2cLqi5Ssh$GLVFfbwKt7jrqj4aVA9D9ArRO3lbQAwI9lYExtt5iFw=','2018-12-12 11:37:06.790267','thailq@intercom.vn','thailq','thailq','d38af6f70b76c0ea50b2b271d611a9c6932bc1600b323074',1,0,0,'gAAAAABcEbv6fdx012SLpz6afWuCKzWrgnL6JRgkJWuAcHcSWuKtGwGzDInLNmymMjbBg9-P5jHnMqdJdGX9lUxdjoSfUt9JrCRF-t4-4iFMG3Z5Jr8hx_L0DlIHIEJXcmup7wqZV1Ir3HPQ-UX7SD3UjlH-NlVps9X9iU90QaX6cPymFhIrOfc','2018-12-13 02:20:05.888001','7880000.0');
/*!40000 ALTER TABLE `superadmin_myuser` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-12-12 21:57:51
