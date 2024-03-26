from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from pojo.entity import Assignment, Behavior, User, Question_Recommend
from util.chatglmApi import generate_recommend
from util.dateParse import parse
from util.logger import logger

scheduler = AsyncIOScheduler()


@scheduler.scheduled_job(trigger=IntervalTrigger(seconds=5))
async def assignment_task():
    logger.info("check overdue assignments...")

    assignments = await Assignment.filter(overdue=False).values('id', 'deadline')
    for a in assignments:
        if parse(a['deadline']) <= datetime.now().timestamp():
            await Assignment.filter(id=a['id']).update(overdue=True)


@scheduler.scheduled_job(trigger=IntervalTrigger(seconds=10))
async def recommend_task():
    logger.info("recommend questions...")

    userIds = await User.all().values_list('id', flat=True)
    for userId in userIds:
        behaviors = await Behavior.filter(userId=userId).values_list('behavior', flat=True)
        questions = generate_recommend(behaviors)

        questionList = []
        for q in questions:
            questionList.append(Question_Recommend(**q, userId=userId))

        await Question_Recommend.bulk_create(questionList)
