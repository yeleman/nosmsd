ALTER TABLE `inbox` ADD `status` ENUM( 'created', 'processed', 'error' ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT 'created',
ADD INDEX ( `status` );
