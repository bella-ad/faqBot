from pathlib import Path

from faqbot.bot import _faq_markdown_to_dict, FAQMarkdown, FAQBot


def test_faq_markdown_to_dict():
    # given
    path_to_markdown = Path("./assets/test_faq.md")

    # when
    faq_dict = _faq_markdown_to_dict(path_to_markdown=path_to_markdown)

    # then
    assert len(faq_dict) == 5


def test_whole_bot():
    faq_markdown = FAQMarkdown(Path("./assets/test_faq.md"))
    faq_bot = FAQBot(faq_markdowns=[faq_markdown])

    print(faq_bot.answer_question("How can I pay?"))
