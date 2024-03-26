from util.dateParse import parse

from fastapi import APIRouter, Query
from typing import Optional, List

from pojo.entity import Question, Course, Chapter, Star, Student_Answer, Assignment_Question
from pojo.dto import QuestionDTO, QuestionListDTO
from pojo.vo import QuestionVO
from pojo.result import Result
from util.chatglmApi import generate_question

teacher_question = APIRouter()


@teacher_question.get("/question/{userId}")
async def get_questions(userId: int,
                        courseId: Optional[int] = None,
                        chapterId: Optional[int] = None,
                        difficulty: Optional[int] = None):
    query = {
        'userId': userId,
        'courseId': courseId,
        'chapterId': chapterId,
        'difficulty': difficulty
    }
    query = {k: v for k, v in query.items() if v is not None}

    questions = await Question.filter(**query).values('id',
                                                      'content',
                                                      'answer',
                                                      'courseId',
                                                      'chapterId',
                                                      'difficulty',
                                                      'createTime')
    questionList = []
    for q in questions:
        course = await Course.get(id=q['courseId']).values('courseName')
        chapter = await Chapter.get(id=q['chapterId']).values('chapterName')

        questionList.append(QuestionVO(id=q['id'],
                                       courseName=course['courseName'],
                                       chapterName=chapter['chapterName'],
                                       content=q['content'],
                                       answer=q['answer'],
                                       difficulty=q['difficulty'],
                                       createTime=parse(q['createTime'])))

    return Result.success(questionList)


@teacher_question.post("/question/new")
async def new_questions(questionDTO: QuestionDTO):
    # 使用模型生成新题目
    if questionDTO.isSimilar:
        res = generate_question(questionDTO.number,
                                questionDTO.courseName,
                                questionDTO.chapterName,
                                questionDTO.difficulty,
                                questionDTO.content)
    else:
        res = generate_question(questionDTO.number,
                                questionDTO.courseName,
                                questionDTO.chapterName,
                                questionDTO.difficulty)
    questionList = []
    i = 1
    for q in res:
        questionList.append(QuestionVO(id=i,
                                       courseName=questionDTO.courseName,
                                       chapterName=questionDTO.chapterName,
                                       difficulty=questionDTO.difficulty,
                                       **q)
                            .model_dump(exclude_unset=True))
        i += 1
    return Result.success(questionList)


@teacher_question.post("/question")
async def add_questions(questionList: QuestionListDTO):
    userId = questionList.userId
    questions = questionList.questions

    for q in questions:
        course = await Course.get(courseName=q.courseName).values('id')
        chapter = await Chapter.get(chapterName=q.chapterName).values('id')

        question = Question(userId=userId,
                            courseId=course['id'],
                            chapterId=chapter['id'],
                            content=q.content,
                            answer=q.answer,
                            difficulty=q.difficulty)
        await question.save()
    return Result.success()


@teacher_question.delete("/question")
async def del_question(questionIds: List[int] = Query(...)):
    await Question.filter(id__in=questionIds).delete()
    await Assignment_Question.filter(questionId__in=questionIds).delete()
    await Star.filter(questionId__in=questionIds).delete()
    await Student_Answer.filter(questionId__in=questionIds).delete()
    return Result.success()
