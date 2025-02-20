from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, PermissionsMixin
from django.utils import timezone

# Create your models here.

# # 自定义用户管理器（如果需要额外的用户管理功能，可以扩展这个类）
# class CustomUserManager(UserManager):
#     def create_user(self, username, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(username=username, email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self.create_user(username, email, password, **extra_fields)

# # 用户模型
# # class User(AbstractBaseUser, PermissionsMixin):
# class User(AbstractUser):
#     username = models.CharField(max_length=50, unique=True)
#     email = models.EmailField(max_length=100, unique=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(default=timezone.now)
#     nickname = models.CharField(max_length=50, blank=True, null=True)
#     avatar_url = models.URLField(blank=True, null=True)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']

#     def __str__(self):
#         return self.username

# 智能体模型
class AgentModel(models.Model):
    agent_id = models.IntegerField()
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
 
    def __str__(self):
        return self.name
 
# 聊天会话模型（只考虑与智能体的会话）
class SessionModel(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    # agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='chat_sessions')
    session_id = models.CharField(max_length=64, null=False, blank=False)
    user_id = models.IntegerField()
    agent_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f'Chat session between {self.user_id} and {self.agent_id}'
 
# 消息模型
class MessageModel(models.Model):
    # session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    session_id = models.CharField(max_length=64, null=False, blank=False)
    # sender 字段在这里不是必需的，因为我们可以通过逻辑来确定发送者（例如，通过检查当前会话的用户和智能体）
    # 但如果你希望明确存储发送者类型，可以添加一个枚举字段（如 sender_type）和一个 GenericForeignKey
    content = models.TextField()
    # 0 代表用户发的消息，1代表智能体的消息
    sender_type = models.SmallIntegerField() 
    timestamp = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f'Message in session {self.session_id} at {self.timestamp}'
 
# # 消息索引模型（用于快速检索或搜索）
# class MessageIndex(models.Model):
#     message = models.OneToOneField(Message, on_delete=models.CASCADE, related_name='index')
#     # 索引字段，例如全文搜索的向量或关键词
#     # 在这个简化的例子中，我们只添加一个示例字段
#     search_vector = models.TextField(blank=True, null=True)  # 这可能是一个由数据库或搜索服务生成的向量
 
#     # 注意：在实际应用中，search_vector字段的填充可能需要额外的逻辑或使用数据库的全文搜索功能
#     # 此外，对于大型数据集，你可能希望使用专门的搜索服务（如Elasticsearch）来处理索引和搜索
 
#     def __str__(self):
#         return f'Index for message {self.message.id}'