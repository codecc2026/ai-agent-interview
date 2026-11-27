# GitHub 上最火的 20 个 AI 项目：一半在造技能，一半在修地基

翻一遍这周的 GitHub Trending，会发现一个和去年很不一样的现象：排在前面的 AI 项目，几乎没有一个是"新模型"。取而代之的是一堆名字里带 `skill`、`mcp`、`agent` 的仓库——它们不训练模型，只负责把模型接到具体的活上。

再看累计 Star 的常青榜，稳坐头名的还是 Ollama、Transformers 这类老面孔，两年过去位置几乎没动。一个追的是本周最热，一个看的是长期地基，两张榜单叠在一起，AI 开源现在的样子就清楚了。

**把两张榜单放一起看，2026 年 AI 开源的主线只有一句：模型本身不再是主角，围绕模型的工程——技能、协议、工具链、本地部署——才是。**

先把口径说清楚。下面两张榜单的 Star 数据来自 GitHub 官方 Trending 周榜和多个 AI 项目聚合榜单，截至 2026 年 11 月中下旬。Star 是个热度信号，不是质量评分，数字每天在变，看量级和相对位置就好，别当成精确的实时值。

## 一、本周飙升榜：11 个正在快速涨的项目

这 11 个按本周新增 Star 排。它们不是同一类东西，硬排成一条榜反而看不出门道，拆成三组才清楚：技能包、协议与工具链、大厂下场的底座。

### 第一组：Agent Skills，把能力打包成可插拔的技能

先解释一下这组共同的底子。Skill 是给编码 Agent 用的一个能力包：一个约定好的目录，里面写清楚什么情况下该用它、按什么步骤做、需要时再翻哪些参考文档。Agent 遇到匹配的场景就自动加载，不用你把整套说明每次都塞进对话。这组项目里的 `stitch-skills`、`last30days-skill`、`ffmpeg-skill`、`claude-trading-skills`，走的都是这个路子。

**google-labs-code/stitch-skills**（本周 +1.8k，TypeScript，累计约 1.07 万 Star）是 Google Labs 出的技能库，配合 Stitch 的 MCP server 用。它遵循 Agent Skills 的开放标准，所以 Antigravity、Gemini CLI、Claude Code、Cursor 这些编码 Agent 都能认。它卖的不是某个单点能力，而是"设计到代码"这条链路——把设计意图通过 MCP 传给编码 Agent，让两边说同一种话。想观察大厂怎么定义技能规范，这个仓库值得当范本读。

**mvanhorn/last30days-skill**（本周 +3.2k，Python，累计约 7.08 万 Star）做的是调研。给它一个话题，它跨 Reddit、X、YouTube、Hacker News、Polymarket 和全网把最近的材料捞一遍，再综合成一份有出处的摘要。它涨得快有个现实原因：做技术选型或追一个热点时，人肉翻十个平台太慢，这种"跨平台近 30 天扫描"正好补上那段最费时间的检索。

**kajisho5/ffmpeg-skill**（本周 +3.0k，Python，累计约 8300 Star）把 FFmpeg 的 42 个工具封成一份机器可读的 contract，再挂一个 MCP server，专门给 Claude Code、Cursor、Codex 用。剪辑、加字幕、改画幅、响度处理、平台导出都能让 Agent 直接调。它的关键取舍是"全本地、无云、无需 API key"——视频素材不出本机，这点对隐私敏感的场景很实在。

**tradermonty/claude-trading-skills**（本周 +3.4k，Python，累计约 7200 Star）面向股票投资者，打包了市场分析、技术图表、经济日历、选股器和交易策略开发这些技能。它和上一个技能合成一组信号：Skills 的竞争已经细分到具体工种，从设计、剪辑到调研、交易，每个垂直领域都在被拆成可复用的能力包。

### 第二组：协议与工具链，让 Agent 能接进来、看得见、审得动

这组不直接给 Agent 加能力，而是解决"怎么接、怎么看、怎么审"的工程问题。

**ag-ui-protocol/ag-ui**（本周 +3.5k，TypeScript，累计约 2.06 万 Star）是 AG-UI 协议，全称 Agent-User Interaction Protocol，管的是 Agent 和前端应用之间怎么交互。做过 Agent 应用的人会遇到一个麻烦：后端 Agent 跑起来是一回事，把它接进前端、把状态流式推给界面、让用户在过程中介入是另一回事，每个框架各搞一套。AG-UI 想做的就是这个位置的通用协议，让前端不用为每种 Agent 重写一套适配。

**ChromeDevTools/chrome-devtools-mcp**（本周 +3.2k，TypeScript，累计约 5.84 万 Star）是 Google 官方维护的 MCP server，把 Chrome DevTools 开放给编码 Agent。Agent 写的网页到底有没有报错、网络请求成没成、DOM 长什么样，以前要人肉截图贴回去，现在 Agent 能自己打开 DevTools 去看。累计 Star 能到 5 万这个量级，说明它已经不是尝鲜工具，而是进了不少人的日常开发环。

**backnotprop/plannotator**（本周 +3.5k，TypeScript，累计约 1.37 万 Star）是一个围绕 Agent 的工作区：先把任务规划出来，再在上下文里做决策、标注、审阅代码，最后一键把反馈发回给 Agent。它切的是人机协作里最容易出现的一个断点——人看完 Agent 的产出想给反馈，却要在聊天框里重新描述一遍上下文。把标注和反馈做成工作流的一部分，这个痛点就顺了。

**alibaba/open-code-review**（本周 +4.5k，Go，累计约 5.44 万 Star）是阿里开源的代码审查工具，架构上走"确定性流水线 + LLM Agent"的混合路线。确定性的部分跑规则：空指针、线程安全、XSS、SQL 注入这些内置的多语言规则集；LLM 的部分负责需要理解上下文的判断，给出精确到行的评论。它兼容 OpenAI 和 Anthropic 的接口，在阿里自己的规模上做过实战。这组里它涨得最快，反映出一个共识：AI 代码审查要落地，光靠模型不行，得让规则和模型分工。

### 第三组：大厂下场，直接做底座

这组三个都有一个共同标签：TypeScript，而且来自大厂。它们做的不是某个 Agent 应用，而是别人搭 Agent 时会踩到的那层地基。

**dream-num/univer**（本周 +7.2k，也就是说这一周它涨得比榜上任何项目都多，累计约 3.04 万 Star）把定位写得很直白：用 Univer Office SDK 搭你自己的 AI Office。它把表格的编辑、计算、协作和文件处理做成一套可扩展的开源内核，让这些能力既能给人用，也能给 Agent 用。想象一下让 Agent 直接读写一张带公式的表、并且改动能被协作系统追踪——这需要的不是一段提示词，而是一套 Office 内核，Univer 做的就是这层。

**GoogleChrome/modern-web-guidance-src**（本周 +6.9k，累计约 9100 Star）解决的是一个很具体的毛病：编码 Agent 的训练数据有滞后，写出来的前端代码常常停留在几年前的最佳实践。这个仓库把最新的 Web 开发规范整理成机器可读的指引，让 Agent 能随时取用。它的累计 Star 不算高但周涨很猛，说明"让 Agent 跟上最新规范"这件事刚被广泛意识到。

**meta/astryx**（本周 +5.0k，累计约 3.1 万 Star）是 Meta 开源的设计系统，卖点是完全可定制、并且 agent-ready。设计系统和 Agent 的关系在于：当界面要由 Agent 生成或改动时，一套结构清晰、语义明确的设计 token 和组件约定，能大幅降低 Agent 生成出"看着对、细节全错"的界面的概率。大厂把自己内部的设计系统开源出来给 Agent 用，这个动作本身比项目细节更值得注意。

## 二、常青顶流榜：9 个项目撑起的地基

飙升榜看的是风往哪吹，常青榜看的是哪些东西已经成了基础设施。这 9 个按累计 Star 排，同样分三组。

### 第一组：本地推理三件套

**ollama/ollama**（约 18.7 万 Star，Go）是本地跑模型的入口级工具。一行命令把 Llama、Qwen、DeepSeek、Gemma 这些模型拉起来，剩下的 GPU 调度、量化、接口服务它都包了。它常年占着 AI 类项目 Star 榜首，靠的是把"在自己机器上跑一个模型"这件曾经很折腾的事，压到了几乎零门槛。隐私、离线、成本可控这三个诉求，让它的基本盘一直稳。

**open-webui/open-webui**（约 15.9 万 Star，Svelte）是自托管的 AI 对话前端，支持 Ollama 和 OpenAI API。它几乎成了 Ollama 的标配界面——本地模型跑起来之后，总要有个能聊天、能管知识库、能切模型的界面，Open WebUI 就把这个位置占了。它和 Ollama 一个管后端一个管前端，常年一起出现在各自的 Star 榜里，是本地 AI 组合里最稳的一对。

**vllm-project/vllm**（约 9.7 万 Star，Python）和上面两个方向不同，它做的是服务端的高吞吐推理。通过 PagedAttention 这类机制把显存利用和吞吐做上去，是生产环境部署 LLM 推理服务时的首选之一。本地跑模型用 Ollama，要对外提供高并发服务就换 vLLM，这条分工线在实践中相当清楚。

### 第二组：模型与应用框架

**huggingface/transformers**（约 16.9 万 Star，Python）是文本、视觉、音频、多模态模型的定义框架，覆盖推理和训练。它更像是整个现代 AI 生态的一个公共底座——大量后续项目和论文都以它为起点。在 Agent 成为主线的今天它依然排在常青榜前列，说明不管上层怎么变，模型这一层的标准件位置没动摇过。

**langchain-ai/langchain**（约 15.0 万 Star，Python）把自己定位成 Agent 工程平台。工具调用、状态管理、链式编排这些做 Agent 绕不开的东西，它提供得最全，生态也最大。它常被拿来和各类新框架比较，优势是覆盖广、文档全，代价是抽象层多——项目大了之后要清楚它在你架构里到底承担哪一层，别把什么都往上堆。

**langgenius/dify**（约 16.1 万 Star，Python）是 LLM 应用开发平台，主打可视化编排 Agent 工作流和 RAG 流水线，模型与工具接得多，既能云上用也能自托管。它和 LangChain 的差别在于面向的人：LangChain 更像给工程师的库，Dify 更偏低代码，让团队里不写代码的人也能搭出一套应用。企业想把原型快速推到生产，这类平台很对路。

### 第三组：三个垂直方向的爆款

**harry0703/MoneyPrinterTurbo**（约 14.5 万 Star，Python）是个中文项目，按一个主题或关键词一键生成高清短视频，背后是一套 AI 大模型加自动化工作流。它的 Star 能冲到这个量级，说明"输入一句话、出一条成片"这种内容生产自动化，需求面比想象中广。

**TauricResearch/TradingAgents**（约 12.3 万 Star，Python）是多 Agent 协作的金融交易框架。它把交易分析拆成不同角色的 Agent 分工协作，是研究"多 Agent 怎么配合完成一个复杂决策"的典型样本。它和飙升榜里的 trading-skills 凑成一组：一个做框架，一个做可插拔技能，金融是这个周期里 Agent 落地最积极的场景之一。

**browser-use/browser-use**（约 12.1 万 Star，Python）让 AI 真正操控浏览器：导航、填表、处理验证码、完成一整套任务。很多没有 API 的旧系统，最后只能靠浏览器去操作，这个位置短期内替代不了。它把"Agent 碰到真实世界"这件事落到了一个具体且高频的入口上。

## 三、两张榜单速览

飙升榜看本周增量：

| 项目 | 本周新增 | 类别 | 一句话定位 |
| --- | --- | --- | --- |
| dream-num/univer | +7.2k | 大厂底座 | 可自建 AI Office 的开源 SDK |
| GoogleChrome/modern-web-guidance-src | +6.9k | 大厂底座 | 让编码 Agent 跟上最新 Web 规范 |
| meta/astryx | +5.0k | 大厂底座 | 完全可定制、agent-ready 的设计系统 |
| alibaba/open-code-review | +4.5k | 工具链 | 规则 + LLM Agent 混合代码审查 |
| backnotprop/plannotator | +3.5k | 工具链 | 规划、标注、审阅代码的工作区 |
| ag-ui-protocol/ag-ui | +3.5k | 协议 | Agent 与前端交互的通用协议 |
| tradermonty/claude-trading-skills | +3.4k | 技能包 | 面向投资者的交易分析 Skills |
| ChromeDevTools/chrome-devtools-mcp | +3.2k | 工具链 | 给编码 Agent 的 Chrome DevTools |
| mvanhorn/last30days-skill | +3.2k | 技能包 | 跨平台近 30 天调研汇总 |
| kajisho5/ffmpeg-skill | +3.0k | 技能包 | 本地视频剪辑的 FFmpeg 技能 |
| google-labs-code/stitch-skills | +1.8k | 技能包 | 配合 Stitch MCP 的设计技能库 |

常青榜看累计存量：

| 项目 | 累计 Star | 分组 | 定位 |
| --- | --- | --- | --- |
| ollama/ollama | 约 18.7 万 | 本地推理 | 一行命令本地跑模型 |
| huggingface/transformers | 约 16.9 万 | 模型框架 | 多模态模型定义框架，事实标准 |
| langgenius/dify | 约 16.1 万 | 应用平台 | 低代码编排 Agent 与 RAG |
| open-webui/open-webui | 约 15.9 万 | 本地推理 | 自托管 AI 对话前端 |
| langchain-ai/langchain | 约 15.0 万 | 应用框架 | Agent 工程平台，生态最全 |
| harry0703/MoneyPrinterTurbo | 约 14.5 万 | 垂直爆款 | 一键生成短视频 |
| TauricResearch/TradingAgents | 约 12.3 万 | 垂直爆款 | 多 Agent 金融交易框架 |
| browser-use/browser-use | 约 12.1 万 | 垂直爆款 | AI 操控浏览器 |
| vllm-project/vllm | 约 9.7 万 | 服务端推理 | 高吞吐 LLM 推理引擎 |

## 四、从这份榜单里能读出什么

三个判断，比我逐个夸项目更有用。

**技能化是当下最明确的一条线。** 飙升榜 11 个里有 4 个是技能包，加上榜单之外还有一批同方向的仓库在涨。竞争焦点已经从"做一个 Agent 产品"变成"做能被任意 Agent 复用的能力包"，而且细分到具体工种：设计、剪辑、调研、交易各有人做。判断一个技能包值不值得用，看两点就够——触发条件写得清不清、有没有把不必要的文档做成按需加载。

**大厂在抢 Agent 的地基。** Google 出最佳实践和技能库，Meta 出设计系统，阿里出代码审查，而且清一色 TypeScript。这些都不是终端应用，而是别人搭 Agent 时会反复踩到的那几层。大厂把自己内部的规范开源出来，一方面是生态卡位，另一方面也说明这些层已经稳定到可以标准化了。对普通开发者，这些仓库是最好的免费教材——照着大厂怎么组织 skill、怎么定设计 token，比自己摸快得多。

**本地和服务端的分工已经定型。** 常青榜里 Ollama、Open WebUI、vLLM 各占一格：本地跑模型、本地对话界面、服务端高并发推理。想动手试，最短路径就是把前两个组合起来，几分钟能在自己机器上起一套。下面这段是通用起步命令，具体参数以各自 README 为准：

```bash
# 1. 用 Ollama 拉起一个本地模型
ollama pull qwen2.5:7b
ollama run qwen2.5:7b

# 2. 用 Open WebUI 套一个 Web 界面（Docker 方式）
docker run -d -p 3000:8080 \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  -v open-webui:/app/backend/data \
  --name open-webui ghcr.io/open-webui/open-webui:main
```

跑起来之后打开 3000 端口，就能在界面里切模型、传文档。这条路径把常青榜里两个项目的价值一次体验到，比单看介绍直观。

顺带说清楚 Skill 长什么样，免得这个最常见的词一直模糊着。一个技能包通常就是一个目录：

```text
my-skill/
├── SKILL.md          # 必需：什么时候用、按什么步骤做
└── references/       # 可选：体积大、按需才读的参考文档
```

`SKILL.md` 里写的是触发条件和执行步骤，Agent 匹配到场景才加载；`references/` 里放详细资料，用到才读。这个"渐进式披露"的结构，就是 Skill 能把大段专业知识塞给 Agent、又不把上下文撑爆的关键。

## 写在最后

两张榜单，一个在造技能，一个在修地基，看起来是两个方向，其实是一件事的两头。地基那 9 个项目把模型怎么跑、应用怎么搭、浏览器怎么控这些底层问题解决了，上面才有空间长出 11 个五花八门的技能包。

如果只能带走一条建议：别追着周榜挨个 clone。先看常青榜里和你的场景对得上的那一两个，把它真正用起来；等遇到具体痛点，再去飙升榜里找有没有人已经把这个痛点做成了技能。榜单的价值是帮你缩小范围，不是替你做选择。

---

## 关注公众号

更多 AI Agent 面试题在公众号持续更新。微信扫码关注 **FullStack 研发派**。

<img src="assets/wechat-qr.jpg" alt="FullStack 研发派" width="220" />
