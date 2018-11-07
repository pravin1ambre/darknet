use camera_images;
CREATE TABLE `image` (
  `id` bigint(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(50) NOT NULL,
  `filepath` TEXT NOT NULL,
  `hostname` TEXT NOT NULL,
  `timestamp` int(11) DEFAULT NULL,
  `mac_address` TEXT NOT NULL,
  `objects` TEXT DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) AUTO_INCREMENT=0;





CREATE TABLE `camera_image` (
  `uuid` varchar(225) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `thumbnail_filepath` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `image_filepath` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `detected_objects` json DEFAULT NULL,
  `payload` json DEFAULT NULL,
  `bb_hostname` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `timestamp` int(13) NOT NULL,
  `cam_mac_address` varchar(25) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`cam_mac_address`, `uuid`)
);