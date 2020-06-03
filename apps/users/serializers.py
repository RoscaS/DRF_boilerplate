from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    registered_at = serializers.DateTimeField(format='%H:%M %d.%m.%Y', read_only=True)
    picture = serializers.ImageField(max_length=None, use_url=True, required=False)
    full_name = serializers.SerializerMethodField(read_only=True)
    short_name = serializers.SerializerMethodField(read_only=True)

    def get_full_name(self, obj):
        return obj.full_name

    def get_short_name(self, obj):
        return obj.short_name

    def get_invitation_accepted(self, obj):
        return obj.was_updated()


    class Meta:
        model = User
        fields = ['id',
                  'email',
                  'picture',
                  'first_name',
                  'last_name',
                  'full_name',
                  'short_name',
                  'registered_at',
                  ]


class UserWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email',
                  'picture',
                  'password',
                  'first_name',
                  'last_name']
