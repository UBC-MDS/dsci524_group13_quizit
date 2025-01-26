# read version from installed package
from importlib.metadata import version
__version__ = version("dsci524_group13_quizit")

# populate package namespace
from dsci524_group13_quizit.quizit import Quizit, QuestionType