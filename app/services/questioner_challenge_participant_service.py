from sqlalchemy.ext.asyncio import AsyncSession
from repositories.questioner_challenge_repository import QuestionerChallengeRepository
from repositories.participant_submission_repository import ParticipantSubmissionRepository
from services.questioner_problem_service import QuestionerProblemService
from services.participant_submission_service import UserSubmissionService
from repositories.participant_submission_model import SubmissionStatus
from services.user_service import UserService

class QuestionerChallengeParticipantService:
    @staticmethod
    async def get_challenge_participants(challenge_id: int, db: AsyncSession):
        # Fetch participants for the challenge using the updated repository method
        participants = await QuestionerChallengeRepository.get_participants_by_challenge(challenge_id, db)
        problems = await QuestionerProblemService.get_problems(challenge_id, db)
        
        total_problems = len(problems)
        # Add submission details for each participant
        detailed_participants = []
        for participant in participants:
            submissions = await ParticipantSubmissionRepository.get_submissions_by_challenge(participant.id, challenge_id, db)
            
            total_submissions = len(submissions)
            last_submission_time = max((submission.submitted_at for submission in submissions), default=None)

            detailed_participants.append({
                "name": participant.username,  # Corrected from name to username
                "student_id": participant.email,  # Corrected from user_id to id
                "last_submission_time": last_submission_time.strftime('%Y-%m-%d %H:%M:%S') if last_submission_time else None,
                "total_problems": total_problems,
                "total_submissions": total_submissions,
                "user_id": participant.id  # Corrected from user_id to id
            })

        return detailed_participants
    
    @staticmethod
    async def get_challenge_participant_submissions(challenge_id: int, participant_id: int, db: AsyncSession):
        submissions = await UserSubmissionService.get_submissions_by_challenge_and_participant(participant_id, challenge_id, db)
        problems = await QuestionerProblemService.get_problems(challenge_id, db)
        problem_dict = {problem.id: problem for problem in problems}


        return [
            {
                "id": submission.id,
                "language": "Python",
                "problem_id": submission.problem_id,
                "status": "Pass" if submission.status == SubmissionStatus.Pass else "Fail",
                "challenge_id": submission.challenge_id,
                "participant_id": submission.user_id,
                "passed_test_cases": submission.passed_test_cases,
                "total_test_cases": submission.total_test_cases,
                "submitted_at": submission.submitted_at.strftime("%Y-%m-%d %I:%M %p") if submission.submitted_at else None,
                "problem_title": problem_dict[submission.problem_id].title if submission.problem_id in problem_dict else None
            }
            for submission in submissions
        ]
        