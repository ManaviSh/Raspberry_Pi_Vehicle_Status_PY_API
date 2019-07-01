# Raspberry Pi Vehicle Status Python API
Forked from: 
[Raspberry Pi Mini Weather Station](https://github.com/JeremyMorgan/Raspberry_Pi_Weather_Station)


This is an alternative endpoint Endpoint using Python/Flask and MariaDB on a Linux Server. 


This can be run on the Pi itself
5. Set up MariaDB for the Vehicle Status
  CREATE DATABASE evData;
  GRANT ALL PRIVILEGES ON evData.* TO web@'%' IDENTIFIED BY 'secretpassword';
  FLUSH PRIVILEGES;
  quit

Log in as that web user:
  mysql -u web -p

You will be created with an SQL prompt. Type the following:
use evData;

CREATE TABLE `evData`.`reading` (
  `readingID` INT NOT NULL AUTO_INCREMENT COMMENT '',
  `angle_x` DECIMAL(3,2) NULL COMMENT '',
  `angle_y` DECIMAL(3,2) NULL COMMENT '',
  `angle_z` DECIMAL(3,2) NULL COMMENT '',
  `acc_x` DECIMAL(4,2) NULL COMMENT '',
  `acc_y` DECIMAL(4,2) NULL COMMENT '',
  `acc_z` DECIMAL(4,2) NULL COMMENT '',
  `velocity` DECIMAL(4,2) NULL COMMENT '',
  `Latitude` DECIMAL(9,6) NULL COMMENT '',
  `Longitude` DECIMAL(9,6) NULL COMMENT '',
  `TimeStamp` VARCHAR(45) NULL COMMENT '',
  PRIMARY KEY (`readingID`)  COMMENT '');
This creates your MariaDB database for storing items.
