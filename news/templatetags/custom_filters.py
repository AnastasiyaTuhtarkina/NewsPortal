from django import template


register = template.Library()

words = ['дурак', 'мудак', 'попа', 'титька', 'хрен', 'вонючка', 'чурбан', 'остолоп', 'чумазую', 'прожорливые', 'монарх']


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(value):
    if type(value) == str:
        value = value.lower().split()
        for i, word in enumerate(value):
            if word in words:
                value[i] = word[0] + '*' * len(word[1:]) 
        return ' '.join(value)

