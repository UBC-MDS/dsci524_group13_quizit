from dsci524_group13_quizit.question_type import QuestionType
import os
import pandas as pd
import pytest

def test_load_questions_empty_csv(quizit_object):
    """Test loading from an empty CSV file."""
    empty_csv_path = "tests/test_data/empty.csv"
    with open(empty_csv_path, "w") as f:
        pass  

    with pytest.raises(ValueError, match="The input file is empty."):
        quizit_object.load_questions(input_file=empty_csv_path)
    
    os.remove(empty_csv_path)  # Clean up

def test_load_questions_empty_dataframe(quizit_object):
    """Test loading from an empty pandas DataFrame."""
    empty_df = pd.DataFrame()
    with pytest.raises(ValueError, match="The input DataFrame cannot be empty."):
        quizit_object.load_questions(questions=empty_df)

def test_load_questions_invalid_file_path(quizit_object):
    """Test loading questions with an invalid file path raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        quizit_object.load_questions(input_file="invalid_path.csv", question_type=QuestionType.MULTIPLE_CHOICE)

def test_load_questions_invalid_file_type(quizit_object, invalid_file_path):
    """Test loading questions with an invalid file type."""
    with pytest.raises(ValueError):
        quizit_object.load_questions(input_file=invalid_file_path, question_type=QuestionType.MULTIPLE_CHOICE)

def test_load_questions_invalid_question_type(quizit_object, shrtq_file_path):
    """Test loading questions with an invalid question type"""
    with pytest.raises(ValueError):
        quizit_object.load_questions(input_file=shrtq_file_path, question_type="essay")

def test_load_questions_missing_question_type(quizit_object, shrtq_file_path):
    """Test loading questions with a missing question type."""
    with pytest.raises(ValueError):
        quizit_object.load_questions(input_file=shrtq_file_path, question_type=None)

def test_load_questions_invalid_question_type(quizit_object, shrtq_file_path):
    """Test loading questions with an invalid question type"""
    with pytest.raises(TypeError):
        quizit_object.load_questions(input_file=shrtq_file_path, question_type=list("New Type"))

def test_load_questions_invalid_dataframe_type(quizit_object):
    """Test loading questions with a list instead of a DataFrame."""
    with pytest.raises(TypeError):
        quizit_object.load_questions(questions=["invalid", "data"], question_type=QuestionType.SHORT_ANSWER)

def test_load_questions_invalid_dataframe_structure(quizit_object):
    """Test loading questions with an invalid dataframe structure."""
    invalid_df = pd.DataFrame({"InvalidColumn": [1, 2, 3]})
    with pytest.raises(ValueError):
        quizit_object.load_questions(questions=invalid_df, question_type=QuestionType.MULTIPLE_CHOICE)

def test_load_questions_invalid_input_file_structure(quizit_object, shrtq_file_path):
    """Test loading questions with an invalid file structure, column length mismatch"""
    with pytest.raises(ValueError):
        quizit_object.load_questions(input_file=shrtq_file_path, question_type=QuestionType.MULTIPLE_CHOICE)

def test_load_questions_invalid_header_names(quizit_object, shrtq_file_path):
    """Test loading questions with an invalid header column names mismatch"""
    valid_df = pd.DataFrame({"questions": ["What continent has the largest population?"], "answers": ["Asia"], "explanations": ["explanation"]})
    with pytest.raises(ValueError, match="The question must follow a specific format. Expected columns"):
        quizit_object.load_questions(questions=valid_df, has_header=True, question_type=QuestionType.SHORT_ANSWER)

def test_load_questions_no_input_or_dataframe(quizit_object):
    """Test loading questions without providing a DataFrame or input file raises an error."""
    with pytest.raises(ValueError):
        quizit_object.load_questions(question_type=QuestionType.SHORT_ANSWER)

def test_load_questions_with_both_input_and_dataframe(quizit_object, shrtq_file_path):
    """Test loading questions with both a dataframe and an input file"""
    valid_df = pd.DataFrame({"question": ["What continent has the largest population?"], "answers": ["Asia"], "explanations": ["explanation"]})
    with pytest.raises(ValueError, match="Please provide either a questions DataFrame or an input file, not both."):
        quizit_object.load_questions(input_file=shrtq_file_path, questions=valid_df, question_type=QuestionType.SHORT_ANSWER)