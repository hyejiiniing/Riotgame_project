from django.db import models

class Match(models.Model):
    team_a_name = models.CharField(max_length=100)
    team_b_name = models.CharField(max_length=100)
    team_a_logo = models.URLField(max_length=200, default='default_logo_url')
    team_b_logo = models.URLField(max_length=200, default='default_logo_url')
    match_date = models.CharField(max_length=100)
    match_time = models.CharField(max_length=100)
    vs_image = models.TextField()

    def __str__(self):
        return f"{self.team_a_name} vs {self.team_b_name} on {self.match_date} at {self.match_time}"
