from django.db import models

class Jobs(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
      
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'Jobs'
        verbose_name = 'Job'
    
    
