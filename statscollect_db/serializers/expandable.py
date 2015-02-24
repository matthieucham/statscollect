from rest_framework import serializers


class ExpandableSerializer(serializers.ModelSerializer):
    expand = []

    def __init__(self, *args, context=None, **kwargs):
        super(ExpandableSerializer, self).__init__(*args, context=context, **kwargs)
        expand = context.get('request').QUERY_PARAMS.get('expand') if context else None

        if expand:
            expand_list = expand.split(',')

            for item in self.expand:
                if item not in expand_list:
                    try:
                        self.fields.pop(item)
                    except KeyError:
                        pass
        else:
            for item in self.expand:
                try:
                    self.fields.pop(item)
                except KeyError:
                    pass