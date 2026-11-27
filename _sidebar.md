- [首页](README.md)

- 1、基础认知与技术选型
  - [001 RAG 和微调（SFT）的核心区别是什么？能不能一起用？](articles/001-RAG-和微调-SFT-的核心区别是什么-能不能一起用.md)
  - [002 大模型应用上线前你最关心哪些工程指标？](articles/002-大模型应用上线前你最关心哪些工程指标.md)
  - [003 什么是 AI Agent？它和传统 AI 应用的区别是什么？](articles/003-什么是-AI-Agent-它和传统-AI-应用的区别是什么.md)
  - [004 Token 和上下文窗口是什么？它们在工程上意味着什么？](articles/004-Token-和上下文窗口是什么-它们在工程上意味着什么.md)
  - [005 什么时候该用 Prompt、RAG、微调、Workflow、Agent？](articles/005-什么时候该用-Prompt-RAG-微调-Workflow-Agent.md)

- 2、Prompt、结构化输出与护栏
  - [006 System Message 和 User Message 应该怎么分工？](articles/006-System-Message-和-User-Message-应该怎么分工.md)
  - [007 如何做 Prompt 版本管理与回归？](articles/007-如何做-Prompt-版本管理与回归.md)
  - [008 结构化输出有哪些常见做法？各自的优缺点是什么？](articles/008-结构化输出有哪些常见做法-各自的优缺点是什么.md)
  - [009 Prompt 工程的边界是什么？为什么不能把一切问题都交给 Prompt？](articles/009-Prompt-工程的边界是什么-为什么不能把一切问题都交给-Prompt.md)
  - [010 Prompt Injection 是什么？为什么 RAG / Agent 场景更要小心？](articles/010-Prompt-Injection-是什么-为什么-RAG-Agent-场景更要小心.md)
  - [011 Prompt Engineering 中，如何系统优化提示词并把准确率做上去？](articles/011-Prompt-Engineering-中-如何系统优化提示词并把准确率做上去.md)

- 3、RAG 全链路
  - [012 有了超长上下文模型，还需要 RAG 吗？](articles/012-有了超长上下文模型-还需要-RAG-吗.md)
  - [013 为什么企业项目里的 RAG 必须重视权限、版本和引用？](articles/013-为什么企业项目里的-RAG-必须重视权限-版本和引用.md)
  - [014 什么是 Agentic RAG？它和「一次检索后直接生成」有什么区别？](articles/014-什么是-Agentic-RAG-它和「一次检索后直接生成」有什么区别.md)
  - [015 请描述一个完整的 RAG 流水线。](articles/015-请描述一个完整的-RAG-流水线.md)
  - [016 RAG 应该如何接入 Agent 执行链路？](articles/016-RAG-应该如何接入-Agent-执行链路.md)
  - [017 什么是 Lost in the Middle？它对 RAG 设计有什么启示？](articles/017-什么是-Lost-in-the-Middle-它对-RAG-设计有什么启示.md)
  - [018 文本切块应该怎么设计？有哪些常见坑？](articles/018-文本切块应该怎么设计-有哪些常见坑.md)
  - [019 混合检索、重排序和查询改写分别解决什么问题？](articles/019-混合检索-重排序和查询改写分别解决什么问题.md)
  - [020 复杂文档 RAG 或多模态 RAG 应该怎么做？](articles/020-复杂文档-RAG-或多模态-RAG-应该怎么做.md)
  - [021 RAG 效果不好时，你会怎么排查？](articles/021-RAG-效果不好时-你会怎么排查.md)

- 4、检索基础设施与检索优化
  - [022 GraphRAG 适合什么场景？和传统向量 RAG 怎么选？](articles/022-GraphRAG-适合什么场景-和传统向量-RAG-怎么选.md)
  - [023 什么是向量数据库？它和传统数据库有什么区别？为什么不能只用 MySQL？](articles/023-什么是向量数据库-它和传统数据库有什么区别-为什么不能只用-MySQL.md)
  - [024 近似检索和精确检索怎么权衡？](articles/024-近似检索和精确检索怎么权衡.md)
  - [025 如何选择一个合适的 Embedding 模型？评估它好坏看什么？](articles/025-如何选择一个合适的-Embedding-模型-评估它好坏看什么.md)
  - [026 Embedding 是什么？它在应用开发里最核心的价值是什么？](articles/026-Embedding-是什么-它在应用开发里最核心的价值是什么.md)
  - [027 在什么场景下，知识图谱或图数据库比纯向量检索更有价值？](articles/027-在什么场景下-知识图谱或图数据库比纯向量检索更有价值.md)

- 5、Tools、Function Calling 与 Agent
  - [028 Tool、Function Calling、Agent 三者是什么关系？](articles/028-Tool-Function-Calling-Agent-三者是什么关系.md)
  - [029 ReAct 模式是什么？它解决了什么问题？](articles/029-ReAct-模式是什么-它解决了什么问题.md)
  - [030 什么是“工具幻觉”？工程上怎么缓解？](articles/030-什么是-工具幻觉-工程上怎么缓解.md)
  - [031 设计 Tool：粒度、命名、幂等这几点怎么定？](articles/031-设计-Tool-粒度-命名-幂等这几点怎么定.md)
  - [032 搭一个能落地的 Agent：哪些组件真必要，哪些是过度设计？](articles/032-搭一个能落地的-Agent-哪些组件真必要-哪些是过度设计.md)
  - [033 如果让你实现一个"查天气、查新闻"的 AI 助手，你会怎么设计？](articles/033-如果让你实现一个-查天气-查新闻-的-AI-助手-你会怎么设计.md)
  - [034 一条 tool_calls 消息是怎么跑完的？Function Calling 原理拆解](articles/034-一条-tool_calls-消息是怎么跑完的-Function-Calling-原理拆解.md)
  - [035 Function Calling 和“让模型输出 JSON 再自己解析”有什么区别？](articles/035-Function-Calling-和-让模型输出-JSON-再自己解析-有什么区别.md)
  - [036 当工具很多时，如何控制上下文长度和调用稳定性？](articles/036-当工具很多时-如何控制上下文长度和调用稳定性.md)

- 6、Agent 框架与编排：LangChain、LCEL、LangGraph
  - [037 LangGraph 的 State / Node / Edge：怎么拼出一个能跑的 Agent？](articles/037-LangGraph-的-State-Node-Edge-怎么拼出一个能跑的-Agent.md)
  - [038 LCEL 不只是语法糖：它到底帮你省了什么？](articles/038-LCEL-不只是语法糖-它到底帮你省了什么.md)
  - [039 用 LangChain 搭 Agent：一条最小可跑链路长什么样？](articles/039-用-LangChain-搭-Agent-一条最小可跑链路长什么样.md)
  - [040 LangGraph 相比普通 Workflow 或链式调用，最大的价值是什么？](articles/040-LangGraph-相比普通-Workflow-或链式调用-最大的价值是什么.md)
  - [041 LangGraph 的进阶特性里，你觉得最有工程价值的是哪些？](articles/041-LangGraph-的进阶特性里-你觉得最有工程价值的是哪些.md)
  - [042 Checkpoint / HITL / Time-Travel：三个特性在真实项目里怎么用？](articles/042-Checkpoint-HITL-Time-Travel-三个特性在真实项目里怎么用.md)
  - [043 现在还需要 LangChain 吗？为什么不是直接手写 SDK 就够了？](articles/043-现在还需要-LangChain-吗-为什么不是直接手写-SDK-就够了.md)

- 7、记忆、MCP 与多智能体
  - [044 MCP 调用如何保证并发？](articles/044-MCP-调用如何保证并发.md)
  - [045 MCP 到底解决了什么？它和 Tool / RAG / Agent 的边界在哪？](articles/045-MCP-到底解决了什么-它和-Tool-RAG-Agent-的边界在哪.md)
  - [046 手写一个 MCP Server：从暴露工具到跑通调用](articles/046-手写一个-MCP-Server-从暴露工具到跑通调用.md)
  - [047 短期记忆 vs 长期记忆：Agent 的记忆该怎么分层落地？](articles/047-短期记忆-vs-长期记忆-Agent-的记忆该怎么分层落地.md)
  - [048 MCP 的流式 HTTP 传输核心优势是什么？](articles/048-MCP-的流式-HTTP-传输核心优势是什么.md)
  - [049 Agent 应该如何接入 MCP 工具？](articles/049-Agent-应该如何接入-MCP-工具.md)
  - [050 A2A 和 MCP 的区别是什么？什么时候需要多智能体？](articles/050-A2A-和-MCP-的区别是什么-什么时候需要多智能体.md)
  - [051 MCP 的能力、消息、传输到底怎么分工？面试别只背四层名字](articles/051-MCP-的能力-消息-传输到底怎么分工-面试别只背四层名字.md)
  - [052 MCP 工具那么多，面试到底该说哪几个？按四类讲才不露怯](articles/052-MCP-工具那么多-面试到底该说哪几个-按四类讲才不露怯.md)
  - [053 如何为 Agent 设计短期记忆和长期记忆系统？技术上通常怎么落地？](articles/053-如何为-Agent-设计短期记忆和长期记忆系统-技术上通常怎么落地.md)
  - [054 MCP vs Function Calling：一个是协议，一个是能力，别混着说](articles/054-MCP-vs-Function-Calling-一个是协议-一个是能力-别混着说.md)
  - [055 MCP 是如何做到跨平台兼容的？](articles/055-MCP-是如何做到跨平台兼容的.md)

- 8、平台实践与框架选型：Coze、Dify、RAGFlow
  - [056 Coze / Dify vs LangChain / LangGraph：零代码平台和代码框架怎么选？](articles/056-Coze-Dify-vs-LangChain-LangGraph-零代码平台和代码框架怎么选.md)
  - [057 用 Python 调用 Dify / Coze 工作流时，最值得关注哪些工程细节？](articles/057-用-Python-调用-Dify-Coze-工作流时-最值得关注哪些工程细节.md)
  - [058 什么时候工作流比 Agent 更合适？](articles/058-什么时候工作流比-Agent-更合适.md)
  - [059 开源 RAG 平台比如 RAGFlow，应该如何选型？和 Dify 或自研链路怎么比较？](articles/059-开源-RAG-平台比如-RAGFlow-应该如何选型-和-Dify-或自研链路怎么比较.md)
  - [060 各类 Agent 开发框架应该如何选取？](articles/060-各类-Agent-开发框架应该如何选取.md)

- 9、安全、评测、部署与可观测性
  - [061 控制大模型应用成本，你会优先从哪些层面下手？](articles/061-控制大模型应用成本-你会优先从哪些层面下手.md)
  - [062 Agent 链路耗时很长时，如何定位性能瓶颈？](articles/062-Agent-链路耗时很长时-如何定位性能瓶颈.md)
  - [063 模型路由应该怎么做？](articles/063-模型路由应该怎么做.md)
  - [064 内网环境下怎么设计 Agent / RAG 系统？](articles/064-内网环境下怎么设计-Agent-RAG-系统.md)
  - [065 大模型幻觉压不掉？应用层能做的几道防线](articles/065-大模型幻觉压不掉-应用层能做的几道防线.md)
  - [066 你会怎么做大模型应用的可观测性？](articles/066-你会怎么做大模型应用的可观测性.md)
  - [067 意图识别 / 任务路由应该怎么做？](articles/067-意图识别-任务路由应该怎么做.md)
  - [068 Agent 上线后该盯哪些指标？只看成功率为什么不够](articles/068-Agent-上线后该盯哪些指标-只看成功率为什么不够.md)
  - [069 Agent 会不会乱来？给它的行为划几道边界](articles/069-Agent-会不会乱来-给它的行为划几道边界.md)
  - [070 RAG 上线后才会遇到的坑：从检索到权限](articles/070-RAG-上线后才会遇到的坑-从检索到权限.md)
  - [071 多用户场景下，如何为 Agent 做安全沙箱隔离？](articles/071-多用户场景下-如何为-Agent-做安全沙箱隔离.md)
  - [072 你会如何评估一个 RAG 或 Agent 系统的效果？](articles/072-你会如何评估一个-RAG-或-Agent-系统的效果.md)

- 10、典型业务场景设计题
  - [073 如何设计类 Manus 通用智能体？](articles/073-如何设计类-Manus-通用智能体.md)
  - [074 如何设计一个 Deep Research 系统？](articles/074-如何设计一个-Deep-Research-系统.md)
  - [075 如何设计 Agent 的完成判断与终止条件，避免过早结束？](articles/075-如何设计-Agent-的完成判断与终止条件-避免过早结束.md)
  - [076 如何开发浏览器自动化 Agent？](articles/076-如何开发浏览器自动化-Agent.md)
  - [077 如果让你设计一个客服智能体，你会优先考虑哪些能力？](articles/077-如果让你设计一个客服智能体-你会优先考虑哪些能力.md)
  - [078 Code Agent 怎么设计？](articles/078-Code-Agent-怎么设计.md)
  - [079 能操作环境的 Agent，和只能调工具的 Agent 差在哪？](articles/079-能操作环境的-Agent-和只能调工具的-Agent-差在哪.md)
  - [080 如果让你设计一个 Deep Research 系统，它和普通 RAG 有什么不同？](articles/080-如果让你设计一个-Deep-Research-系统-它和普通-RAG-有什么不同.md)
  - [081 如何设计 Python 代码解释器？](articles/081-如何设计-Python-代码解释器.md)
  - [082 如果让你设计一个 NL2SQL Agent，你会重点控制哪些风险？](articles/082-如果让你设计一个-NL2SQL-Agent-你会重点控制哪些风险.md)
  - [083 如果让你设计一个企业知识库问答系统，你会怎么做？](articles/083-如果让你设计一个企业知识库问答系统-你会怎么做.md)

- 11、项目表达与面试实战
  - [084 面试官让你介绍一个做过的 RAG / Agent 项目，你应该怎么讲？](articles/084-面试官让你介绍一个做过的-RAG-Agent-项目-你应该怎么讲.md)
  - [085 如果面试官问"你们为什么不用某个更热门的框架或模型"，怎么回答更稳？](articles/085-如果面试官问-你们为什么不用某个更热门的框架或模型-怎么回答更稳.md)
  - [086 如果线上效果波动很大，你怎么向面试官展示你的排障能力？](articles/086-如果线上效果波动很大-你怎么向面试官展示你的排障能力.md)

- 12、工具生态与岗位认知
  - [087 你常用哪些 AI 开发工具？各自适合什么场景？](articles/087-你常用哪些-AI-开发工具-各自适合什么场景.md)
  - [088 如果让你总结"AI 应用工程师"和"算法研究岗"的差异，你会怎么说？](articles/088-如果让你总结-AI-应用工程师-和-算法研究岗-的差异-你会怎么说.md)
  - [089 Cursor、Claude Code、Copilot 这类 AI 编码工具的差异该怎么理解？](articles/089-Cursor-Claude-Code-Copilot-这类-AI-编码工具的差异该怎么理解.md)

- 专题
  - [GitHub 上最火的 20 个 AI 项目：一半在造技能，一半在修地基](articles/GitHub-上最火的-20-个-AI-项目-一半在造技能-一半在修地基.md)
  - [Super-agent 五模块架构拆解：让 Agent 从「单次会话」走向「持续在线」](articles/Super-agent-五模块架构拆解-让-Agent-从「单次会话」走向「持续在线」.md)
  - [DeepSeek 开源 SuperAgent：你只提需求，AI 自己开会话、自己派活](articles/DeepSeek-开源-SuperAgent-你只提需求-AI-自己开会话-自己派活.md)
  - [DeepSeek Harness 是什么？](articles/DeepSeek-Harness-是什么.md)
  - [SAG2 完整梳理：不用向量、不调大模型建库，多跳检索怎么反而更准](articles/SAG2-完整梳理-不用向量-不调大模型建库-多跳检索怎么反而更准.md)
  - [DeepSeek Super-agent 架构拆解：从 Harness 底座到常驻调度内核](articles/DeepSeek-Super-agent-架构拆解-从-Harness-底座到常驻调度内核.md)
