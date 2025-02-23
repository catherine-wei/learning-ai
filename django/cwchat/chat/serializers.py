from rest_framework import serializers
from .models.models import MessageModel, AgentModel, SessionModel

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


from .models.model_character import CharacterRoleModel, CharacterModelModel, CharacterActionModel, CharacterEmotionModel
from .models.model_bgimg import BackgroundImageModel
from .models.model_asr import AsrHotwordsModel, AsrSensitivewordsModel, AsrRecordsModel
from .models.model_tts import TtsVoiceIdModel, TtsVoiceCloneModel, TtsRecordsModel
from .models.model_llm import LlmPromptModel
from .models.model_schedule import SchedulesModel

#######################
# Background image
#######################
class BackgroundImageSerializer(serializers.ModelSerializer):
    original_name = serializers.CharField(required=False)
    class Meta:
        model = BackgroundImageModel
        fields = '__all__'

#######################
# Character
#######################
class CharacterRoleSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(required=True)
    class Meta:
        model = CharacterRoleModel
        fields = '__all__'

class CharacterEmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterEmotionModel
        fields = '__all__'

class CharacterActionSerializer(serializers.ModelSerializer):
    original_name = serializers.CharField(required=False)
    class Meta:
        model = CharacterActionModel
        fields = '__all__'

class CharacterModelSerializer(serializers.ModelSerializer):
    original_name = serializers.CharField(required=False)
    vrm_type = serializers.CharField(required=False)
    class Meta:
        model = CharacterModelModel
        fields = '__all__'

#######################
# LLM
#######################
class LlmPromptSerializer(serializers.ModelSerializer):
    prompt_name = serializers.CharField(required=True)
    class Meta:
        model = LlmPromptModel
        fields = '__all__'

# class ChatlogSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ChatlogModel
#         fields = '__all__'

#######################
# ASR
#######################
class AsrHotwordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsrHotwordsModel
        fields = '__all__'

class AsrSensitivewordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsrSensitivewordsModel
        fields = '__all__'


#######################
# TTS
#######################
class TtsVoiceIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = TtsVoiceIdModel
        fields = '__all__'

class TtsVoiceCloneSerializer(serializers.ModelSerializer):
    class Meta:
        model = TtsVoiceCloneModel
        fields = '__all__'

#######################
# 会议精灵
#######################
class OmScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchedulesModel
        fields = '__all__'
