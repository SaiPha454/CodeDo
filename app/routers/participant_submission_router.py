from fastapi import APIRouter, Request, Body, Depends, HTTPException, Form
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
from services.code_evaluation_service import CodeEvaluationService
from repositories.participant_testcase_repository import ParticipantTestCaseRepository

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
    submission_status = await UserSubmissionService.get_problem_status(user.id, problem_id, db)  # Fetch submission status

    return templates.TemplateResponse("participant/participant_submission_form.html", {
        "request": request,
        "problem": problem,
        "challenge": challenge,
        "sample_testcases": sample_testcases,
        "submission_status": submission_status  # Pass status to template
    })


@router.get("/{submission_id}/report")
async def get_submission_report(request: Request, submission_id: int, db: AsyncSession = Depends(get_db)):
    user = await AuthLogic.get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)
    # Verify the user's role
    if user.role != UserRole.participant:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    submission = await UserSubmissionService.get_submission_by_id(submission_id, db)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    return templates.TemplateResponse("participant/participant_submission_report.html", {
        "request": request,
        "submission": submission
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

    # Fetch test cases for the problem
    test_cases = await ParticipantTestCaseRepository.get_test_cases(problem_id, db)

    # Evaluate the user's code
    evaluation_results = await CodeEvaluationService.evaluate_code(code, test_cases)

    # Calculate the number of passed test cases
    passed_test_cases = sum(1 for evaluation in evaluation_results if evaluation["result"]["status"] == "Pass")
    total_test_cases = len(test_cases)
    print("=========================================================")
    print(evaluation_results)

    # Save the submission
    submission = await UserSubmissionService.submit_solution(
        user_id=user_id,
        problem_id=problem_id,
        challenge_id=challenge_id,
        code=code,
        total_test_cases=total_test_cases,
        passed_test_cases=passed_test_cases,
        evaluation_results=evaluation_results,
        db=db,
    )
    return {"message": "Submission successful", "submission_id": submission.id}