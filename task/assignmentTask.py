from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from pojo.entity import Assignment

scheduler = AsyncIOScheduler()


@scheduler.scheduled_job(trigger=IntervalTrigger(minutes=5))
async def check_overdue():
    assignments = await Assignment.filter(overdue=False).values('id', 'deadline')
    print(1)
    for a in assignments:
        if a['deadline'] < datetime.now():
            await Assignment.filter(id=a['id']).update(overdue=True)
