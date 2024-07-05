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
    
# 팀 정보
class Player(models.Model):
    team_logo = models.URLField()
    team_name = models.CharField(max_length=100)
    position_icon = models.CharField(max_length=100)
    position_name = models.CharField(max_length=10)
    player_photo = models.URLField()
    player_name = models.CharField(max_length=100)

    def __str__(self):
        return self.player_name

# lck 순위
# class TeamRanking(models.Model):
#     team_logo = models.URLField()
#     team_name = models.CharField(max_length=100)
#     wins = models.IntegerField()
#     losses = models.IntegerField()
#     points = models.IntegerField()
#     rank = models.IntegerField(default=0)
#     season = models.CharField(max_length=100, default='2024 LCK 서머')
#     win_rate = models.FloatField(default=0.0) 
#     kda = models.FloatField(default=0.0)       
#     kills = models.IntegerField(default=0)    
#     deaths = models.IntegerField(default=0)    
#     assists = models.IntegerField(default=0)   