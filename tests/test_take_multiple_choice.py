import pytest
import sys
import os
import pandas as pd
import numpy as np
from io import StringIO
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from dsci524_group13_quizit.take_multiple_choice import Quizit
from dsci524_group13_quizit.utils import (
    select_questions, print_question, prompt_input, input_check, 
    mcq_score, score_log, question_log, QuizResult
)



@pytest.fixture
def sample_mcq():
    """Sample DataFrame fixture for testing"""
    return pd.DataFrame({
    "question": ["Question 1?", "Question 2?" , "Question 3?", "Question 4?", "Question 5?"], 
    "options": [["option1", "option2", "option3", "option4"], ["option1", "option2", "option3", "option4", "option5"], ["option1", "option2"], ["option1", "option2", "option3", "option4"], ["option1", "option2", "option3"]],
    "answers": [["option1"], ["option1", "option2", "option3"], ["option1"], ["option1", "option2"], ["option3", "option2"]],
    "explanations" :["explanation1", "explanation2", "explanation3", "explanation4", "explanation5"]
})


def test_select_questions(sample_mcq):
    """
    1. Test if select_question fucntion selectes questions without replacement and returns a DataFrame with correct length.
    2. Test if select_question function returns all questions if n > number of questions available.
    """
    # Test 1
    n, quiz = select_questions(sample_mcq, 3)
    assert n == 3
    assert quiz.shape == (3, 4)
    assert isinstance(quiz, pd.DataFrame)
    assert any(quiz.duplicated(subset=["question", "explanations"])) == False

    # Test 2
    n, quiz = select_questions(sample_mcq, 10)
    assert n == 5
    assert quiz.shape == (5, 4)
    assert isinstance(quiz, pd.DataFrame)
    assert any(quiz.duplicated(subset=["question", "explanations"])) == False

def test_prompt_input(monkeypatch):
    """Test if prompt_input function prompts users for input and return it"""
    mock_response = StringIO("A")
    monkeypatch.setattr('sys.stdin', mock_response)
    assert prompt_input() == "A"


def test_print_question(sample_mcq):
    """
    1. Test if the print_question function returns correct list and dictionary of print_q=True
    2. Test if the print_question function returns a string containing the question and its options if print_q = False
    """
    question = sample_mcq.iloc[0]
    n_options, options_dict = print_question(question, iter=0, print_q=True)
    assert n_options == ["A", "B", "C", "D"]
    assert options_dict == {"A": "option1", "B": "option2", "C": "option3", "D": "option4"}

    q_str = print_question(question, iter=0, print_q=False)
    assert q_str == 'Question 1?\nA : option1\nB : option2\nC : option3\nD : option4\n'
 

def test_input_check():
    """Test the input_check function for correct validation of user input and handling of invalid cases """
    n_options = ["A", "B", "C"]
    valid_input = ["A", ", c , A , b, "]
    
    # Validate Valid input
    user_input, valid, message = input_check(valid_input[0], n_options, count=1)
    assert valid is True
    assert user_input == ["A"]
    assert message == f"Your Answer: {['A']}"

    user_input, valid, message = input_check(valid_input[1], n_options, count=1)
    assert valid is True
    assert user_input == ["C", "A", "B"]
    assert message == f"Your Answer: {['C', 'A', 'B']}"
    
    # Handling Invalid input
    invalid_input = ["1, a, b, #", "", "D, "]

    user_input, valid, message = input_check(invalid_input[0], n_options, count=1)
    assert valid is False
    assert user_input == "1, a, b, #"
    assert "Please select a valid option from the given choices." in message

    user_input, valid, message = input_check(invalid_input[1], n_options, count=2)
    assert valid is False
    assert user_input == ""
    assert "Please select a valid option from the given choices." in message

    user_input, valid, message = input_check(invalid_input[2], n_options, count=3)
    assert valid is True
    assert user_input == ""
    assert "Maximum attempts reached" in message

def test_mcq_score(sample_mcq):
    """Test if mcq_score function returns correct score based on user's response"""
    options_dict = {"A": "option1", "B": "option2", "C": "option3", "D": "option4", "E": "option5"}
    question = sample_mcq.iloc[1]

    # Correct answer
    score = mcq_score(options_dict, question, ["C", "A", "B"])
    assert score == 1.0

    # Partially correct answer
    score = mcq_score(options_dict, question, ["A", "B", "D"])
    assert score == 0.60

    score = mcq_score(options_dict, question, ["D"])
    assert score == 0.2

    # Incorrect answer
    score = mcq_score(options_dict, question, ["D", "E"])
    assert score == 0.0


def test_take_multiple_choice_no_questions():
    """Test that the take_multiple_choice method raises an error if no questions are loaded."""
    quiz = Quizit()
    with pytest.raises(ValueError, match="No multiple-choice questions loaded."):
        quiz.take_multiple_choice(2)

def test_take_multiple_choice_invalid_arguments(sample_mcq):
    """Test if the take_multiple_choice method raises errors for invalid arguments."""
    quiz = Quizit()
    quiz.mcq = sample_mcq

    # Invalid save_questions
    with pytest.raises(TypeError, match="Invalid value for 'save_questions'"):
        quiz.take_multiple_choice(2, save_questions="invalid")

    # Invalid save_score
    with pytest.raises(TypeError, match="Invalid value for 'save_score'"):
        quiz.take_multiple_choice(2, save_score="invalid")

    # Invalid n
    with pytest.raises(TypeError, match="Invalid value for 'n'"):
        quiz.take_multiple_choice("two")
        quiz.take_multiple_choice(-1)
    
    sample_mcq["options"] = [[], [], [], [], []]
    quiz.mcq = sample_mcq
    with pytest.raises(ValueError, match="No valid multiple-choice questions are available"):
        quiz.take_multiple_choice(1)

def test_score_log():
    """Tests the score_log function for correct file creation, logging, and handling of save options."""
    path = os.path.join("tests", "score.txt")
    if os.path.exists(path):
        os.remove(path)
    
    score_log(0.7, 12, save_score=False, file_path="tests")
    assert not os.path.exists(path)

    score_log(0.8, 10.5, save_score=True, file_path="tests")
    score_log(0.7, 12, save_score=True, file_path="tests")
    assert os.path.exists(path)
    with open(path, "r") as f:
        content = f.read()
    assert "Date                      | Score    |Time Used (s)" in content
    assert "80%" in content
    assert "10.5" in content
    assert "70%" in content
    assert "12" in content

    if os.path.exists(path):
        os.remove(path)
    

def test_question_log(sample_mcq):
    """Tests the question_log function for correct filtering and logging of questions."""
    # Create Test Data
    sample_mcq["response"] = [["A"], ["B", "E"], ["B"], ["A", "B", "D"], ["B", "C"]]
    sample_mcq["score"] = [1.0, 0.6, 0.0, 0.75, 1.0]
    files = ["all.txt", "incorrect.txt", "correct.txt"]

    # Remove existing test files
    for f in files:
        path = os.path.join("tests", f)
        if os.path.exists(path):
            os.remove(path)
    
    # Test for save_question="all"
    path = os.path.join("tests", "all.txt")
    quiz = question_log(False, sample_mcq, file_path="tests")
    assert quiz.shape == (5, 6)
    assert not os.path.exists(path)

    quiz = question_log("all", sample_mcq.iloc[0:2], file_path="tests")
    assert quiz.shape == (2, 6)

    quiz = question_log("all", sample_mcq.iloc[[2]], file_path="tests")
    assert os.path.exists(path)
    with open(path, "r") as f:
        content = f.read()
    assert "Question 1?" in content
    assert "Question 2?" in content
    assert "Question 3?" in content
    assert "Your Answer:" in content    
    assert "Correct Answer:" in content
    assert "Explanations:" in content

    # Test for save_question="incorrect"
    path = os.path.join("tests", "incorrect.txt")
    quiz = question_log("incorrect", sample_mcq.iloc[[0]], file_path="tests")
    assert os.path.exists(path)
    assert os.path.getsize(path) == 0
    assert quiz.shape == (0, 6)
    
    quiz = question_log("incorrect", sample_mcq.iloc[0:2], file_path="tests")
    assert quiz.shape == (1, 6)

    quiz = question_log("incorrect", sample_mcq.iloc[3:5], file_path="tests")
    with open(path, "r") as f:
        content = f.read()
    assert "Question 1?" not in content
    assert "Question 2?" in content
    assert "Question 4?" in content
    assert "Question 5?" not in content

    # Test for save_question="correct"
    path = os.path.join("tests", "correct.txt")
    quiz = question_log("correct", sample_mcq.iloc[[1]], file_path="tests")
    assert os.path.exists(path)
    assert os.path.getsize(path) == 0
    assert quiz.shape == (0, 6)

    quiz = question_log("correct", sample_mcq.iloc[0:2], file_path="tests")
    assert quiz.shape == (1, 6)

    quiz = question_log("correct", sample_mcq.iloc[3:5], file_path="tests")
    with open(path, "r") as f:
        content = f.read()
    assert "Question 1?" in content
    assert "Question 2?" not in content
    assert "Question 4?" not in content
    assert "Question 5?" in content

    # Clean up test files
    for f in files:
        path = os.path.join("tests", f)
        if os.path.exists(path):
            os.remove(path)


def test_quiz_result_class(sample_mcq):
    """Tests the QuizResult class for correct initialization and attribute storage."""
    sample_mcq["response"] = [["A"], ["B", "E"], ["B"], ["A", "B", "D"], ["B", "C"]]
    sample_mcq["score"] = [1.0, 0.6, 0.0, 0.75, 1.0]
    result = QuizResult(time_used=15.3, score=0.85, question_summary=sample_mcq)
    assert result.time_used == 15.3
    assert result.score == 0.85
    assert result.question_summary.shape == sample_mcq.shape

def test_take_multiple_choice_quiz(sample_mcq, monkeypatch):
    """Tests the take_multiple_choice method for functionality, result generation, and file logging."""
    files = ["score.txt", "all.txt", "incorrect.txt", "correct.txt"]

    # Remove existing test files
    for f in files:
        path = os.path.join("tests", f)
        if os.path.exists(path):
            os.remove(path)

    quiz = Quizit()
    quiz.mcq = sample_mcq
    
    mock_response = StringIO("A\nB\nF\nF\nF")
    monkeypatch.setattr('sys.stdin', mock_response)
    result = quiz.take_multiple_choice(3, save_questions="all", save_score=True, file_path="tests")

    assert isinstance(result, QuizResult)
    assert result.time_used >= 0
    assert 0 <= result.score <= 1
    assert result.question_summary is not None
    assert os.path.exists(os.path.join("tests", "score.txt"))
    assert os.path.exists(os.path.join("tests", "all.txt"))
    assert not os.path.exists(os.path.join("tests", "correct.txt"))
    assert not os.path.exists(os.path.join("tests", "incorrect.txt"))

    # Clean up created test files
    for f in files:
        path = os.path.join("tests", f)
        if os.path.exists(path):
            os.remove(path)
