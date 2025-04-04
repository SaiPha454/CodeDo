from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from config.dbcon import get_db
from services.questioner_challenge_participant_service import QuestionerChallengeParticipantService
from services.questioner_challenge_service import QuestionerChallengeService
from services.user_service import UserService
router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def get_challenge_participant(request: Request, challenge_id: int, db: AsyncSession = Depends(get_db)):
    challenge = await QuestionerChallengeService.get_challenge(challenge_id, db)
    participants = await QuestionerChallengeParticipantService.get_challenge_participants(challenge_id, db)
    return templates.TemplateResponse("questioner/challenge_participants.html", {"request": request, "participants": participants, "challenge": challenge})

@router.get("/{participant_id}/submissions", response_class=HTMLResponse)
async def get_participant_submissions(request: Request, participant_id: int, challenge_id: int, db: AsyncSession = Depends(get_db)):
    print("User===============>", participant_id)
    challenge = await QuestionerChallengeService.get_challenge(challenge_id, db)
    submissions = await QuestionerChallengeParticipantService.get_challenge_participant_submissions(challenge_id, participant_id, db)
    participant = await UserService.get_user_by_id(participant_id, db)
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    return templates.TemplateResponse("questioner/participant_submissions.html", {"request": request, "submissions": submissions, "challenge": challenge, "participant": participant})