from django import template


register = template.Library()


@register.filter(name='censor')
def censor(value):
    count = 0
    bad_words = ['сука', 'черт', 'блин', 'скотина', 'падла', 'гадость']
    text = value.split()
    for word in text:
        word = word.lower()
        for bad_word in bad_words:
            if word == bad_word:
                return value.replace(text[count], '*' * len(word))
        count += 1
    return value
