from django.contrib import admin
from .models import Match

class MatchAdmin(admin.ModelAdmin):
    list_display = ('team_a_name', 'team_b_name', 'match_date', 'match_time')

admin.site.register(Match, MatchAdmin)
