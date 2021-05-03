from django import template
register = template.Library()

@register.filter()
def already_selected_by(subject, user):
  if subject in user.interests.all():
    return True
  return False

@register.filter()
def already_attempted_quiz_by(quiz, student):
  if student.taken_quizzes.filter(quiz=quiz).exists():
    return True
  return False
