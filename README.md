# dsci524_group13_quizit
[![Documentation Status](https://readthedocs.org/projects/dsci524-group13-quizit/badge/?version=latest)](https://dsci524-group13-quizit.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/UBC-MDS/dsci524_group13_quizit/graph/badge.svg?token=788HY26XUG)](https://codecov.io/gh/UBC-MDS/dsci524_group13_quizit)

A python package for creating and taking quizzes.

## Summary
### Project Summary
This Python package is designed to help users to create custom build quizzes.
The package allows users to load multiple-choice and/or short-answer question sets.
It will then randomly select a user-defined number of questions from the question sets and generate a quiz.
Quiz scores and time used will be displayed at the end of the quiz.
Optionally, users can also have their quiz scores and incorrect and correct questions in a text file. 

### Package Functions

The package consists of three classes: 
1. `Quizit` —— The main class for creating and taking quizzes. This class has three methods:

- `load_questions` —— Allow users to load in their own multiple-choice or short answer question sets 

    ```python
    load_questions(questions: pd.DataFrame = None, input_file: str = None, question_type: QuestionType = None, has_header: bool = True, delimeter: str = None)
    ```

- `take_multiple_choice` —— Allow users to take a multiple-choice quiz with optional result tracking.

    ```python
    take_multiple_choice(n, save_questions=False, save_score=False, file_path=False)
    ```

- `take_short_answer` —— Allow users to take a short answer quiz with optional result tracking.

    ```python
    take_short_answer(n, save_questions=False, save_score=False, file_path=False)
    ```
2. `QuestionType` —— This class is used in `load_questions` to specify the type of quiz questions (multiple-choice or short-answer). 

3. `QuizResult` —— This class stores the quiz results returned by the `take_multiple_choice` and `take_short_answer` functions. It includes the score, time used, question summary and question type of the quiz.

 

### Python Ecosystem Integration

`dsci524_group13_quizit` is a fantastic tool for both educators and learners, providing a seamless way to create and take quizzes. Unlike other Python packages such as [`quizzer`](https://pypi.org/project/quizzer/) and [`QuizzingPackage`](https://pypi.org/project/QuizzingPackage/), this package stands out by supporting both multiple-choice and short answer formats. Additionally, it offers the unique feature of saving quiz results to a text file, making it an invaluable resource for tracking progress and performance. 
Whether you're teaching a class or studying for an exam, `dsci524_group13_quizit` is designed to make the quiz experience as smooth and effective as possible.


## Installation

```bash
$ pip install dsci524_group13_quizit
```

## Documentation
To learn more about interacting with this package visit the [online documentation](https://dsci524-group13-quizit.readthedocs.io/en/latest/).

## Usage
Below are outlined steps on how to interact with this package as a user. The tutorial assumes you are using Python and have already installed the package.
1. **Import the package and necessary modules:**
    ```python
    from dsci524_group13_quizit import Quizit, QuestionType
    ```

2. **Load your question sets:** ensure the file paths exist
    ```python
    mcq_file_path = "tests/test_data/multiple_choice.csv"
    shrtq_file_path = "tests/test_data/short_answer.csv"
    

    quiz = Quizit()
    mc_questions = quiz.load_questions(input_file=mcq_file_path, question_type=QuestionType.MULTIPLE_CHOICE, delimeter=";")
    shrt_questions = quiz.load_questions(input_file=shrtq_file_path, question_type=QuestionType.SHORT_ANSWER, delimeter=";")
    ```

3. **Take a multiple-choice quiz:**
    ```python
    quiz.take_multiple_choice(n=1)
    ```

4. **Take a short-answer quiz:**
    ```python
    quiz.take_short_answer(n=1)
    ```

These steps will guide you through the basic usage of the `dsci524_group13_quizit` package. For more detailed information, refer to the [online documentation](https://dsci524-group13-quizit.readthedocs.io/en/latest/).


## Contributors

Mavis Wong([@MavisWong295](https://github.com/MavisWong295)), Shangjia Yu([@shangjiayuu](https://github.com/shengjiayuu)), Sopuruchi Chisom([@cs-uche](https://github.com/cs-uche))

## Contributing

Interested in contributing? Check out the [contributing guidelines](./CONTRIBUTING.md). Please note that this project is released with a [Code of Conduct](./CONDUCT.md). By contributing to this project, you agree to abide by its terms.

## License

`dsci524_group13_quizit` was created by Mavis Wong, Shengjia Yu, Sopuruchi Chisom. It is licensed under the terms of the [MIT license](./LICENSE).

## Credits

`dsci524_group13_quizit` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).

## Changelog

All notable changes to this project will be documented in [CHANGELOG.md](./CHANGELOG.md).
