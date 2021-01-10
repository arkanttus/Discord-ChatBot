from chatterbot import ChatBot
from chatterbot.languages import POR
from chatterbot.comparisons import LevenshteinDistance
from chatterbot.response_selection import get_first_response, get_random_response
import spacy

nlp = spacy.load('pt')

chatbot = ChatBot(
    "TEU TIO",
    language=POR,
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": LevenshteinDistance,
            "response_selection_method": get_random_response
        }
    ]
)
