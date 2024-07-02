from django.db import models

class Champion(models.Model):
    key = models.CharField(max_length=100)
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    lore = models.TextField()
    blurb = models.TextField()
    allytips = models.TextField()
    enemytips = models.TextField()
    tags = models.CharField(max_length=100)
    partype = models.CharField(max_length=100)

class ChampionImage(models.Model):
    champion = models.OneToOneField(Champion, on_delete=models.CASCADE)
    full = models.CharField(max_length=100)
    sprite = models.CharField(max_length=100)
    group = models.CharField(max_length=100)
    x = models.IntegerField()
    y = models.IntegerField()
    W = models.IntegerField()
    h = models.IntegerField()

class ChampionSkin(models.Model):
    champion = models.ForeignKey(Champion, on_delete=models.CASCADE)
    id = models.CharField(max_length=100, primary_key=True)
    num = models.IntegerField()
    name = models.CharField(max_length=100)
    chromas = models.BooleanField()

class ChampionInfo(models.Model):
    champion = models.OneToOneField(Champion, on_delete=models.CASCADE)
    attack = models.IntegerField()
    defense = models.IntegerField()
    magic = models.IntegerField()
    difficulty = models.IntegerField()

class ChampionStat(models.Model):
    champion = models.OneToOneField(Champion, on_delete=models.CASCADE)
    hp = models.FloatField()
    hpperlevel = models.FloatField()
    mp = models.FloatField()
    mpperlevel = models.FloatField()
    movespeed = models.FloatField()
    armor = models.FloatField()
    armorperlevel = models.FloatField()
    spellblock = models.FloatField()
    spellblockperlevel = models.FloatField()
    attackrange = models.FloatField()
    hpregen = models.FloatField()
    hpregenperlevel = models.FloatField()
    mpregen = models.FloatField()
    mpregenperlevel = models.FloatField()
    crit = models.FloatField()
    critperlevel = models.FloatField()
    attackdamage = models.FloatField()
    attackdamageperlevel = models.FloatField()
    attackspeedperlevel = models.FloatField()
    attackspeed = models.FloatField()

class ChampionSpell(models.Model):
    champion = models.ForeignKey(Champion, on_delete=models.CASCADE)
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    tooltip = models.TextField()
    maxrank = models.IntegerField()
    cooldown = models.TextField()
    cooldownBurn = models.CharField(max_length=100)
    cost = models.TextField()
    costBurn = models.CharField(max_length=100)
    costType = models.CharField(max_length=100)
    range = models.TextField()
    resource = models.CharField(max_length=100, blank=True)

class SpellImage(models.Model):
    spell = models.OneToOneField(ChampionSpell, on_delete=models.CASCADE)
    full = models.CharField(max_length=100)
    sprite = models.CharField(max_length=100)
    group = models.CharField(max_length=100)
    x = models.IntegerField()
    y = models.IntegerField()
    W = models.IntegerField()
    h = models.IntegerField()

class ChampionPassive(models.Model):
    champion = models.OneToOneField(Champion, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()

class PassiveImage(models.Model):
    passive = models.OneToOneField(ChampionPassive, on_delete=models.CASCADE)
    full = models.CharField(max_length=100)
    sprite = models.CharField(max_length=100)
    group = models.CharField(max_length=100)
    x = models.IntegerField()
    y = models.IntegerField()
    W = models.IntegerField()
    h = models.IntegerField()
