from fastapi import FastAPI
from pydantic import BaseModel
from agents.interview_simulator import InterviewSimulator
from agents.qualitative_assessor import QualitativeAssessor
from agents.quantitative_assessor import QuantitativeAssessor
from agents.meta_reviewer import MetaReviewer  # new import

app = FastAPI()

interview_agent = InterviewSimulator()
qualitative_assessor = QualitativeAssessor()
quantitative_assessor = QuantitativeAssessor()
meta_reviewer = MetaReviewer()  # new instance

class InterviewRequest(BaseModel):
    topic: str

class AssessRequest(BaseModel):
    interview: str

class QuantitativeRequest(BaseModel):
    interview: str

class MetaReviewRequest(BaseModel):  # new request model
    interview: str
    qualitative_assessment: str
    quantitative_assessment: str

@app.post("/simulate")
def simulate_interview(request: InterviewRequest):
    result = interview_agent.simulate(request.topic)
    return {"conversation": result}

@app.post("/assess")
def qualitative_assessment(request: AssessRequest):
    result = qualitative_assessor.assess(request.interview)
    return {"assessment": result}

@app.post("/quantify")
def quantitative_assessment(request: QuantitativeRequest):
    result = quantitative_assessor.assess(request.interview)
    return {"quantitative_assessment": result}

@app.post("/meta_review")  # new endpoint
def meta_review(request: MetaReviewRequest):
    result = meta_reviewer.review(
        request.interview,
        request.qualitative_assessment,
        request.quantitative_assessment
    )
    return {"diagnostic_suggestion": result}
