from django import template
from news.resources import censor_list

register = template.Library()


@register.filter()
def censor(words):
    if not isinstance(words, str):
        raise TypeError('censor applide to a non-string type')
    for i in censor_list:
        words = words.replace(i[1:], '*' * (len(i) - 1))
    return words
