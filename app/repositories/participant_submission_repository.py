from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from repositories.participant_submission_model import UserSubmission
import datetime
class ParticipantSubmissionRepository:
    @staticmethod
    async def add_or_update_submission(user_id: int, problem_id: int, challenge_id: int, code: str, status: str, total_test_cases: int, passed_test_cases: int, evaluation_results , db: AsyncSession):
        try:
            # Check if a submission already exists
            result = await db.execute(
                select(UserSubmission).where(
                    UserSubmission.user_id == user_id,
                    UserSubmission.problem_id == problem_id
                )
            )
            submission = result.scalars().first()

            if submission:
                # Update existing submission
                submission.code = code
                submission.status = status
                submission.total_test_cases = total_test_cases
                submission.passed_test_cases = passed_test_cases
                submission.evaluation_results = evaluation_results
                submission.submitted_at = datetime.datetime.now()
            else:
                # Add new submission
                submission = UserSubmission(
                    user_id=user_id,
                    problem_id=problem_id,
                    challenge_id=challenge_id,
                    code=code,
                    status=status,
                    total_test_cases=total_test_cases,
                    passed_test_cases=passed_test_cases,
                    evaluation_results=evaluation_results,
                )
                db.add(submission)

            await db.commit()
            return submission
        except SQLAlchemyError as e:
            await db.rollback()
            raise e


    @staticmethod
    async def get_submission_by_id(submission_id: int, db: AsyncSession):
        result = await db.execute(
            select(UserSubmission).where(UserSubmission.id == submission_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_submission_status(user_id: int, problem_id: int, db: AsyncSession):
        result = await db.execute(
            select(UserSubmission).where(
                UserSubmission.user_id == user_id,
                UserSubmission.problem_id == problem_id
            )
        )
        return result.scalars().first()

    @staticmethod
    async def get_submissions_by_challenge(user_id: int, challenge_id: int, db: AsyncSession):
        result = await db.execute(
            select(UserSubmission).where(
                UserSubmission.user_id == user_id,
                UserSubmission.challenge_id == challenge_id
            )
        )
        return result.scalars().all()