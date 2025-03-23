[TOC]
# 小落同学项目信息全览
# 一、前言
由于是一个真正的小白开始，从前端界面，到Django框架，再到后端引擎，都是我从来没有接触过的一些新东西、新技术，整个过程完全是靠不断的问Deepseek，文心一言，千问, 豆包等大模型问出来的，代码也基本上都是靠这些大模型先给我写一个版本，然后再自己一边猜一边改出来的，所以，这些代码包括了从我完全不懂，再到有一点点懂，这个过程，更直白一点讲就是这些代码里有许多做法对于真正有经验的人来说，可能写得乱七八糟。

因此，如果你看到代码里有什么错误的地方，还请见谅，并不啬赐教，您的指正可能会帮助到很多人。

代码：https://github.com/catherine-wei/learning-ai
演示：https://x.oddmeta.net

# 二、我自己对小落同学的期望
复刻虚拟人生：给自己做一个专属的虚拟人，把TA当作我自己的一个树洞，每天或者每过一段时间把自己想说的话，想说的事，都告诉TA，然后如果某一天我想咨询一件事情的时候，可以去问问TA，看看一旦TA的数据多了后，TA会不会比我自己更懂我？

# 三、学习记录与计划
在README.md（总）和docs（分）目录下分文件记录学习过程。
计划：
- 自学编程的情况以及每周的学习计划，如每周学习2小时，完成博文至少一篇。
- 开始做一个微信公众号：奥德元，目前已经有将近10个人关注（都是朋友，而且都是僵尸粉，哈哈），本新人表示，真的很难，不过呢，没什么人关注也好，没压力，想做就做，不想做就不做。

# 四、项目代码总览
## 1。前端及Django学习
- Web开发: 前端界面相关。新东西、新技术的测试都放在tests/目录下。包括wechat和tests/downloads的相关文件中，尝试将Next.js项目的前端代码转换为纯HTML + JavaScript实现，以模仿开源项目的界面。
- Django项目：在src/cwchat目录下是一个Django项目，src/cwchat/chat是这个项目里创建的一个app。
- three.js相关：模型相关。 学习VRoid Studio/Blender/DAZ3D/Epic/VTuber等。

## 2。主进程及守护任务
详见src/cwchat/
- 配置并监听TCP地址127.0.0.1:8000，支持HTTP/Websocket（与前端之间用流式对话）。
- 聊天守护任务（Chat Deamon Task）：用于跟大模型做交互。
- 聊天历史记录保存任务（Chat History Task）：将聊天的输入输出保存到数据库。
- 直播连接器任务（Live Connecter Task）：用于与Bilibili、Douyin、Taobao、Kuaishou等平台交互。

## 3。后台引擎
chat/engine 目录下包含多个功能引擎，以下是对各个功能引擎的汇总：
- [ ] chat/engine/asr 语音识别引擎 - 跟公司的一个产品冲突，暂不准备做。
	- [ ] asr/base_asr_driver.py 语音识别的基础驱动接口的一个空架子，暂未作任何实现。
- [x] chat/engine/character 角色模型与动作初始化引擎
	- [x] sys_models.py 模型初始化 initSysDefault3dModels 函数初始化系统默认的角色3D模型。
	- [x] sys_actions.py 动作初始化 initSysDefaultActions 函数初始化系统默认的角色动作。
- [x] chat/engine/emotion 情感识别与响应引擎
	文件：emotion_manage.py
	- [x] 生成表情：GenerationEmote 类根据文本推测对应的表情。用于给前端的three.js播放与该回复相对应的表情
	- [x] 情感识别：EmotionRecognition 类通过调用大语言模型（LLM）识别用户对话的情感分类。
	- [x] 情感响应：EmotionRespond 类根据用户的情感问题分类生成简短的对话策略。
- [ ] chat/engine/live 直播引擎
	- [ ] base_live_driver.py 直播的基础驱动接口
	- [ ] live_bilibili_sdk.py
	- [ ] live_douyin_sdk.py
- [x] chat/engine/llm 大语言模型引擎
	- [x] base_llm_driver.py 大语言模型的基础驱动接口
	- [x] claude/claude_sdk.py 展示了如何使用 Claude API 进行对话
	- [ ] langchain/langchain_sdk.py 使用LangChain库创建智能代理，调用多种工具进行对话。
	- [x] text_generation/text_generation_sdk.py 基于文本生成 API 的聊天功能
	- [x] openai/openai_sdk.py 使用OpenAI创建智能代理，调用多种工具进行对话
	- [x] baidu/ernie_sdk.py 使用Ernie创建智能代理，调用多种工具进行对话
	- [x] deepseek/deepseek_sdk.py 使用deepseek创建智能代理，调用多种工具进行对话
	- [ ] qwen/qwen_sdk.py 使用Qwen创建智能代理，调用多种工具进行对话
	- [x] llm_engine.py
- [x] chat/engine/memory 记忆引擎
	- [x] base_memory_driver.py 记忆引擎的基础驱动接口
	- [x] memory_shorttime_impl.py 短期记忆
	- [ ] memory_longtime_impl.py 长期记忆
	- [ ] milvus_memory.py
	- [ ] embedding.py
- [ ] chat/engine/prompt 提示词引擎
	- [x] general: general character persona prompt 通用角色系统人设。
	- [x] agent: agent character persona prompt 代理角色系统人设。
	- [x] others: chat bot persona prompt 对话机器人系统人设。除persona外，额外加入personality, example of dialog等。
	- [x] AI角色话题生成：topic_generator.py 根据角色的记忆上下文自主生成话题，或者回复建议。
	- [ ] 人物画像生成引擎：portrait_recognition.py 根据对话文本识别文本中包含的用户的人物画像。
- [ ] chat/engine/relection 反思引擎
	- [ ] reflection_template.py 提供了一个模板，用于根据历史记录推导出高级见解。
	- [ ] reflection_generation.py 反思
- [ ] chat/engine/translation 翻译引擎
	- base_translation_driver.py 翻译功能的一个空架子。暂未作任何实现。
- [x] chat/engine/tts 语音合成引擎
	- [x] tts/base_tts_driver.py：语音合成的基础驱动接口。
	- [x] tts/tts_bert_vits2.py 基于 Bert-VITS2 的语音合成
	- [x] tts/tts_bert_vits2_v2.py 基于 Bert-VITS2 v2 的语音合成
	- [x] tts/tts_chattts.py 基于 ChatTTS 的语音合成。
	- [x] tts/tts_paddle_speech.py 基于 PaddleSpeech 的语音合成。
- [ ] utility: 杂七杂八

## 4。后台管理系统
计划中的后台管理系统功能如下：
- [ ] 用户管理
	- [x] 注册与登录：
		- [x] register.html：提供用户注册界面，包含用户名、邮箱、密码等信息的输入框，以及注册协议的勾选框。
		- [x] login.html：提供用户登录界面，包含邮箱和密码输入框，支持记住密码功能，同时提供社交账号登录选项。
	- [x] 个人中心：
		- [x] user_profile.html：显示用户的个人信息，包括用户名、姓、名、邮箱等，并允许用户修改和保存这些信息。
		- [x] user_pwd.html: 密码修改功能。
		- [x] 忘记密码
- [ ] 记忆管理
	- [x] 短时记忆
		- [x] memory_shorttime.html：管理短时记忆相关内容。
		- [x] 记忆删除
		- [ ] 记忆查询
		- [ ] 记忆分类
	- [ ] 长时记忆：
		- [ ] memory_longtime.html：管理长时记忆相关内容。
- [ ] 虚拟人管理
	- [x] 虚拟人超市
		- [x] character_role_store.html：提供虚拟人超市的界面。
		- [x] character_role_add.html：用于添加新的虚拟人。
		- [x] character_role_detail.html：查看虚拟人的详细信息。
		- [x] character_role_modify.html：修改虚拟人的信息。
	- [x] 虚拟人角色模板：
		- [x] character_template_store.html：管理虚拟人角色模板。
		- [x] character_template_add.html：用于添加新的虚拟人角色模板。
		- [x] character_template_detail.html：查看虚拟人模板的详细信息。
		- [x] character_template_modify.html：修改虚拟人模板的信息。
	- [ ] 虚拟人人物模型（VRM）：
		- [x] character_model_store.html：管理虚拟人人物模型列表。
		- [x] character_model_add.html：用于添加新的虚拟人人物模型。
	- [x] 虚拟人动作（mixiamo）：
		- [x] character_action_store.html：管理虚拟人动作。
		- [x] character_action_add.html：用于添加新的虚拟人动作。
		- [x] character_action_detail.html：查看虚拟人动作的详细信息。
		- [x] character_action_modify.html：修改虚拟人动作的信息。
	- [x] 虚拟人表情（three.js）
		- [x] character_emotions.html：管理虚拟人表情。针对three.js的13种表情，包括：正常，眨眨眼，开心的，生气的，伤心的，放松的，惊讶的，向上看，向下看，向左看，向右看，眨左眼，眨右眼。
- [ ] 大语言模型管理
	- [x] LLM设定：llm_settings：进行大语言模型的相关设定。
	- [ ] 知识库管理：llm_kb.html：显示知识库列表，包含知识库的ID、名称、文件存储路径、状态、拥有者、加入日期等信息，并提供操作按钮。
	- [ ] 提示词模板：llm_prompt.html：管理大语言模型的提示词模板。
- [ ] 语音合成管理
	- [x] 实时语音合成：tts_live.html：提供语音合成功能，包括输入待转写的文字、选择角色模型、语速、语调、音量等参数，支持转语音和播语音操作。
	- [ ] 文件语音合成：tts_file.html：支持上传单轨的WAV格式、MP3格式的录音件进行语音合成，可选择是否启用热词和敏感词，提交合成任务。
	- [ ] 语音克隆：tts_clone.html：提供语音克隆功能。
	- [ ] 合成设置：tts_settings.html：显示合成语音列表，包含语音的ID、名称、模型、性别、语言等信息，并提供搜索功能。
- [ ] 语音转写管理 - 跟公司的一个产品冲突，暂不准备做。
	- [ ] 实时语音转写：
		- [ ] asr_live.html和asr_live2.html：提供实时语音转写功能，包括输入转写任务的名称、地点、人员等信息，选择是否云端存储、启用热词和敏感词，开始和停止转写操作，显示转写结果。
	- [ ] 文件语音转写：
		- [ ] asr_file.html：支持上传单轨的WAV格式、MP3格式的录音件进行语音转写，可选择是否启用热词和敏感词，提交转写任务。
	- [ ] 数据管理：
		- [ ] minutes_list.html：管理语音转写的数据。
	- [ ] 热词设置：
		- [ ] asr_hotwords.html：进行热词设置。
		- [ ] asr_hotwords_show.html：展示热词信息。
	- [ ] 敏感词设置：
		- [ ] asr_sensiwords.html：进行敏感词设置。
		- [ ] asr_sensiwords_show.html：展示敏感词信息。
- [x] 背景管理
	- [x] 背景列表：background_list.html：显示背景列表，支持选择壁纸、上传和删除背景图片，提供图片预览功能。

# 五、我自己对小落同学的期望
复刻虚拟人生：给自己做一个专属的虚拟人，把TA当作我自己的一个树洞，每天或者每过一段时间把自己想说的话，想说的事，都告诉TA，然后如果某一天我想咨询一件事情的时候，可以去问问TA，看看一旦TA的数据多了后，TA会不会比我自己更懂我？
