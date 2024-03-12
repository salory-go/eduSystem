from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `assignment` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `courseId` INT NOT NULL  COMMENT '课程ID',
    `userId` INT NOT NULL  COMMENT '教师ID',
    `title` VARCHAR(32) NOT NULL  COMMENT '作业标题',
    `description` VARCHAR(500) NOT NULL  COMMENT '作业描述',
    `deadline` DATETIME(6) NOT NULL  COMMENT '截止时间',
    `overdue` BOOL NOT NULL  COMMENT '是否过期',
    `createTime` DATETIME(6) NOT NULL  COMMENT '创建时间',
    `updateTime` DATETIME(6) NOT NULL  COMMENT '更新时间'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `assignment_question` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `assignmentId` INT NOT NULL  COMMENT '作业ID',
    `userId` INT NOT NULL  COMMENT '学生ID',
    `questionIds` VARCHAR(100) NOT NULL  COMMENT '题目列表'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `course` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `courseName` VARCHAR(32) NOT NULL UNIQUE COMMENT '课程名称',
    `userId` INT NOT NULL  COMMENT '教师ID',
    `createTime` DATETIME(6) NOT NULL  COMMENT '创建时间',
    `updateTime` DATETIME(6) NOT NULL  COMMENT '更新时间'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `question` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `courseId` INT NOT NULL,
    `userId` INT NOT NULL  COMMENT '教师ID',
    `chapter` VARCHAR(32) NOT NULL  COMMENT '章节',
    `content` VARCHAR(500) NOT NULL  COMMENT '题目内容',
    `answer` VARCHAR(500) NOT NULL  COMMENT '题目答案',
    `difficulty` INT NOT NULL  COMMENT '题目难度(1.简单2.中等3.困难',
    `topic` VARCHAR(32) NOT NULL  COMMENT '知识点',
    `createTime` DATETIME(6) NOT NULL  COMMENT '创建时间',
    `updateTime` DATETIME(6) NOT NULL  COMMENT '更新时间'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `star` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `userId` INT NOT NULL  COMMENT '学生ID',
    `questionId` INT NOT NULL  COMMENT '题目ID',
    `createTime` DATETIME(6) NOT NULL  COMMENT '创建时间'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `student_answer` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `userId` INT NOT NULL  COMMENT '学生ID',
    `questionId` INT NOT NULL  COMMENT '题目ID',
    `studentAnswer` VARCHAR(500) NOT NULL  COMMENT '学生答案',
    `isCorrect` BOOL NOT NULL  COMMENT '学生答案是否正确',
    `submitTime` DATETIME(6) NOT NULL  COMMENT '提交时间'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `student_assignment` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `userId` INT NOT NULL  COMMENT '学生ID',
    `assignmentId` INT NOT NULL  COMMENT '作业ID',
    `completed` BOOL NOT NULL  COMMENT '是否完成',
    `score` DOUBLE NOT NULL  COMMENT '成绩',
    `submitTime` DATETIME(6) NOT NULL  COMMENT '提交时间'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `student_course` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `userId` INT NOT NULL  COMMENT '学生ID',
    `courseId` INT NOT NULL  COMMENT '课程ID'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `user` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(32) NOT NULL UNIQUE COMMENT '姓名',
    `password` VARCHAR(32) NOT NULL  COMMENT '密码',
    `email` VARCHAR(32) NOT NULL UNIQUE COMMENT '电子邮箱',
    `name` VARCHAR(32) NOT NULL  COMMENT '名称',
    `role` INT NOT NULL  COMMENT '角色(1.教师2.管理员3.学生)',
    `personalization` VARCHAR(32) NOT NULL  COMMENT '个性化内容',
    `createTime` DATETIME(6) NOT NULL  COMMENT '创建时间',
    `updateTime` DATETIME(6) NOT NULL  COMMENT '更新时间'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
