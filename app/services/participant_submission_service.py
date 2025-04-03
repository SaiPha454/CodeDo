from sqlalchemy.ext.asyncio import AsyncSession
from repositories.participant_submission_repository import ParticipantSubmissionRepository
from typing import List, Dict
from repositories.participant_submission_model import SubmissionStatus
from fastapi import HTTPException


class UserSubmissionService:
    @staticmethod
    async def submit_solution(user_id: int, problem_id: int, challenge_id: int, code: str, total_test_cases: int, passed_test_cases: int, evaluation_results , db: AsyncSession):
        # Determine the status based on passed and total test cases
        status = SubmissionStatus.Pass if passed_test_cases == total_test_cases else SubmissionStatus.Fail

        # Add or update the submission
        return await ParticipantSubmissionRepository.add_or_update_submission(
            user_id=user_id,
            problem_id=problem_id,
            challenge_id=challenge_id,
            code=code,
            status=status,
            total_test_cases=total_test_cases,
            passed_test_cases=passed_test_cases,
            evaluation_results=evaluation_results,
            db=db
        )

    @staticmethod
    async def get_submission_by_id(submission_id: int, db: AsyncSession):
        # Fetch the submission by ID from the repository
        submission = await ParticipantSubmissionRepository.get_submission_by_id(submission_id, db)
        if not submission:
            raise HTTPException(status_code=404, detail="Submission not found")
        return {
            "submission_id": submission.id,
            "user_id": submission.user_id,
            "problem_id": submission.problem_id,
            "challenge_id": submission.challenge_id,
            "code": submission.code,
            "status": submission.status,
            "total_test_cases": submission.total_test_cases,
            "passed_test_cases": submission.passed_test_cases,
            "evaluation_results": submission.evaluation_results
        }

    @staticmethod
    async def get_problem_status(user_id: int, problem_id: int, db: AsyncSession) -> Dict:
        submission = await ParticipantSubmissionRepository.get_submission_status(user_id, problem_id, db)
        if not submission:
            return {"status": "Not Submitted", "passed_test_cases": 0, "total_test_cases": 0}

        return {
            "status": "Pass" if submission.status == SubmissionStatus.Pass else "Fail",
            "passed_test_cases": submission.passed_test_cases,
            "total_test_cases": submission.total_test_cases,
        }

    @staticmethod
    async def get_challenge_submissions(user_id: int, challenge_id: int, db: AsyncSession) -> List[Dict]:
        submissions = await ParticipantSubmissionRepository.get_submissions_by_challenge(user_id, challenge_id, db)
        return [
            {
                "problem_id": submission.problem_id,
                "status": submission.status,
                "passed_test_cases": submission.passed_test_cases,
                "total_test_cases": submission.total_test_cases
            }
            for submission in submissions
        ]