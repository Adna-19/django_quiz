from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from .fields import OrderField

class Subject(models.Model):
  name        = models.CharField(max_length=50)
  slug        = models.SlugField(max_length=200, unique=True, blank=True)
  badge_color = models.CharField(max_length=7, default="#989898")

  def save(self, *args, **kwargs):
    self.slug = slugify(self.name)
    super(Subject, self).save(*args, **kwargs)

  def __str__(self):
    return self.name

class Quiz(models.Model):
  title          = models.CharField(max_length=200)
  teacher        = models.ForeignKey('accounts.TeacherProfile', 
                                      related_name='created_quizzes', 
                                      on_delete=models.CASCADE)
  subject        = models.ForeignKey(Subject, related_name='quizzes', on_delete=models.CASCADE)
  slug           = models.SlugField(max_length=200, unique=True, blank=True)
  summary        = models.TextField()
  score          = models.PositiveIntegerField(null=True, blank=True)
  date_created   = models.DateTimeField(auto_now_add=True)
  date_updated   = models.DateTimeField(auto_now=True)
  # date_published = models.DateTimeField()

  starts_at = models.DateTimeField()
  ends_at   = models.DateTimeField()

  def save(self, *args, **kwargs):
    self.slug = f"{slugify(self.title)}-{slugify(timezone.now())}"
    super(Quiz, self).save(*args, **kwargs)

  def get_absolute_url(self):
    return f"/quizzes/{self.slug}/quiz/"

  def __str__(self):
    return f"| {self.title} || by {self.teacher.user.full_name}"

  class Meta:
    verbose_name_plural = 'Quizzes'

class Question(models.Model):
  quiz         = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
  text         = models.CharField(max_length=400)
  score        = models.PositiveIntegerField(null=True, blank=True)
  is_active    = models.BooleanField(default=True)
  date_created = models.DateTimeField(auto_now_add=True)
  date_updated = models.DateTimeField(auto_now=True)
  order        = OrderField(null=True, blank=True, for_fields=['quiz'])

  def __str__(self):
    return f"Q: '{self.text}' from Quiz '{self.quiz.title}'"

  class Meta:
    ordering = ['order']

class Answer(models.Model):
  question     = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
  text         = models.CharField(max_length=200)
  is_correct   = models.BooleanField(default=False)
  is_active    = models.BooleanField(default=True)
  date_created = models.DateTimeField(auto_now_add=True)
  date_updated = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"Answer: {self.text} for Q: {self.question.text}"

class TakenQuiz(models.Model):
  student = models.ForeignKey('accounts.StudentProfile', 
                              related_name='taken_quizzes', 
                              on_delete=models.CASCADE)
  quiz    = models.ForeignKey(Quiz, on_delete=models.CASCADE)

  def __str__(self):
    return f"Quiz: {self.quiz.title} taken by {self.student.user.full_name}"

class StudentAnswer(models.Model):
  taken_quiz = models.ForeignKey(TakenQuiz, related_name='answers', on_delete=models.CASCADE)
  question   = models.ForeignKey(Question, on_delete=models.CASCADE)
  answer     = models.ForeignKey(Answer, on_delete=models.CASCADE)

  def __str__(self):
    return f"Answer: {self.answer.text} for Q:{self.question.text} in Quiz: {self.taken_quiz.quiz.title}"