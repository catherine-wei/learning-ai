from rest_framework import serializers
from .models import MessageModel, AgentModel, SessionModel

class MessageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageModel
        fields = '__all__'  # 这将序列化模型中的所有字段
        # 或者，你可以显式地列出要序列化的字段，例如：
        # fields = ['id', 'name', 'description', 'created_at', 'updated_at']


class AgentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentModel
        fields = '__all__'

class SessionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionModel
        fields = '__all__'

