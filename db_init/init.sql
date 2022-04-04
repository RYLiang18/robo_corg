CREATE TABLE STREAMER_TBL (
    `id` int NOT NULL AUTO_INCREMENT,
    `twitch_name` varchar(100) DEFAULT NULL,
    `is_live` tinyint(1) DEFAULT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE SUBSCRIBER_TBL (
    `id` int NOT NULL AUTO_INCREMENT,
    `phone_number` tinyblob,
    `discord_id` varchar(100) DEFAULT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE RELATIONSHIP_TBL (
    `streamer_id` int NOT NULL,
    `subscriber_id` int NOT NULL,
    PRIMARY KEY (`streamer_id`,`subscriber_id`),
    KEY `subscriber_id` (`subscriber_id`),
    CONSTRAINT `RELATIONSHIP_TBL_ibfk_1` FOREIGN KEY (`streamer_id`) REFERENCES `STREAMER_TBL` (`id`),
    CONSTRAINT `RELATIONSHIP_TBL_ibfk_2` FOREIGN KEY (`subscriber_id`) REFERENCES `SUBSCRIBER_TBL` (`id`)
)