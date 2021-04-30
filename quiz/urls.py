from django.urls import path
from .views import teacher_views, student_views

urlpatterns = [

]

# TEACHERS LOGIC PATTERNS 

urlpatterns += [
  path('teachers/home/', teacher_views.TeacherQuizHomeView.as_view(), name='teachers_dashboard'),
  path('teachers/quiz/<int:pk>/details/', teacher_views.TeacherQuizDetailView.as_view(), name='quiz_cms_details'),
  path('quiz/create/', teacher_views.QuizCreateUpdateView.as_view(), name='create_quiz'),
  path('quiz/<int:id>/update/', teacher_views.QuizCreateUpdateView.as_view(), name='update_quiz'),
  path('quiz/<int:id>/delete/', teacher_views.QuizDeleteView.as_view(), name='delete_quiz'),
  path('quiz/question/<int:pk>/delete/', teacher_views.QuestionDeleteView.as_view(), name='delete_question'),
  path('quiz/<int:pk>/question/create/', teacher_views.QuestionCreateUpdateView.as_view(), name='create_question'),
  path('quiz/<int:pk>/question/<int:question_id>/update/', teacher_views.QuestionCreateUpdateView.as_view(), name='update_question'),
  path('questions/order/', teacher_views.OrderQuestion.as_view(), name='order_questions'),
]

# STUDENTS LOGIC PATTERNS

urlpatterns += [
  path('students/home/', student_views.StudentHomeView.as_view(), name='students_dashboard'),
]