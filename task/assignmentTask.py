from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from pojo.entity import Assignment
from util.logger import logger

scheduler = AsyncIOScheduler()


@scheduler.scheduled_job(trigger=IntervalTrigger(seconds=5))
async def check_overdue():
    logger.info("check overdue assignments...")

    assignments = await Assignment.filter(overdue=False).values('id', 'deadline')
    for a in assignments:
        if a['deadline'] < datetime.now().replace(microsecond=0):
            await Assignment.filter(id=a['id']).update(overdue=True)
