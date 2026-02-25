-- MySQL dump 10.13  Distrib 8.3.0, for macos14 (arm64)
--
-- Host: localhost    Database: Deshidratacion
-- ------------------------------------------------------
-- Server version	8.3.0

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
-- Table structure for table `Alertas`
--

DROP TABLE IF EXISTS `Alertas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Alertas` (
  `ID_Alerta` int NOT NULL AUTO_INCREMENT,
  `ID_Proceso` int NOT NULL,
  `Tipo` varchar(50) NOT NULL,
  `Mensaje` varchar(255) NOT NULL,
  `Fecha` datetime NOT NULL,
  PRIMARY KEY (`ID_Alerta`),
  KEY `ID_Proceso` (`ID_Proceso`),
  CONSTRAINT `alertas_ibfk_1` FOREIGN KEY (`ID_Proceso`) REFERENCES `Procesos` (`ID_Proceso`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Alertas`
--

LOCK TABLES `Alertas` WRITE;
/*!40000 ALTER TABLE `Alertas` DISABLE KEYS */;
/*!40000 ALTER TABLE `Alertas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Frutas`
--

DROP TABLE IF EXISTS `Frutas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Frutas` (
  `ID_Fruta` int NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(100) NOT NULL,
  `Tipo` varchar(50) DEFAULT NULL,
  `Tiempo_Deshidratacion` int NOT NULL,
  `Temperatura_Ideal` decimal(5,2) NOT NULL,
  PRIMARY KEY (`ID_Fruta`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Frutas`
--

LOCK TABLES `Frutas` WRITE;
/*!40000 ALTER TABLE `Frutas` DISABLE KEYS */;
INSERT INTO `Frutas` VALUES (2,'pera','fruta',29,23.00),(3,'Manzana','Fruta',2,13.00),(4,'Fresa','Fruta',1,12.00);
/*!40000 ALTER TABLE `Frutas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Procesos`
--

DROP TABLE IF EXISTS `Procesos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Procesos` (
  `ID_Proceso` int NOT NULL AUTO_INCREMENT,
  `ID_Fruta` int NOT NULL,
  `ID_Usuario` int NOT NULL,
  `Fecha_Inicio` datetime NOT NULL,
  `Fecha_Fin` datetime DEFAULT NULL,
  `Estado` varchar(50) NOT NULL,
  `Resultado` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID_Proceso`),
  KEY `ID_Fruta` (`ID_Fruta`),
  KEY `ID_Usuario` (`ID_Usuario`),
  CONSTRAINT `procesos_ibfk_1` FOREIGN KEY (`ID_Fruta`) REFERENCES `Frutas` (`ID_Fruta`),
  CONSTRAINT `procesos_ibfk_2` FOREIGN KEY (`ID_Usuario`) REFERENCES `Usuarios` (`ID_Usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Procesos`
--

LOCK TABLES `Procesos` WRITE;
/*!40000 ALTER TABLE `Procesos` DISABLE KEYS */;
INSERT INTO `Procesos` VALUES (2,3,4,'2026-01-15 22:23:20','2026-01-16 00:01:53','finalizado','deshidratado'),(7,3,2,'2026-01-16 00:02:11','2026-01-16 00:58:33','finalizado','deshidratado'),(8,4,2,'2026-01-16 12:51:38',NULL,'en progreso',NULL);
/*!40000 ALTER TABLE `Procesos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Reporte_Final`
--

DROP TABLE IF EXISTS `Reporte_Final`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Reporte_Final` (
  `ID_Reporte` int NOT NULL AUTO_INCREMENT,
  `ID_Proceso` int NOT NULL,
  `Fecha_Generacion` datetime NOT NULL,
  `Duracion_Minutos` int DEFAULT NULL,
  `Total_Alertas` int DEFAULT NULL,
  `Temperatura_Promedio` decimal(5,2) DEFAULT NULL,
  `Resultado` varchar(50) DEFAULT NULL,
  `Observaciones` text,
  PRIMARY KEY (`ID_Reporte`),
  KEY `ID_Proceso` (`ID_Proceso`),
  CONSTRAINT `reporte_final_ibfk_1` FOREIGN KEY (`ID_Proceso`) REFERENCES `Procesos` (`ID_Proceso`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Reporte_Final`
--

LOCK TABLES `Reporte_Final` WRITE;
/*!40000 ALTER TABLE `Reporte_Final` DISABLE KEYS */;
INSERT INTO `Reporte_Final` VALUES (1,2,'2026-01-16 00:53:43',98,1,13.00,'finalizado','Se deshidrato bien'),(2,7,'2026-01-16 01:03:07',56,0,13.00,'finalizado','Sin incidencias'),(3,2,'2026-01-16 12:52:14',98,0,13.00,'finalizado','Sin incidencias');
/*!40000 ALTER TABLE `Reporte_Final` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Usuarios`
--

DROP TABLE IF EXISTS `Usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Usuarios` (
  `ID_Usuario` int NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(100) NOT NULL,
  `Email` varchar(150) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `Rol` varchar(50) NOT NULL,
  PRIMARY KEY (`ID_Usuario`),
  UNIQUE KEY `Email` (`Email`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Usuarios`
--

LOCK TABLES `Usuarios` WRITE;
/*!40000 ALTER TABLE `Usuarios` DISABLE KEYS */;
INSERT INTO `Usuarios` VALUES (2,'Cristel','martinezcristel953@gmail.com','12345','administrador'),(4,'Yeni','yenimtzga@gmail.com','1234','administrador'),(7,'Brissa','brisa123@gmail.com','1234','operador');
/*!40000 ALTER TABLE `Usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-25 16:37:47
