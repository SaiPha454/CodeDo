from sqlalchemy.ext.asyncio import AsyncSession
from services.questioner_problem_service import QuestionerProblemService
from repositories.participant_problem_repository import ParticipantProblemRepository
from repositories.participant_submission_repository import UserSubmissionRepository
from fastapi import HTTPException


class ParticipantProblemService:
    @staticmethod
    async def get_problem_detail( user_id: int, problem_id: int, db: AsyncSession):
        # Call the QuestionerProblemService to fetch problem details
        problem = await QuestionerProblemService.get_problem(problem_id, db)

        # Fetch the submission for the problem
        submission = await UserSubmissionRepository.get_submission_status(user_id, problem_id, db)

        # Attach the submission to the problem details
        problem.submission = submission

        return problem

    @staticmethod
    async def get_sample_test_cases(problem_id: int, db: AsyncSession):
        # get the test firs two testcases of a problem
        testcases = await ParticipantProblemRepository.get_first_two_test_cases(problem_id, db)
        return testcases
    
    @staticmethod
    async def get_problem_by_id(problem_id: int, db: AsyncSession):
        problem = await ParticipantProblemRepository.get_problem_by_id(problem_id, db)
        if not problem:
            raise HTTPException(status_code=404, detail="Problem not found")    
        return problem