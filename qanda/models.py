from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Question(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('question_detail', kwargs={'pk': self.pk})
    
    class Meta:
        ordering = ['-date_posted']

class Answer(models.Model):
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    likes = models.ManyToManyField(User, related_name='liked_answers', blank=True)
    
    def __str__(self):
        return f"Answer by {self.author.username} on {self.question.title}"
    
    def total_likes(self):
        return self.likes.count()
    
    class Meta:
        ordering = ['-date_posted']
