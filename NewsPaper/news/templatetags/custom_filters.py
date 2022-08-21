from django import template


register = template.Library()

STOP_LIST=[
   'редиска',
]

@register.filter()
def censor(text):
   text = str.lower(text)
   for word in text.split():
      if word.lower() in STOP_LIST:
         text = text.replace(word, f'{word[0]}{"*" * (len(word) - 1)}')
   return text



