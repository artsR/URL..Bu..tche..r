from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.utils import timezone

from urlbutcher.models import Url, SlugClickCounter
from urlbutcher.views import ALPHABET



class SlugSerializer(serializers.ModelSerializer):
    counter = serializers.SlugRelatedField(
        read_only=True, allow_null=True, slug_field='click_counter'
    )
    user = serializers.ReadOnlyField(source='user.username')

    def create(self, validated_data):
        """Given the validated URL (optionally custom SLUG), creates random slug
        for authenticated user.
        """
        custom_slug = validated_data.get('slug', None)
        new_slug = Url.get_unique_slug(ALPHABET) if custom_slug is None else custom_slug
        new_url = validated_data.get('url')
        user = self.context['request'].user
        url_obj, _ = Url.objects.update_or_create(
            slug=new_slug,
            defaults={'url': new_url, 'created_at': timezone.now(), 'user': user}
        )
        return url_obj

    def validate_slug(self, value):
        if not value:
            return value

        old_slug = Url.objects.filter(slug=value).first()
        if (old_slug is not None) and (not old_slug.expired()):
            raise serializers.ValidationError({'slug': 'Slug already used'})
        return value

    class Meta:
        model = Url
        fields = ('slug', 'url', 'created_at', 'counter', 'user')
        extra_kwargs = {'slug': {'required': False, 'validators': []}}
        read_only_fields = ('created_at',)
