from rest_framework import serializers
from statscollect_db.models import Person


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ('last_name', 'first_name', 'usual_name', 'sex',)
