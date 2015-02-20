from rest_framework import serializers
from rest_framework.reverse import reverse

from statscollect_db.models import Person


class PersonSerializer(serializers.ModelSerializer):
    rep_country = serializers.SerializerMethodField('get_country')
    href = serializers.HyperlinkedIdentityField(view_name='person-detail', lookup_field='uuid')
    links = serializers.SerializerMethodField()

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
                    'person-currentteam-list-nested', args=(obj.uuid,), request=request
                ),
            },
        }

    class Meta:
        model = Person
        fields = ('uuid', 'href', 'last_name', 'first_name', 'usual_name', 'sex', 'rep_country', 'field', 'status',
                  'links')


