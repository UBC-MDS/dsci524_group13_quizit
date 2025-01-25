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
    
    path = os.path.join("temp", "score_mcq.txt")
    if os.path.exists(path):
        os.remove(path)
    if os.path.exists("temp"):
        os.rmdir("temp")
    
    score_log(70, 12, save_score=False, question_type="mcq", dir_name="temp")
    assert not os.path.exists(path)

    score_log(80, 10.5, save_score=True, question_type="mcq",dir_name="temp")
    score_log(70.23, 12, save_score=True, question_type="mcq", dir_name="temp")
    assert os.path.exists(path)
    with open(path, "r") as f:
        content = f.read()
    assert "|Time Used (s)" in content
    assert "80%" in content
    assert "10.5" in content
    assert "70.23%" in content
    assert "12" in content

    if os.path.exists(path):
        os.remove(path)
    

def test_question_log(sample_mcq):
    """Tests the question_log function for correct filtering and logging of questions."""
    # Create Test Data
    sample_mcq["response"] = [["A"], ["B", "E"], ["B"], ["A", "B", "D"], ["B", "C"]]
    sample_mcq["score"] = [1.0, 0.6, 0.0, 0.75, 1.0]
    path_wrg = os.path.join("temp", "incorrect_mcq.txt")
    path_rt = os.path.join("temp", "correct_mcq.txt")
    
    # Remove existing test files

    if os.path.exists(path_wrg):
        os.remove(path_wrg)
    if os.path.exists(path_rt):
        os.remove(path_rt)
    if os.path.exists("temp"):
        os.rmdir("temp")

    # Test for save_question=False
    question_log(type=False, quiz=sample_mcq, question_type="mcq", dir_name="temp")
    assert not os.path.exists(path_wrg)
    assert not os.path.exists(path_rt)

    # Test for save_question="incorrect"
    question_log(type="incorrect", quiz=sample_mcq.iloc[[4]], question_type="mcq", dir_name="temp")
    assert os.path.exists(path_wrg)
    assert os.path.getsize(path_wrg) == 0
    os.remove(path_wrg)

    question_log(type="incorrect", quiz=sample_mcq.iloc[0:2], question_type="mcq", dir_name="temp")
    question_log(type="incorrect", quiz=sample_mcq.iloc[[3]], question_type="mcq", dir_name="temp")
    with open(path_wrg, "r") as f:
        content = f.read()
    assert "Question 2?" in content
    assert "Question 4?" in content
    assert "Question 1?" not in content
    assert "Your Answer:" in content    
    assert "Correct Answer:" in content
    assert "Explanations:" in content
    
  # Test for save_question="correct"
    question_log("correct", sample_mcq.iloc[[1]],question_type="mcq", dir_name="temp")
    assert os.path.getsize(path_rt) == 0

    question_log("correct", sample_mcq.iloc[0:2],question_type="mcq", dir_name="temp")
    question_log("correct", sample_mcq.iloc[[4]],question_type="mcq", dir_name="temp")
    with open(path_rt, "r") as f:
        content = f.read()
    assert "Question 1?" in content
    assert "Question 2?" not in content
    assert "Question 5?" in content
    assert "Your Answer:" in content    
    assert "Correct Answer:" in content
    assert "Explanations:" in content

    # Test for save_question="all"
    if os.path.exists(path_wrg):
        os.remove(path_wrg)
    if os.path.exists(path_rt):
        os.remove(path_rt)
    question_log(type="all", quiz=sample_mcq.iloc[0:3], question_type="mcq", dir_name="temp")
    assert os.path.exists(path_wrg)
    assert os.path.exists(path_rt)

    # Clean up test files
    if os.path.exists(path_wrg):
        os.remove(path_wrg)
    if os.path.exists(path_rt):
        os.remove(path_rt)
    if os.path.exists("temp"):
        os.rmdir("temp")


def test_quiz_result_class(sample_mcq):
    """Tests the QuizResult class for correct initialization and attribute storage."""
    sample_mcq["response"] = [["A"], ["B", "E"], ["B"], ["A", "B", "D"], ["B", "C"]]
    sample_mcq["score"] = [1.0, 0.6, 0.0, 0.75, 1.0]
    result = QuizResult(time_used=15.3, score=0.85, question_summary=sample_mcq, question_type="mcq")
    assert result.time_used == 15.3
    assert result.score == 0.85
    assert result.question_summary.shape == sample_mcq.shape

def test_take_multiple_choice_quiz(sample_mcq, monkeypatch):
    """Tests the take_multiple_choice method for functionality, result generation, and file logging."""
    files = ["score_mcq.txt", "incorrect_mcq.txt", "correct_mcq.txt"]

    # Remove existing test files
    for f in files:
        path = os.path.join("temp", f)
        if os.path.exists(path):
            os.remove(path)
    if os.path.exists("temp"):
        os.rmdir("temp")

    quiz = Quizit()
    quiz.mcq = sample_mcq
    
    mock_response = StringIO("A\nB\nF\nF\nF")
    monkeypatch.setattr('sys.stdin', mock_response)
    result = quiz.take_multiple_choice(3, save_questions="all", save_score=True, file_path="temp")

    assert isinstance(result, QuizResult)
    assert result.time_used >= 0
    assert 0 <= result.score <= 100
    assert result.question_summary is not None
    assert os.path.exists(os.path.join("temp", "score_mcq.txt"))
    assert os.path.exists(os.path.join("temp", "correct_mcq.txt"))
    assert os.path.exists(os.path.join("temp", "incorrect_mcq.txt"))

    # Clean up created test files
    for f in files:
        path = os.path.join("temp", f)
        if os.path.exists(path):
            os.remove(path)
    os.rmdir("temp")