from datetime import datetime

from fastapi import APIRouter

from pojo.entity import Assignment, Assignment_Question
from pojo.dto import AssignmentDTO
from util.result import Result

assignment = APIRouter()


@assignment.get("/teacher/assignment")
async def get_assignments(userId: int):
    assignments = await Assignment.filter(userId=userId)
    return Result.success(assignments)


@assignment.post("/teacher/assignment")
async def create_assignment(tags: AssignmentDTO):
    tags.createTime = datetime.now()
    tags.updateTime = datetime.now()
    questionIds = tags.questionIds

    new_assignment = Assignment(**tags.model_dump(exclude_unset=True).pop("questionIds"))
    await new_assignment.save()
    id = new_assignment.id
    # TODO
    for qId in questionIds:
        Assignment_Question.create()