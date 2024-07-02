import os
import json
from django.core.management.base import BaseCommand
from typing import Dict
from django.conf import settings
from model_champion.models import Champion, ChampionImage, ChampionInfo, ChampionPassive, ChampionSkin, ChampionSpell, ChampionStat, PassiveImage, SpellImage

def intListToStr(arr):
    return ",".join(map(str, arr))

def putChampions(json_file_path):
    with open(json_file_path, encoding='UTF-8') as f:
        data: Dict = json.load(f)['data']

    Champion.objects.all().delete()

    for key, value in data.items():
        allytips = ",".join(value['allytips'])
        enemytips = ",".join(value['enemytips'])
        tags = ",".join(value['tags'])

        champion = Champion.objects.create(
            key=value['key'],
            id=value['id'],
            name=value['name'],
            title=value['title'],
            lore=value['lore'],
            blurb=value['blurb'],
            allytips=allytips,
            enemytips=enemytips,
            tags=tags,
            partype=value['partype']
        )

        ChampionImage.objects.create(
            champion=champion,
            full=value['image']['full'],
            sprite=value['image']['sprite'],
            group=value['image']['group'],
            x=value['image']['x'],
            y=value['image']['y'],
            W=value['image']['w'],
            h=value['image']['h'],
        )

        skinBulkList = [
            ChampionSkin(
                champion=champion,
                id=skin['id'],
                num=skin['num'],
                name=skin['name'],
                chromas=skin['chromas']
            ) for skin in value['skins']
        ]
        ChampionSkin.objects.bulk_create(skinBulkList)

        ChampionInfo.objects.create(
            champion=champion,
            attack=value['info']['attack'],
            defense=value['info']['defense'],
            magic=value['info']['magic'],
            difficulty=value['info']['difficulty']
        )

        ChampionStat.objects.create(
            champion=champion,
            hp=value['stats']['hp'],
            hpperlevel=value['stats']['hpperlevel'],
            mp=value['stats']['mp'],
            mpperlevel=value['stats']['mpperlevel'],
            movespeed=value['stats']['movespeed'],
            armor=value['stats']['armor'],
            armorperlevel=value['stats']['armorperlevel'],
            spellblock=value['stats']['spellblock'],
            spellblockperlevel=value['stats']['spellblockperlevel'],
            attackrange=value['stats']['attackrange'],
            hpregen=value['stats']['hpregen'],
            hpregenperlevel=value['stats']['hpregenperlevel'],
            mpregen=value['stats']['mpregen'],
            mpregenperlevel=value['stats']['mpregenperlevel'],
            crit=value['stats']['crit'],
            critperlevel=value['stats']['critperlevel'],
            attackdamage=value['stats']['attackdamage'],
            attackdamageperlevel=value['stats']['attackdamageperlevel'],
            attackspeedperlevel=value['stats']['attackspeedperlevel'],
            attackspeed=value['stats']['attackspeed'],
        )

        for spell in value['spells']:
            championSpell = ChampionSpell.objects.create(
                champion=champion,
                id=spell['id'],
                name=spell['name'],
                description=spell['description'],
                tooltip=spell.get('tooltip', ''),
                maxrank=spell['maxrank'],
                cooldown=intListToStr(spell['cooldown']),
                cooldownBurn=spell['cooldownBurn'],
                cost=intListToStr(spell['cost']),
                costBurn=spell['costBurn'],
                costType=spell['costType'],
                range=intListToStr(spell['range']),
                resource=spell.get('resource', '')
            )

            SpellImage.objects.create(
                spell=championSpell,
                full=spell['image']['full'],
                sprite=spell['image']['sprite'],
                group=spell['image']['group'],
                x=spell['image']['x'],
                y=spell['image']['y'],
                W=spell['image']['w'],
                h=spell['image']['h'],
            )

        championPassive = ChampionPassive.objects.create(
            champion=champion,
            name=value['passive']['name'],
            description=value['passive']['description']
        )

        PassiveImage.objects.create(
            passive=championPassive,
            full=value['passive']['image']['full'],
            sprite=value['passive']['image'].get('sprite', ''),  # 기본 값으로 빈 문자열 설정
            group=value['passive']['image']['group'],
            x=value['passive']['image']['x'],
            y=value['passive']['image']['y'],
            W=value['passive']['image']['w'],
            h=value['passive']['image']['h'],
        )

    return "챔피언 데이터베이스 업데이트 완료"

class Command(BaseCommand):
    help = 'Load champion data into the database'

    def add_arguments(self, parser):
        parser.add_argument('json_file_path', type=str, help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        json_file_path = kwargs['json_file_path']
        message = putChampions(json_file_path)
        self.stdout.write(self.style.SUCCESS(message))
