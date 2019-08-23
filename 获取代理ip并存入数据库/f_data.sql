CREATE TABLE `foot_data` (
  `game_no` int(11) NOT NULL COMMENT '比赛编号',
  `game_week` varchar(50) DEFAULT NULL COMMENT '比赛场次',
  `start_datetime` datetime DEFAULT NULL COMMENT '开始时间',
  `team1_name` varchar(25) DEFAULT NULL COMMENT '队1',
  `team2_name` varchar(25) DEFAULT NULL COMMENT '队2',
  PRIMARY KEY (`game_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;