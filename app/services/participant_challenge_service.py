from sqlalchemy.ext.asyncio import AsyncSession
from repositories.participant_challenge_repository import ParticipantChallengeRepository
from repositories.participant_submission_repository import ParticipantSubmissionRepository
from fastapi import HTTPException
from typing import List, Dict
from repositories.participant_submission_model import SubmissionStatus

class ParticipantChallengeService:
    @staticmethod
    async def get_participant_challenges(participant_id: int, db: AsyncSession) -> List[Dict]:
        # Fetch challenges for the participant from the repository
        rows = await ParticipantChallengeRepository.get_challenges_by_participant(participant_id, db)

        # Serialize the results into dictionaries
        challenges = [
            {
                "challenge_id": challenge.id,
                "title": challenge.title,
                "created_at": challenge.created_at.strftime("%Y-%m-%d %I:%M %p") if challenge.created_at else None,
                "created_by": challenge.created_by,
                "num_problems": len(challenge.problems) if challenge.problems else 0,
            }
            for _, challenge in rows
        ]

        return challenges

    @staticmethod
    async def get_challenge_details( user_id: int, challenge_id: int,db: AsyncSession):
        # Fetch the challenge and its problems from the repository
        challenge = await ParticipantChallengeRepository.get_challenge_with_problems(challenge_id, db)
        if not challenge:
            return None
        submissions = await ParticipantSubmissionRepository.get_submissions_by_challenge(user_id, challenge_id, db)
        submitted_problems = {submission.problem_id: submission for submission in submissions}
        # Serialize the challenge details with submission statuses
        return {
            "challenge_id": challenge.id,
            "title": challenge.title,
            "created_at": challenge.created_at.strftime("%Y-%m-%d %I:%M %p") if challenge.created_at else None,
            "created_by": challenge.created_by,  # Ensure this exists in the Challenge model
            "problems": [
                {
                    "problem_id": problem.id,
                    "title": problem.title,
                    "problem_definition": problem.problem_definition,
                    "input_format": problem.input_format,
                    "output_format": problem.output_format,
                    "submission_status": None if problem.id not in submitted_problems else "Pass" if submitted_problems[problem.id].status == SubmissionStatus.Pass else "Fail",
                }
                for problem in challenge.problems
            ],
        }

    @staticmethod
    async def get_challenge_by_id(challenge_id: int, db: AsyncSession):
        # Fetch the challenge by ID from the repository
        challenge = await ParticipantChallengeRepository.get_challenge_by_id(challenge_id, db)
        if not challenge:
            raise HTTPException(status_code=404, detail="Challenge not found")
        return challenge