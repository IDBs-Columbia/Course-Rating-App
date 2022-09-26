CREATE TABLE `user_props` (
  `email` varchar(50) NOT NULL,
  `name` varchar(30) NOT NULL,
  `password` varchar(255) NOT NULL,
  `is_admin` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`email`)
) ;

CREATE TABLE `admin_user` (
  `admin_id` int NOT NULL AUTO_INCREMENT,
  `can_manage_report` tinyint(1) NOT NULL,
  `can_manage_course` tinyint(1) NOT NULL,
  `can_manage_comment` tinyint(1) NOT NULL,
  `can_manage_user` tinyint(1) NOT NULL,
  `email` varchar(50) NOT NULL,
  PRIMARY KEY (`admin_id`),
  FOREIGN KEY (`email`) REFERENCES `user_props` (`email`) ON DELETE CASCADE
) ;

CREATE TABLE `regular_user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `status` enum('active','restricted','blocked') NOT NULL,
  `strikes` int NOT NULL DEFAULT '0',
  `email` varchar(50) NOT NULL,
  PRIMARY KEY (`user_id`),
  FOREIGN KEY (`email`) REFERENCES `user_props` (`email`) ON DELETE CASCADE
) ;

CREATE TABLE `institution` (
  `institution_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`institution_id`)
) ;

CREATE TABLE `course` (
  `call_number` varchar(5) NOT NULL,
  `course_number` varchar(10) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` longtext,
  `instructor` varchar(100) NOT NULL,
  `institution_id` int DEFAULT NULL,
  PRIMARY KEY (`call_number`),
  FOREIGN KEY (`institution_id`) REFERENCES `institution` (`institution_id`)
) ;

CREATE TABLE `rating` (
  `rating_id` int NOT NULL AUTO_INCREMENT,
  `rating` int NOT NULL,
  `difficulty` int NOT NULL,
  `workload` int NOT NULL,
  `description` longtext NOT NULL,
  `from_user_id` int NOT NULL,
  `to_course_num` varchar(5) NOT NULL,
  PRIMARY KEY (`rating_id`),
  FOREIGN KEY (`to_course_num`) REFERENCES `course` (`call_number`) ON DELETE CASCADE,
  FOREIGN KEY (`from_user_id`) REFERENCES `regular_user` (`user_id`) ON DELETE CASCADE
) ;

CREATE TABLE `comment` (
  `comment_id` int NOT NULL,
  `from_rating_id` int NOT NULL,
  `content` longtext NOT NULL,
  `from_user_id` int NOT NULL,
  `reply_to_comment_id` int DEFAULT NULL,
  PRIMARY KEY (`comment_id`,`from_rating_id`),
  FOREIGN KEY (`from_rating_id`) REFERENCES `rating` (`rating_id`) ON DELETE CASCADE,
  FOREIGN KEY (`from_user_id`) REFERENCES `regular_user` (`user_id`) ON DELETE CASCADE,
  FOREIGN KEY (`reply_to_comment_id`) REFERENCES `comment` (`comment_id`) ON DELETE CASCADE,
) ;

CREATE TABLE `report` (
  `report_id` int NOT NULL AUTO_INCREMENT,
  `category` enum('offensive language','untruthful','academic misconduct') NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `from_user_id` int NOT NULL,
  `to_rating_id` int DEFAULT NULL,
  `to_comment_id` int DEFAULT NULL,
  PRIMARY KEY (`report_id`),
  FOREIGN KEY (`to_comment_id`) REFERENCES `comment` (`comment_id`) ON DELETE CASCADE,
  FOREIGN KEY (`to_rating_id`) REFERENCES `rating` (`rating_id`) ON DELETE CASCADE,
  FOREIGN KEY (`from_user_id`) REFERENCES `regular_user` (`user_id`)
) ;



