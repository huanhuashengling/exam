from django import template
register = template.Library()

@register.filter
def getindex(indexable, i):
    return indexable[i]

@register.filter
def getsplitindex(indexable, answerInfo):
    answers = answerInfo.split(",")
    result = ""
    for answer in answers:
      result += indexable[int(answer)]
    return result