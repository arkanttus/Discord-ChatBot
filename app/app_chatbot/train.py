import os
import sys
from pathlib import Path
from chatterbot.conversation import Statement
from chatterbot.trainers import Trainer
from chatterbot import utils
from .bot import chatbot

class ChatterBotCorpusTrainer(Trainer):
    """
    Allows the chat bot to be trained using data from the
    ChatterBot dialog corpus.
    """

    def train(self, *corpus_paths):
        from chatterbot.corpus import load_corpus, list_corpus_files

        data_file_paths = []

        # Get the paths to each file the bot will be trained with
        for corpus_path in corpus_paths:
            data_file_paths.extend(list_corpus_files(corpus_path))

        for corpus, categories, file_path in load_corpus(*data_file_paths):

            statements_to_create = []

            # Train the chat bot with each statement and response pair
            for conversation_count, conversations in enumerate(corpus):

                if self.show_training_progress:
                    utils.print_progress_bar(
                        'Training ' + str(os.path.basename(file_path)),
                        conversation_count + 1,
                        len(corpus)
                    )

                previous_statements_texts = [None]
                previous_statements_search_texts = ['']

                for conversation in conversations:

                    if isinstance(conversation, str):
                        conversation = [conversation]
                    
                    statements_texts = []
                    statements_search_texts = []

                    for previous_statement_text, previous_statement_search_text in zip(previous_statements_texts, previous_statements_search_texts):

                        for text in conversation:
                            statement_search_text = self.chatbot.storage.tagger.get_bigram_pair_string(text)

                            statement = Statement(
                                text=text,
                                search_text=statement_search_text,
                                in_response_to=previous_statement_text,
                                search_in_response_to=previous_statement_search_text,
                                conversation='training'
                            )

                            statement.add_tags(*categories)

                            statement = self.get_preprocessed_statement(statement)

                            statements_texts.append(statement.text)
                            statements_search_texts.append(statement_search_text)

                            statements_to_create.append(statement)

                    previous_statements_texts = statements_texts
                    previous_statements_search_texts = statements_search_texts

            if statements_to_create:
                self.chatbot.storage.create_many(statements_to_create)

trainer = ChatterBotCorpusTrainer(chatbot)

path = Path(__file__).parent / "./corpus/"

for files in os.listdir(path):
    trainer.train(fr'{path.__str__()}/{files}')