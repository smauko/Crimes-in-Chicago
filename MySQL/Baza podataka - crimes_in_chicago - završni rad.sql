DROP DATABASE IF EXISTS crimes_in_chicago;
CREATE DATABASE crimes_in_chicago;
USE crimes_in_chicago;


CREATE TABLE lokacija (
 id INTEGER AUTO_INCREMENT,
 adresa VARCHAR(60) UNIQUE,
 strana_grada VARCHAR(25),
 last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 CONSTRAINT lokacija_pk PRIMARY KEY(id)
);


CREATE TABLE tip_zlocina (
 id INTEGER AUTO_INCREMENT,
 tip_zlocina VARCHAR(40) UNIQUE,
 cijena_zlocina DECIMAL(10,2),
 last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 CONSTRAINT tip_zlocina_pk PRIMARY KEY(id)
);


CREATE TABLE dobna_skupina (
 id INTEGER AUTO_INCREMENT,
 dobna_skupina VARCHAR(30) UNIQUE,
 raspon_godina VARCHAR(10) UNIQUE,
 CONSTRAINT dobna_skupina_pk PRIMARY KEY(id)
);


CREATE TABLE pocinitelj (
 id INTEGER AUTO_INCREMENT,
 spol CHAR(1),
 prijasnje_kaznjavnanje VARCHAR(5),	
 id_dobna_skupina INT,
 last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 CONSTRAINT pocinitelj_pk PRIMARY KEY(id),
 CONSTRAINT dobna_skupina_fk FOREIGN KEY (id_dobna_skupina) REFERENCES dobna_skupina (id)
);


CREATE TABLE pocinjeni_zlocini (
 id INTEGER AUTO_INCREMENT,
 datum DATE,
 vrijeme TIME,
 opis_zlocina TEXT,
 uhicenje VARCHAR(5),
 obiteljsko_zlostavljanje VARCHAR(5),
 mjesto_i_okruzenje VARCHAR(85),
 kolicina_svjedoka INT,
 id_tip_zlocina INT,
 id_pocinitelj INT,
 id_lokacija INT,
 last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 CONSTRAINT pocinjeni_zlocini_pk PRIMARY KEY(id),
 CONSTRAINT tip_zlocina_fk FOREIGN KEY (id_tip_zlocina) REFERENCES tip_zlocina (id) on delete set null,
 CONSTRAINT pocinitelj_fk FOREIGN KEY (id_pocinitelj) REFERENCES pocinitelj (id) on delete set null,
 CONSTRAINT lokacija_fk FOREIGN KEY (id_lokacija) REFERENCES lokacija (id) on delete set null
);

INSERT INTO dobna_skupina VALUES (1,'Teen','13-19'),
                         (2,'Young adult','20-29'),
                         (3,'Middle age','30-49'),
                          (4,'Senior','50+');

SET SQL_SAFE_UPDATES = 1; 


-- prije prvog update-a kroz pentaho napraviti etl proces
UPDATE `crimes_in_chicago`.`lokacija` SET `adresa` = '043XX S WOOD STA', `last_modified` = '2024-10-31 01:32:42' WHERE (`id` = '1');
UPDATE `crimes_in_chicago`.`pocinjeni_zlocini` SET `vrijeme` = '13:32:00' WHERE (`id` = '1');
-- prije drugog update-a kroz pentaho ponovno napraviti etl proces
UPDATE `crimes_in_chicago`.`lokacija` SET `adresa` = '043XX S WOOD ST', `last_modified` = '2024-10-31 01:35:17' WHERE (`id` = '1');




