from repositories.questioner_problem_repository import QuestionerProblemRepository
from repositories.challenge_model import Challenge
from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from services.questioner_challenge_service import QuestionerChallengeService

class QuestionerProblemService:
    @staticmethod
    async def verify_challenge_exists(challenge_id: int, db: AsyncSession):
        
        challenge = await QuestionerChallengeService.get_challenge(challenge_id, db)
        if not challenge:
            raise HTTPException(status_code=404, detail="Challenge not found")
        

    @staticmethod
    async def get_problems(challenge_id: int, db: AsyncSession):
        return await QuestionerProblemRepository.get_problems_by_challenge_id(challenge_id, db)

    @staticmethod
    async def create_problem(challenge_id: int, title: str, problem_definition: str, input_format: str, output_format: str, db: AsyncSession):
        await QuestionerProblemService.verify_challenge_exists(challenge_id, db)
        return await QuestionerProblemRepository.create_problem(challenge_id, title, problem_definition, input_format, output_format, db)

    @staticmethod
    async def get_problem(problem_id: int, db: AsyncSession):
        problem = await QuestionerProblemRepository.get_problem_by_id(problem_id, db)
        if not problem:
            raise HTTPException(status_code=404, detail="Problem not found")
        return problem

    @staticmethod
    async def update_problem(problem_id: int, title: str, problem_definition: str, input_format: str, output_format: str, db: AsyncSession):
        problem = await QuestionerProblemRepository.update_problem(problem_id, title, problem_definition, input_format, output_format, db)
        if not problem:
            raise HTTPException(status_code=404, detail="Problem not found")
        return problem

    @staticmethod
    async def delete_problem(problem_id: int, db: AsyncSession):
        problem = await QuestionerProblemRepository.delete_problem(problem_id, db)
        if not problem:
            raise HTTPException(status_code=404, detail="Problem not found")
        return problem

    @staticmethod
    async def get_test_cases(problem_id: int, db: AsyncSession):
        problem = await QuestionerProblemRepository.get_problem_by_id(problem_id, db)
        if not problem:
            raise HTTPException(status_code=404, detail="Problem not found")
        return await QuestionerProblemRepository.get_test_cases_by_problem_id(problem_id, db)