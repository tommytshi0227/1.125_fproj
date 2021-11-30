--  CREATE ENTITY DB

DROP DATABASE IF EXISTS `entities`;
CREATE DATABASE IF NOT EXISTS `entities`;
USE `entities`;

--  CREATE ENTITIES TABLE

CREATE TABLE `entities` (
   `entityName`   varchar (500),
   `entityType`	varchar (100),
   `entitySalience`	decimal(5,2),
   `entitySentScore`	decimal(5,2),
   `entSentMag`	decimal(5,2)   
);

