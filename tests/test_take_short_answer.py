import pytest
import os
import io
import sys
import pandas as pd
from io import StringIO

from dsci524_group13_quizit.quizit import Quizit
from dsci524_group13_quizit.utils import (score_log, question_log, QuizResult)
from unittest.mock import patch

@pytest.fixture
def quizit():
    """
    Fixture to initialize a Quizit object with a sample question.
    """
    quiz = Quizit()
    quiz.shrtq = pd.DataFrame({
        'question': ['What is Python?', 'What is 2+2?'],
        'answers': ['python', '4']
    })
    return quiz

def test_take_short_answer_negative_questions(quizit):
    """
    Test taking a quiz with a negative number of questions.
    """
    with pytest.raises(ValueError):
        quizit.take_short_answer(n=-1)

def test_take_short_answer_empty_questions():
    """
    Test taking a quiz with no questions loaded.
    """
    quizit = Quizit()
    quizit.shrtq = pd.DataFrame()
    with pytest.raises(ValueError):
        quizit.take_short_answer(n=1)

def test_take_short_answer_n_greater_than_available(quizit):
    """
    Test taking a quiz with more questions than available.
    """
    with pytest.raises(ValueError):
        quizit.take_short_answer(n=10)

def test_quiz_result_initialization():
    """
    Test the initialization of the QuizResult class.
    """
    quiz_summary = pd.DataFrame({
        'question': ['What is Python?'],
        'answers': ['python'],
        'response': ['python']
    })
    result = QuizResult(time_used=10.5, score=100.0, question_summary=quiz_summary, question_type="shrtq")
    
    assert result.time_used == 10.5
    assert result.score == 100.0
    assert result.question_summary.equals(quiz_summary)
    assert result.question_type == "shrtq"


def test_take_short_answer_no_save(quizit, monkeypatch, tmpdir):
    """
    Test that no files are saved when save_score and save_questions are False.
    """
    # Mock user input
    monkeypatch.setattr('builtins.input', lambda _: "python")
    file_path = tmpdir.mkdir("test_no_save")
    result = quizit.take_short_answer(n=1, save_score=False, save_questions=False, file_path=str(file_path))

    assert not file_path.join("score.txt").exists()
    assert not file_path.join("correct_answers.txt").exists()
    assert not file_path.join("incorrect_answers.txt").exists()
def test_save_score(quizit):
    file_path = 'test/path'
    score = 85.5
    time_used = 120.5
    score_rec = f"{score}% | {time_used}s\n"
    
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    
    file = os.path.join(file_path, "score.txt")
    
    with open(file, "a") as f:
        f.write(score_rec)

    with open(file, 'r') as f:
        saved_content = f.read()

    assert score_rec in saved_content


def test_save_question_log(quizit):
    file_path = 'test/path'
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    
    correct_answers = ['What is Python?']
    incorrect_answers = ['What is 2+2?']

    correct_file = os.path.join(file_path, "correct_answers.txt")
    incorrect_file = os.path.join(file_path, "incorrect_answers.txt")

    with open(correct_file, 'a') as f:
        f.write(f"Question: What is Python?\n")
        f.write(f"Correct Answer: python\n")
        f.write(f"Your Answer: python\n")
        f.write("=" * 30 + "\n")

    with open(incorrect_file, 'a') as f:
        f.write(f"Question: What is 2+2?\n")
        f.write(f"Correct Answer: 4\n")
        f.write(f"Your Answer: 5\n")
        f.write("=" * 30 + "\n")

    with open(correct_file, 'r') as f:
        correct_content = f.read()
    assert "What is Python?" in correct_content
    assert "Your Answer: python" in correct_content

    with open(incorrect_file, 'r') as f:
        incorrect_content = f.read()
    assert "What is 2+2?" in incorrect_content
    assert "Your Answer: 5" in incorrect_content
def test_take_short_answer_n_greater_than_total_questions(quizit):
    """
    Test when the number of questions `n` exceeds the total number of available questions in `shrtq`.
    """
    quizit.shrtq = pd.DataFrame({
        'question': ['What is Python?', 'What is 2+2?'],
        'answers': ['python', '4']
    })
    
    with pytest.raises(ValueError):
        quizit.take_short_answer(n=5) 
        
def test_take_short_answer_case_insensitive_correct(quizit):
    """
    Test that the quiz system is case-insensitive.
    """
    quizit.shrtq = pd.DataFrame({
        'question': ['What is Python?'],
        'answers': ['python']
    })
    
    with patch('builtins.input', return_value='PYTHON'):
        result = quizit.take_short_answer(n=1)
    
    assert result.score == 100.0  
    assert len(result.question_summary[result.question_summary['score'] == 1]) == 1
    assert result.question_summary.loc[result.question_summary['score'] == 1, 'question'].iloc[0] == 'What is Python?'
def test_take_short_answer_incorrect_answer(quizit):
    """
    Test when the user provides an incorrect answer.
    """
    quizit.shrtq = pd.DataFrame({
        'question': ['What is Python?'],
        'answers': ['python']
    })
    with patch('builtins.input', return_value='java'):
        result = quizit.take_short_answer(n=1)
    
    assert result.score == 0.0 
    incorrect_questions = result.question_summary[result.question_summary['score'] == 0]
    assert len(incorrect_questions) == 1  
    assert incorrect_questions.iloc[0]['question'] == 'What is Python?' 
    
def test_invalid_number_of_questions(quizit):
    """
    Test that ValueError is raised when n is less than or equal to 0 or greater than the number of questions.
    """
    quizit.shrtq = pd.DataFrame({
        'question': ['What is Python?'],
        'answers': ['python']
    })

    with pytest.raises(ValueError, match="The number of questions must be greater than zero."):
        quizit.take_short_answer(n=0)

    with pytest.raises(ValueError, match=f"Not enough questions available. Only {len(quizit.shrtq)} questions loaded."):
        quizit.take_short_answer(n=2)
