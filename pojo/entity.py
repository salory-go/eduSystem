from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    userNumber = fields.CharField(max_length=32, description="学工号", unique=True)
    password = fields.CharField(max_length=32, description="密码", default="123456")
    email = fields.CharField(max_length=32, description="电子邮箱", unique=True)
    name = fields.CharField(max_length=32, description="姓名")
    role = fields.IntField(description="角色(1.教师2.管理员3.学生)")
    createTime = fields.DatetimeField(description="创建时间", auto_now_add=True)
    updateTime = fields.DatetimeField(description="更新时间", auto_now=True)


class Course(Model):
    id = fields.IntField(pk=True)
    image = fields.CharField(max_length=32, description="课程头像")
    courseName = fields.CharField(max_length=32, description="课程名称", unique=True)
    userId = fields.IntField(description="教师ID")
    createTime = fields.DatetimeField(description="创建时间", auto_now_add=True)
    updateTime = fields.DatetimeField(description="更新时间", auto_now=True)


class Student_Course(Model):
    id = fields.IntField(pk=True)
    userId = fields.IntField(description="学生ID")
    courseId = fields.IntField(description="课程ID")
    joinTime = fields.DatetimeField(description="加入时间", auto_now_add=True)


class Question(Model):
    id = fields.IntField(pk=True)
    courseId = fields.IntField(description="课程ID")
    chapterId = fields.IntField(description="章节ID")
    userId = fields.IntField(description="教师ID")
    content = fields.TextField(max_length=500, description="题目内容")
    answer = fields.TextField(max_length=500, description="题目答案")
    difficulty = fields.IntField(description="题目难度(1.简单2.中等3.困难")
    createTime = fields.DatetimeField(description="创建时间", auto_now_add=True)
    updateTime = fields.DatetimeField(description="更新时间", auto_now=True)


class Chapter(Model):
    id = fields.IntField(pk=True)
    chapterName = fields.CharField(max_length=32, description="章节名称", unique=True)
    courseId = fields.IntField(description="课程ID")
    createTime = fields.DatetimeField(description="创建时间", auto_now_add=True)
    updateTime = fields.DatetimeField(description="更新时间", auto_now=True)


class Assignment(Model):
    id = fields.IntField(pk=True)
    courseId = fields.IntField(description="课程ID")
    chapterId = fields.IntField(description="章节ID")
    userId = fields.IntField(description="教师ID")
    title = fields.CharField(max_length=32, description="作业标题")
    deadline = fields.DatetimeField(description="截止时间")
    overdue = fields.BooleanField(description="是否过期", default=False)
    isPersonalized = fields.BooleanField(description="是否个性化")
    createTime = fields.DatetimeField(description="创建时间", auto_now_add=True)
    updateTime = fields.DatetimeField(description="更新时间,", auto_now=True)


class Assignment_Question(Model):
    id = fields.IntField(pk=True)
    assignmentId = fields.IntField(description="作业ID")
    userId = fields.IntField(description="学生ID")
    questionId = fields.IntField(description="题目ID")
    studentAnswer = fields.TextField(max_length=500, description="学生答案", default="")
    score = fields.FloatField(description="得分", default=0)


class Student_Answer(Model):
    id = fields.IntField(pk=True)
    userId = fields.IntField(description="学生ID")
    questionId = fields.IntField(description="题目ID")
    studentAnswer = fields.TextField(max_length=500, description="学生答案")
    score = fields.FloatField(description="学生答案分数", default=0)
    submitTime = fields.DatetimeField(description="提交时间", auto_now_add=True)


class Student_Assignment(Model):
    id = fields.IntField(pk=True)
    userId = fields.IntField(description="学生ID")
    assignmentId = fields.IntField(description="作业ID")
    completed = fields.BooleanField(description="是否完成", default=False)
    score = fields.FloatField(description="成绩", default=0)


class Star(Model):
    id = fields.IntField(pk=True)
    userId = fields.IntField(description="学生ID")
    questionId = fields.IntField(description="题目ID")
    createTime = fields.DatetimeField(description="创建时间", auto_now_add=True)


class Question_Recommend(Model):
    id = fields.IntField(pk=True)
    userId = fields.IntField(description="学生ID")
    courseName = fields.CharField(max_length=50, description="课程名称")
    chapterName = fields.CharField(max_length=50, description="章节名称")
    content = fields.TextField(max_length=500, description="推荐内容")
    difficulty = fields.IntField(description="题目难度")
    createTime = fields.DatetimeField(description="创建时间", auto_now_add=True)


class Behavior(Model):
    id = fields.IntField(pk=True)
    userId = fields.IntField(description="学生ID")
    behavior = fields.TextField(description='学生行为')
    createTime = fields.DatetimeField(description="创建时间", auto_now_add=True)

