from sqlalchemy.ext.asyncio import AsyncSession
from repositories.participant_submission_repository import UserSubmissionRepository
from typing import List, Dict

class UserSubmissionService:
    @staticmethod
    async def submit_solution(user_id: int, problem_id: int, challenge_id: int, code: str, total_test_cases: int, passed_test_cases: int, db: AsyncSession):
        # Determine the status based on passed and total test cases
        status = "Pass" if passed_test_cases == total_test_cases else "Fail"

        # Add or update the submission
        return await UserSubmissionRepository.add_or_update_submission(
            user_id=user_id,
            problem_id=problem_id,
            challenge_id=challenge_id,
            code=code,
            status=status,
            total_test_cases=total_test_cases,
            passed_test_cases=passed_test_cases,
            db=db
        )

    @staticmethod
    async def get_problem_status(user_id: int, problem_id: int, db: AsyncSession) -> Dict:
        submission = await UserSubmissionRepository.get_submission_status(user_id, problem_id, db)
        if not submission:
            return {"status": "Not Submitted", "passed_test_cases": 0, "total_test_cases": 0}

        return {
            "status": submission.status,
            "passed_test_cases": submission.passed_test_cases,
            "total_test_cases": submission.total_test_cases
        }

    @staticmethod
    async def get_challenge_submissions(user_id: int, challenge_id: int, db: AsyncSession) -> List[Dict]:
        submissions = await UserSubmissionRepository.get_submissions_by_challenge(user_id, challenge_id, db)
        return [
            {
                "problem_id": submission.problem_id,
                "status": submission.status,
                "passed_test_cases": submission.passed_test_cases,
                "total_test_cases": submission.total_test_cases
            }
            for submission in submissions
        ]