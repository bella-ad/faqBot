# FAQ Bot
This is a small script to play around with TfidfVectorizer.

The FAQBot can answer frequently asked questions based on the actual FAQs you provide.
When you are lucky you might even get the correct answer :)

You can easily use when you provide FAQs in markdown. 
The standard format for supported FAQs is:

```markdown
**Q: This is my question?**
And this is my answer.

**Q: This is another question?**
And this is another answer.
```

You can then create a bot with:
```python
from pathlib import Path
from faqbot.bot import FAQMarkdown, FAQBot

faq_markdown = FAQMarkdown(Path("path/to/faq.md"))
faq_bot = FAQBot(faq_markdowns=[faq_markdown])

print(faq_bot.answer_question("How can I pay?"))
```

If the format of your FAQs differ you can also provide a regex that splits the questions and answers:
```python
from pathlib import Path
from faqbot.bot import FAQMarkdown, FAQBot

faq_markdown = FAQMarkdown(Path("path/to/faq.md", r"\*\*Q: (.*?)\*\*\s*(.*?)(?=\*\*Q:|\Z)"))
faq_bot = FAQBot(faq_markdowns=[faq_markdown])

print(faq_bot.answer_question("How can I pay?"))
```

Finally, you can also provide multiple markdown files with different regex:
```python
from pathlib import Path
from faqbot.bot import FAQMarkdown, FAQBot

faq_markdown = FAQMarkdown(Path("path/to/faq.md", r"\*\*Q: (.*?)\*\*\s*(.*?)(?=\*\*Q:|\Z)"))
faq_bot = FAQBot(faq_markdowns=[
    FAQMarkdown(Path("path/to/faq.md", r"\*\*Q: (.*?)\*\*\s*(.*?)(?=\*\*Q:|\Z)")),
    FAQMarkdown(Path("path/to/other/faq.md", r"\*\*Question: (.*?)\*\*\s*(.*?)(?=\*\*Q:|\Z)"))
])

print(faq_bot.answer_question("How can I pay?"))
```