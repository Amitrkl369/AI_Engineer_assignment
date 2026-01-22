from pydantic import BaseModel, Field
from typing import Optional, List

class FieldValue(BaseModel):
    value: Optional[str] = None
    confidence: float = 0.0

class CandidateDetails(BaseModel):
    name: FieldValue = Field(default_factory=FieldValue)
    father_name: FieldValue = Field(default_factory=FieldValue)
    mother_name: FieldValue = Field(default_factory=FieldValue)
    roll_no: FieldValue = Field(default_factory=FieldValue)
    registration_no: FieldValue = Field(default_factory=FieldValue)
    dob: FieldValue = Field(default_factory=FieldValue)
    exam_year: FieldValue = Field(default_factory=FieldValue)
    board: FieldValue = Field(default_factory=FieldValue)
    institution: FieldValue = Field(default_factory=FieldValue)

class SubjectMark(BaseModel):
    subject: FieldValue = Field(default_factory=FieldValue)
    max_marks: FieldValue = Field(default_factory=FieldValue)
    obtained_marks: FieldValue = Field(default_factory=FieldValue)
    grade: Optional[FieldValue] = None

class MarksheetOutput(BaseModel):
    candidate: CandidateDetails
    subjects: List[SubjectMark] = []
    overall_result: FieldValue = Field(default_factory=FieldValue)
    issue_date: Optional[FieldValue] = None
    issue_place: Optional[FieldValue] = None
    confidence_explanation: Optional[str] = None
    raw_text: Optional[str] = None
