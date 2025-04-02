from repositories.participant_testcase_repository import ParticipantTestCaseRepository
from sqlalchemy.ext.asyncio import AsyncSession

class ParticipantTestcaseService:

    @staticmethod
    async def get_test_cases(problem_id: int, db: AsyncSession):
        """
        Fetch all test cases for a given problem.
        """
        return await ParticipantTestCaseRepository.get_test_cases(problem_id, db)

    @staticmethod
    async def get_sample_test_cases(problem_id: int, db: AsyncSession):
        """
        Fetch the first two test cases for a given problem.
        """
        return await ParticipantTestCaseRepository.get_first_two_test_cases(problem_id, db)