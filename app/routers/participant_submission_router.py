from fastapi import APIRouter, Request, Body, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from config.dbcon import get_db
from services.participant_submission_service import UserSubmissionService
from services.participant_problem_service import ParticipantProblemService
from services.participant_challenge_service import ParticipantChallengeService
from services.participant_testcase_service import ParticipantTestcaseService
from fastapi.templating import Jinja2Templates
from services.auth_service import AuthLogic
from repositories.user_model import UserRole

router = APIRouter(prefix="/participants/submissions", tags=["participants"])
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def get_submission_form(request: Request, problem_id: int, challenge_id: int, db: AsyncSession = Depends(get_db)):
    
    user = await AuthLogic.get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)
    # Verify the user's role
    if user.role != UserRole.participant:
        raise HTTPException(status_code=403, detail="Forbidden")
    problem = await ParticipantProblemService.get_problem_detail(user.id, problem_id, db)
    challenge = await ParticipantChallengeService.get_challenge_by_id(challenge_id, db)
    sample_testcases = await ParticipantTestcaseService.get_sample_test_cases(problem_id, db)
    return templates.TemplateResponse("participant/participant_submission_form.html", {
        "request": request,
        "problem": problem,
        "challenge": challenge,
        "sample_testcases": sample_testcases
    })

@router.post("/")
async def submit_solution(
    request: Request,
    problem_id: int = Body(...),
    challenge_id: int = Body(...),
    code: str = Body(...),
    db: AsyncSession = Depends(get_db)
):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    problem = await ParticipantProblemService.get_problem(problem_id, db) 
    challenge = await ParticipantChallengeService.get_challenge_by_id(challenge_id, db) 
    testcases = await ParticipantTestcaseService.get_test_cases(problem_id, db)

    # Evaluate the code

    print("Code : ===========>")
    print(code)

    # total_test_cases = 1
    # passed_test_cases = 2
    # await UserSubmissionService.submit_solution(
    #     user_id=user_id,
    #     problem_id=problem_id,
    #     challenge_id=challenge_id,
    #     code=code,
    #     total_test_cases=total_test_cases,
    #     passed_test_cases=passed_test_cases,
    #     db=db
    # )
    return {"submission_id":1}
    # return RedirectResponse(url=f"/participants/challenges/{challenge_id}", status_code=302)