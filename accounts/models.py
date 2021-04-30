from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from quiz.models import Subject

class User(AbstractUser):
  USER_CHOICES = (
    ('S', 'STUDENT'),
    ('T', 'TEACHER'),
  )
  user_role = models.CharField(max_length=15, choices=USER_CHOICES)

  def save(self, *args, **kwargs):
    created = self.id is None
    super(User, self).save(*args, **kwargs)
    if created and self.user_role == 'T':
      self.groups.add(Group.objects.get(name="Teacher"))
    elif created and self.user_role == 'S':
      self.groups.add(Group.objects.get(name="Student"))

  @property
  def full_name(self):
    return f"{self.first_name} {self.last_name}"

class TeacherProfile(models.Model):
  GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
  )
  user           = models.OneToOneField(User, related_name='teacher_profile', on_delete=models.CASCADE)
  gender         = models.CharField(max_length=10, choices=GENDER_CHOICES, default='M')
  profile_image  = models.ImageField(upload_to='profile_images/teachers_profile_images/')
  place_of_birth = models.CharField(max_length=30)
  about             = models.TextField()
  facebook_profile  = models.URLField()
  twitter_profile   = models.URLField()
  github_profile    = models.URLField()
  instagram_profile = models.URLField()

  def __str__(self):
    return f"{self.user.full_name}"


class StudentProfile(models.Model):
  GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
  )
  user          = models.OneToOneField(User, related_name='student_profile', on_delete=models.CASCADE)
  profile_image = models.ImageField(upload_to='profile_images/students_profile_images/')
  gender        = models.CharField(max_length=10, choices=GENDER_CHOICES)
  interests     = models.ManyToManyField(Subject, blank=True)
  bio           = models.TextField()

  def __str__(self):
    return f"{self.user.full_name}"