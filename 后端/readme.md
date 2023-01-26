
创建数据库命令

CREATE TABLE `weibohotpot1` (
`id` int(8) NOT NULL AUTO_INCREMENT,
`title` varchar(255) DEFAULT NULL,
`url` text,
`hot` int(8) DEFAULT NULL,
`create_date` date DEFAULT NULL,
`zhong` varchar(255) DEFAULT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8



CREATE TABLE `weiboeventsxiang` (
`wid` int(8) NOT NULL,
`title` varchar(255) DEFAULT NULL,
`user_id` int(16) DEFAULT NULL,
`user_name` varchar(255) DEFAULT NULL,
`gender` varchar(2) NOT NULL,
`publish_time` datetime DEFAULT NULL,
`text` text,
`like_count` int(8) NOT NULL,
`comment_count` int(8) NOT NULL,
`forward_count` int(8) NOT NULL,
PRIMARY KEY (`wid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8



select DATE_FORMAT(create_date,'%Y-%m'),count(*) from weibohotpot group by DATE_FORMAT(create_date,'%Y-%m')
select DATE_FORMAT(create_date,'%Y-%m'),count(*) from weibohotpot group by DATE_FORMAT(create_date,'%Y-%m')