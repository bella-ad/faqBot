import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

FAQ_SPLIT_REGEX = r"\*\*Q: (.*?)\*\*\s*(.*?)(?=\*\*Q:|\Z)"


def _faq_markdown_to_dict(path_to_markdown: Path, split_regex: str = FAQ_SPLIT_REGEX):
    """
    Given a path to a faq file, returns a dict with the questions as key and the answers as values.
    """

    markdown = _read_markdown_file(path_to_markdown=path_to_markdown)
    faq_dict = {}
    question_answer_pairs = re.findall(split_regex, markdown, re.DOTALL)

    for pair in question_answer_pairs:
        question = pair[0].strip()
        answer = pair[1].strip()
        faq_dict[question] = answer
    return faq_dict


def _read_markdown_file(path_to_markdown: Path) -> str:
    with open(path_to_markdown, "r") as markdown_file:
        return markdown_file.read()


@dataclass
class FAQMarkdown:
    path_to_markdown: Path
    question_split_regex: str = FAQ_SPLIT_REGEX


class FAQBot:

    def __init__(self, faq_markdowns: List[FAQMarkdown]):
        self._question_answer_dict = self._create_question_answer_dict(faq_markdowns=faq_markdowns)
        self.vectorizer = TfidfVectorizer()
        self.vectorizer.fit(self._question_answer_dict.keys())

    @staticmethod
    def _create_question_answer_dict(faq_markdowns: List[FAQMarkdown]) -> Dict:
        faq_dict = {}
        for faq_markdown in faq_markdowns:
            faq_dict.update(
                _faq_markdown_to_dict(
                    path_to_markdown=faq_markdown.path_to_markdown, split_regex=faq_markdown.question_split_regex
                )
            )
        return faq_dict

    def answer_question(self, question: str) -> str:
        user_vector = self.vectorizer.transform([question])
        questions_vector = self.vectorizer.transform(self._question_answer_dict.keys())

        similarities = cosine_similarity(user_vector, questions_vector)
        closest = similarities.argmax()

        return list(self._question_answer_dict.values())[closest]
