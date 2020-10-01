from rest_framework import serializers

from urlbutcher.models import Url, SlugClickCounter



class SlugSerializer(serializers.ModelSerializer):
    counter = serializers.SlugRelatedField(
        read_only=True, allow_null=True, slug_field='click_counter'
    )

    class Meta:
        model = Url
        fields = ('slug', 'url', 'created_at', 'counter')
