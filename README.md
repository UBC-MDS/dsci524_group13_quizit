# dsci524_group13_quizit

A python package for creating and taking quizzes.

## Summary
### Project Summary
This Python package is designed to help users to create custom build quizzes.
The package allows users to load multiple-choice and/or short-answer question sets.
It will then randomly select a user-defined number of questions from the question sets and generate a quiz.
Quiz scores and time used will be displayed at the end of the quiz.
Optionally, users can also have their quiz scores and incorrect and correct questions in a text file. 

### Package Functions
The package has three functions: 
- `load_questions()` : allow users to load in their own multiple-choice or short answer question sets 
- `take_multiple_choice(n, save_questions=False, save_score=False)`:
    - Allow users to take a multiple-choice quiz with optional result tracking.
- `take_short_answer()` : allow users to take a short answer quiz.

### Python Ecosystem Integration



## Installation

```bash
$ pip install dsci524_group13_quizit
```

## Tests

## Usage

- TODO

## Contributors

Mavis Wong(@MavisWong295), Shangjia Yu(@shangjiayuu), Sopuruchi Chisom(@cs-uche)

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`dsci524_group13_quizit` was created by Mavis Wong, Shengjia Yu, Sopuruchi Chisom. It is licensed under the terms of the MIT license.

## Credits

`dsci524_group13_quizit` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
