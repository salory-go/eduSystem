from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    userNumber = fields.CharField(max_length=32, description="学工号", unique=True)
    password = fields.CharField(max_length=32, description="密码")
    email = fields.CharField(max_length=32, description="电子邮箱", unique=True)
    name = fields.CharField(max_length=32, description="姓名")
    role = fields.IntField(description="角色(1.教师2.管理员3.学生)")
    personalization = fields.CharField(max_length=32,description="个性化内容")  # 格式待定
    createTime = fields.DatetimeField(description="创建时间")
    updateTime = fields.DatetimeField(description="更新时间")


class Course(Model):
    id = fields.IntField(pk=True)
    courseName = fields.CharField(max_length=32, description="课程名称", unique=True)
    userId = fields.IntField(description="教师ID")
    createTime = fields.DatetimeField(description="创建时间")
    updateTime = fields.DatetimeField(description="更新时间")


class Student_Course(Model):
    id = fields.IntField(pk=True)
    userId = fields.IntField(description="学生ID")
    courseId = fields.IntField(description="课程ID")


class Question(Model):
    id = fields.IntField(pk=True)
    courseId = fields.IntField()
    userId = fields.IntField(description="教师ID")
    chapter = fields.CharField(max_length=32,description="章节")
    content = fields.CharField(max_length=500, description="题目内容")
    answer = fields.CharField(max_length=500, description="题目答案")
    difficulty = fields.IntField(description="题目难度(1.简单2.中等3.困难")
    topic = fields.CharField(max_length=32, description="知识点")
    createTime = fields.DatetimeField(description="创建时间")
    updateTime = fields.DatetimeField(description="更新时间")


class Assignment(Model):
    id = fields.IntField(pk=True)
    courseId = fields.IntField(description="课程ID")
    userId = fields.IntField(description="教师ID")
    title = fields.CharField(max_length=32, description="作业标题")
    description = fields.CharField(max_length=500, description="作业描述")
    deadline = fields.DatetimeField(description="截止时间")
    overdue = fields.BooleanField(description="是否过期")
    createTime = fields.DatetimeField(description="创建时间")
    updateTime = fields.DatetimeField(description="更新时间")


class Assignment_Question(Model):
    id = fields.IntField(pk=True)
    assignmentId = fields.IntField(description="作业ID")
    userId = fields.IntField(description="学生ID")
    questionIds = fields.CharField(max_length=100,description="题目列表")


class Student_Answer(Model):
    id = fields.IntField(pk=True)
    userId = fields.IntField(description="学生ID")
    questionId = fields.IntField(description="题目ID")
    studentAnswer = fields.CharField(max_length=500, description="学生答案")
    isCorrect = fields.BooleanField(description="学生答案是否正确")
    submitTime = fields.DatetimeField(description="提交时间")


class Student_Assignment(Model):
    id = fields.IntField(pk=True)
    userId = fields.IntField(description="学生ID")
    assignmentId = fields.IntField(description="作业ID")
    completed = fields.BooleanField(description="是否完成")
    score = fields.FloatField(description="成绩")
    submitTime = fields.DatetimeField(description="提交时间")


class Star(Model):
    id = fields.IntField(pk=True)
    userId = fields.IntField(description="学生ID")
    questionId = fields.IntField(description="题目ID")
    createTime = fields.DatetimeField(description="创建时间")

# class Suggestion(Model):
#     id = fields.IntField(pk=True)
#     studentId = fields.IntField(description="学生ID")
#     content = fields.CharField(max_length=500,description="建议内容")
#     createTime = fields.DatetimeField(description="创建时间")
#     updateTime = fields.DatetimeField(description="更新时间")

# class Exam(Model):
#     id = fields.IntField(pk=True)
#     title = fields.CharField(max_length=32,description="试卷标题")
#     description = fields.CharField(max_length=100,description="试卷描述")
#     teacherId = fields.IntField(description="创建者")
#     createTime = fields.DatetimeField(description="创建时间")
#     updateTime = fields.DatetimeField(description="更新时间")
#
# class Exam_Question(Model):
#     id = fields.IntField(pk=True)
#     examId = fields.IntField(description="试卷ID")
#     questionId = fields.IntField(description="题目ID")
#     weight = fields.IntField(description="题目权重")
