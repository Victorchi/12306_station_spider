CREATE  database IF NOT EXISTS `12306-train`;

GRANT  USAGE ON *.* TO '12306'@'localhost';
DROP USER '12306'@'localhost';

CREATE USER '12306'@'localhost' IDENTFIED BY '12306';
GRANT ALL PRIVILEGES ON `12306-train`.* to '12306'@'localhost';

USE `12306-train`;

drop table if not exists 'example':

create table 'example'(
`code` varchar(6) primary key,
`start` varchar(6) not null,
`end` varchar(6) not null
) ENGINE = INNODB DEFAULT CHARSET = utf8;
insert ignore into `example` values ('G308', '成都', '北京'), ('G101', '北京', '上海'), ('D352', '上海', '成都');