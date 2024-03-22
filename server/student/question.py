from typing import Optional

from fastapi import APIRouter

from pojo.dto import AnswerDTO
from pojo.entity import Course, Question, Chapter, Student_Answer
from pojo.vo import QuestionVO, ReferenceVO, AnswerVO
from pojo.result import Result
import os
from zhipuai import ZhipuAI

os.environ["ZHIPUAI_API_KEY"] = "your api key"
client = ZhipuAI()
import  time
def print_with_typewriter_effect(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
student_question = APIRouter()


@student_question.get("/question")
async def get_questions(courseId: Optional[int] = None, difficulty: Optional[int] = None,
                        chapterId: Optional[int] = None):
    query = {
        'courseId': courseId,
        'chapterId': chapterId,
        'difficulty': difficulty
    }
    query = {k: v for k, v in query.items() if v is not None}

    questions = await Question.filter(**query).values("id", "courseId", "chapterId", "content", "difficulty")
    questionList = []
    for q in questions:
        course = await Course.get(id=q["courseId"]).values('courseName')
        chapter = await Chapter.get(id=q["chapterId"]).values('chapterName')

        questionVO = QuestionVO(id=q["id"], courseName=course["courseName"], chapterName=chapter["chapterName"],
                                content=q["content"],
                                difficulty=q["difficulty"])
        questionList.append(questionVO)

    return Result.success(questionList)


@student_question.post("/question")
async def submit_answer(answerDTO: AnswerDTO):
    # TODO 打分
    score = 100
    studentAnswer = await Student_Answer.filter(userId=answerDTO.userId, questionId=answerDTO.questionId).first()
    question = await Question.filter(id=answerDTO.questionId).first()

    if studentAnswer:
        await Student_Answer.filter(userId=answerDTO.userId, questionId=answerDTO.questionId).update(
            studentAnswer=answerDTO.studentAnswer, score=score)
    else:
        await Student_Answer.create(userId=answerDTO.userId, questionId=answerDTO.questionId,
                                    studentAnswer=answerDTO.studentAnswer, score=score)

    return Result.success()


@student_question.get("/question/reference")
async def get_reference(questionId: int):
    question = await Question.get(id=questionId).values("courseId", "chapterId", "content", "answer")
    course = await Course.get(id=question['courseId'])
    chapter = await Chapter.get(id=question['chapterId'])
    courseName = course.courseName
    chapterName = chapter.chapterName
    # TODO 用大模型生成解析
    response = client.chat.completions.create(
        model="glm-4",
        messages=[
            {
                "role": "user",
                "content": "你是一名大学计算机教授，请根据我给出的题目内容，课程名称，章节名称，"
                           "生成一份详细的解析，要求解析内容详细，条理清晰，语言通俗易懂。"
                           "随后再生成这个题目所考察的知识点，要求知识点准确，全面，不重复。"
                           "题目内容为：" +
                           question['content'] + "，课程名称为：" + courseName + "，章节名称为：" +
                           chapterName + "。"+"输出格式为：“解析内容：\n知识点:\n”"
            }
        ],
        top_p=0.7,
        temperature=0.9,
        stream=True,
        max_tokens=2000,
    )

    if response:
        for chunk in response:
            content = chunk.choices[0].delta.content
            print_with_typewriter_effect(content)
    idea = ""
    topic = ""
    reference = ReferenceVO(idea=idea, tpoic=topic, answer=question['answer'])
    return Result.success(reference)


@student_question.get("/question/history")
async def get_history_answer(userId: int, questionId: int):
    studentAnswer = await Student_Answer.filter(userId=userId, questionId=questionId).first()
    answer = AnswerVO(studentAnswer=studentAnswer.studentAnswer,score=studentAnswer.score,submitTime=studentAnswer.submitTime)
    if studentAnswer:
        return Result.success(answer)
    else:
        return Result.error('未曾作答')
