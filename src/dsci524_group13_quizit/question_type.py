from enum import Enum

class QuestionType(Enum):
    """
    A class for the different types of questions. Inherits from the Enum Class

    Attributes
    ----------
        MULTIPLE_CHOICE (str): Represents a multiple choice question type.
        SHORT_ANSWER (str): Represents a short answer question type.
    """
    
    MULTIPLE_CHOICE = "multiple choice"
    SHORT_ANSWER = "short answer"

MCQ_COLUMNS = ["question","options","answers","explanations"]
SHRTQ_COLUMNS = ["question","answers","explanations"]

QUESTION_COLUMN_MAPPING = {
    QuestionType.MULTIPLE_CHOICE: MCQ_COLUMNS,
    QuestionType.SHORT_ANSWER: SHRTQ_COLUMNS
}