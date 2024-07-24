from django.db import models
from django.utils import timezone

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
    team_name = models.CharField(max_length=100)
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

# # 계정
# class Member(models.Model):
#     member_id = models.CharField(max_length=30, primary_key=True)
#     member_password = models.CharField(max_length=30)
#     member_name = models.CharField(max_length=20)
#     member_nickname = models.CharField(max_length=30)
#     member_gender = models.CharField(max_length=5)
#     member_email = models.CharField(max_length=40)
#     member_phone = models.CharField(max_length=25)
#     member_zipcode = models.CharField(max_length=15)
#     member_address1 = models.CharField(max_length=100)
#     member_address2 = models.CharField(max_length=100, default='') 
#     member_birthday = models.CharField(max_length=15)
#     reg_date = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return "self.member_id="+self.member_id+", self.member_password="+self.member_password

