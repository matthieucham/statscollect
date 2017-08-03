from rest_framework import serializers
from rest_framework.reverse import reverse

from statscollect_db import models


class PersonSerializer(serializers.ModelSerializer):
    rep_country = serializers.SerializerMethodField('get_country')
    href = serializers.HyperlinkedIdentityField(view_name='person-detail', lookup_field='uuid')

    def get_country(self, obj):
        if obj.rep_country:
            return obj.rep_country.name
        else:
            return None

    class Meta:
        model = models.Person
        fields = ('uuid', 'created_at', 'updated_at', 'href', 'last_name', 'first_name', 'usual_name', 'sex',
                  'rep_country', 'field', 'status')


class FootballPlayerSerializer(serializers.ModelSerializer):
    rep_country = serializers.SerializerMethodField('get_country')
    href = serializers.HyperlinkedIdentityField(view_name='footballplayer-detail', lookup_field='uuid')
    links = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()

    def get_position(self, obj):
        if isinstance(obj, models.FootballPerson):
            return obj.position
        elif obj.field == 'FOOTBALL':
            return models.FootballPerson.objects.get(pk=obj.pk).position
        return None

    def get_country(self, obj):
        if obj.rep_country:
            return obj.rep_country.name
        else:
            return None

    def get_links(self, obj):
        request = self.context.get('request', None)

        return {
            'current_teams': {
                'href': reverse(
                    'footballplayer-currentteam-list-nested', args=(obj.uuid,), request=request
                ),
            },
            'meetings_history': {
                'href': reverse(
                    'footballplayer-instance-list-nested', args=(obj.uuid,), request=request
                ),
            }
        }

    class Meta:
        model = models.FootballPerson
        fields = ('uuid',
                  'created_at', 'updated_at',
                  'href',
                  'last_name',
                  'first_name',
                  'usual_name',
                  'position',
                  'rep_country',
                  'status',
                  'links',)


