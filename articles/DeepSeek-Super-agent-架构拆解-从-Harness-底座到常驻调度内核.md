# DeepSeek Super-agent 架构拆解：从 Harness 底座到常驻调度内核

## 写在前面

前两次分别梳理过 Super-agent 的五个模块和 dsh 这个运行时，但把它们分开看，容易得出一个错误印象：好像 DeepSeek 先做了一个 Agent 运行时，又另起炉灶做了一套多 Agent 调度系统。

把两边的实现文档对着读之后，结论更干脆：**这是同一套系统的三层，不是两个产品。** Super-agent 没有自己实现会话、工具、上下文管理，它只是定义了领域对象和一个调度内核，底下所有"跑起来"的能力都来自 dsh。

这篇只讲架构：对象怎么划分、状态怎么流转、一致性怎么保证、哪些设计是被明确否决过的。发布信息、运营数据、实验跑分一律不展开。

## 一、先把位置摆正

官方公式是 `Agent = Model + Harness`。dsh 是 Harness 这一层——模型之外的工具、权限、会话、主循环，全部做成可替换的插件。

Super-agent 的安装命令直接暴露了它的身份：

```
dsh plugin --profile superagent \
  add "link:$PWD"
```

它是挂在 `superagent` 这个 Profile 下的一个插件包。更硬的证据在实现里：

| 实现细节 | 归属 |
| --- | --- |
| Router 主会话 | dsh Session，Preset 为 `dsh-superagent-router` |
| Worker 会话 | dsh Session，Preset 为 `dsh-superagent-worker` |
| Worker 派生子 Agent | 直接用 dsh 的 `standard` Preset |
| 进度与报告投递 | 走 DeepSeek Harness inbox |
| 长命令不阻塞 | Preset 里配的 5 秒 shell 转后台 |
| 上下文截断与续读 | dsh 的 spill 子系统 |
| 并发控制 | dsh 的 slots 子系统 |

而 Super-agent 自己写的东西，是一个领域模型（Trigger、Thread、Ticket、Mandate……）加一个同步的 Engine。领域文档里有一句很关键的话：**Executor 连同它的 Session 和目录，在领域模型之外，只通过 Assignment 接进来。**

这一刀划得很有意思：会话是实现细节，工单才是业务对象。调度系统不绑定某个运行时，理论上换个 Executor 也能跑。

## 二、底座层：dsh 交出了哪些原语

| 原语 | 提供什么 | Super-agent 拿它做什么 |
| --- | --- | --- |
| Cordis 插件树 | 挂载 / 依赖 / 服务 / 事件 / 卸载清理 | 把整套调度打包成可安装的 bundle |
| Bundle / Profile / Patch | 四层配置叠加 | 一套装配方案定义一个「常驻 Agent」 |
| Session + Preset | 独立会话、工具清单、系统提示词、技能 | Router 与 Worker 的物理隔离、能力白名单 |
| append-only 事件流 | 模型看到什么就记什么，支持 resume / fork / replay | 判断一条消息是否真的被读进历史 |
| spill / compaction | 长内容截断、续读入口、上下文压缩 | 把上下文窗口当 Cache 管 |
| 子 Agent / 后台任务 | 派生会话、shell 转后台、结果唤醒 | Worker 并发、异步执行 |
| 拦截点 / inbox / hooks | step 前后、工具前后可批准改写阻断 | 报告中继、通知、审批 |
| 沙箱三档 | OS 原生隔离与生效报告 | 权限边界（原型里用了最高档） |

值得单独说的是 Preset 的工具裁剪。Router 只拿编排工具，Worker 拿执行工具但**不给**"向人提问""改配置""给其他 Session 发消息"。职责分离不是写在提示词里的，是工具清单里根本没有——这是把架构约束落到了能力层，比任何 prompt 约束都可靠。

## 三、领域模型层：把「常驻」变成可计算的对象

Super-agent 的领域模型只保留工作真正需要的概念，业务属性挂在对象上，不另造实体。核心对象如下：

| 对象 | 定义 | 它守住的规则 |
| --- | --- | --- |
| Source | 事件流；kind 是实现，instance 是一份配置 | 持有读位置与 bot 身份；重启不能重放事件 |
| Trigger | 一次不可变事件 | 可属多个 Thread；同一 Trigger 接两次只产生一个 Ticket |
| Thread | 按时间排序的 Trigger 序列 | 同时最多跑一个 Eval；期间到达的 Trigger 并入下一批 |
| Correlation | 共享 Trigger 的 Thread 之间关系 | 只加上下文，不参与路由 |
| Channel | Thread 的写侧地址 | 回执、回复、PR、评审回复都是写 |
| Policy | 带版本的准入规则 | 规则变了，进行中的 Eval 必须作废重来 |
| Eval | 对一批 Trigger 的判定（Gate + Assessment） | 输入是上下文，输出是 Decision，自身无状态 |
| Mandate | accept 授予的东西 | 策略版本、范围、强度、发起人身份；不可变 |
| Ticket | 一个被授权的工作单元 | 自己定义状态，不跟随 Executor |
| Assignment | Ticket 与一个 Executor 实例的绑定 | 独立于 Ticket 走 pending → running → ended |
| Subscription | Ticket 与 Thread 的多对多关系，由 Thread 持有 | 扇出不校验发送者；人发的消息直接归该 Ticket |

三条规则撑起了整个调度：

**Thread 是串行化的单位**，不是"话题"那么简单。一个 Thread 同时只允许一个 Eval，等价于给每个线索加了一把锁，避免同一件事被并发开出多个工单。

**授权与上下文解耦**。Subscription 只负责把消息送到，不给任何权限；能不能干活由 Mandate 决定。所以一个 Ticket 可以 `followForContext` 订阅别的 Thread 拿信息，但那些消息既不能让它续命，也不能让它认领 follow-up。

**Ticket 自带状态**。它可以被换 Executor、被 resume、被多个 Assignment 先后执行，状态都不依赖 Session。这是常驻系统能长期活着的前提。

### 被否决的概念

领域文档里专门列了一张「Rejected concepts」表，这部分比正面描述更能看出架构功力：

| 被否决 | 为什么 | 换成了什么 |
| --- | --- | --- |
| 把「人」建成实体 / 跨 Source 身份映射 | 身份映射会逼出一套账号系统 | 人只是 Trigger 的 actor 元数据；白名单属于该 Source 的 Policy |
| 一个 Thread 最多一个 live Ticket | 一条线索可以承载几件独立工作 | 允许多个，靠评估时的 Ticket 列表去重 |
| 增加一种「追加到 Ticket」的 Decision | 追加只是消息扇出 | Subscription fan-out，不进 Eval |
| Correlation 参与路由 | 上下文和路由混在一起会失控 | 只加上下文；路由交给 Subscription |
| Ticket 状态跟随 DSH Session | 会话会被交接、恢复、替换 | Ticket 自己定义状态 |
| 策略变更时取消运行中的 Ticket | 会留下一堆半成品 | 记录变更并投递给 Assignment，Mandate 不撤销 |
| 从报告自由文本推断「在等人」 | 分类需要结构化事实 | Executor 通过结构化字段提问 |
| 失败时锁死 Session 全部工具 | 会拒绝人直接在 Session 里继续 | 只暂停自动 Input |

我的判断：这张表的价值在于**每一条都是在砍复杂度**。做常驻系统时最容易犯的错就是概念越加越多，最后状态空间爆炸；这里反过来，凡是能用已有对象表达的一律不新增。

## 四、调度内核：一个同步、单写者、每命令一事务的 Engine

这是最值得细看的一层。

`Runtime`（`src/app/runtime.ts`）只做组装：锁住状态目录、打开 Store、构造各组件、装 hook、恢复中断的 Assignment、启动 passes 和 effects。它**不含任何领域规则**。

`Engine`（`src/core/engine.ts`）是 Trigger、Thread、Decision、Ticket、Assignment 的**唯一写者**。几个硬约束：

- 所有方法**同步**
- 每条命令在一个事务里改完自己的聚合
- `evaluateDue` 为每个变动的 Eval / Ticket 单独开事务
- 端口在事务内**入队**外部工作，适配器在提交后才真正执行
- 非法请求直接抛 `UserError`

最后一条是整个一致性的关键：**外部副作用不在事务里做，只把"要做的事"持久化下来**。于是不需要分布式事务，单进程内就能保证状态一致。这套手法在消息队列系统里很常见，搬到 Agent 调度里同样成立。

### 五个内部 Part，依赖单向

| Part | 管什么 | 依赖 |
| --- | --- | --- |
| Intake | Trigger 入库、挂 Thread、扇出订阅 Ticket、排队 Eval | Tickets |
| Evals | 批处理、Gate 强度、deadline、过期重排、四种 Decision | Tickets |
| Tickets | 创建（含 Mandate / Subscription / 首个 Assignment）、resume、retry、restart、stop、end | Replies |
| Assignments | Executor 上报的事实：启动、Input 送达、中断、Report | Tickets, Replies |
| Replies | 经 Outbox 写回执、回答、结果、attention | 无 |

### 端口与角色裁剪

Engine 从 `ports.ts` 拿六个端口：`Repositories`、Policy getter、`SourceScope`、`Assessor`、`Executor`、`Outbox`。调用方拿到的不是完整 Engine，而是**按角色 Pick 出来的接口**：

```
EngineForSources / EngineForMainSession /
EngineForPeople / EngineForSettings /
EngineForExecutor
```

Source 只能 `receive`，主会话只能 `candidate` / `decide` / `attach`，人只能 `stopTicket` / `retry` / `unsubscribe`，Executor 只能上报 `assignmentStarted` / `inputsDelivered` / `report`。**谁能改什么，是类型系统决定的**，不是运行时检查。

还有个喜欢的细节：命令用祈使句（`stopTicket`），适配层上报的既成事实用过去时（`assignmentStarted`），查询用名词（`candidate`）。命名约定统一之后，读代码时不用查文档就能分清"这是请求"还是"这是事实"。

状态变更后 Engine 发出 `DomainEvents`：`trigger.received`、`eval.started`、`decision.recorded`、`ticket.created`、`ticket.resumed`、`ticket.ended`、`assignment.started`、`assignment.ended`、`thread.subscribed`……面板和通知都挂在这条事件流上，不侵入核心。

### 单写者原则不止在 Engine

| 状态 | 唯一写者 |
| --- | --- |
| 领域聚合 | Engine |
| Source 的读位置 | Source 自己 |
| Outbox 回执 | Outbox |
| 健康记录 | HealthBoard |

一处状态只有一个写者，就不存在"谁覆盖谁"的问题。这在长时间运行、随时可能重启的系统里，比加锁便宜得多。

## 五、运行时：一条 Trigger 走完全程

```
Source 轮询 / 推送
  → receive(t)  # stored / dup / filtered
Intake: 入库、挂 Thread、扇出已订阅 Ticket
  → 排队 Eval（人发的且已命中 Ticket 则不排）
Passes 每 2s：到期 effects → evaluateDue
  → 每个 Thread 取一批 Trigger 合并评估
Gate（规则）：谁可发起、强度 explicit/inferred
  → Assessment（模型）：要不要接
Decision: accept / stop / ignore
          / unavailable
  → 带 reason 码，可解释
accept: 原子创建 Ticket + Mandate
        + Assignment + Subscription + 回执
Worker: 独立 Session(worker-<id>) + 独立目录
  → 5s 后长命令转后台，前台继续接消息
后续评论 → 订阅直通，程序直接投给 Worker
  → 越界 follow-up 走 handback / attach
结果 → Outbox → 原 Channel（PR / 回帖）
Ticket 结束（followsDone：PR 关闭或合并）
  → 未读 follow-up 回落到 Eval
```

两个"回落"最容易被架构图漏掉，但长生命周期系统全靠它不丢任务：

- Ticket 结束时，未被确认、未被回答、未被 handback 的未读消息回到 Eval 重新评估
- Eval 过期会重排，连续两次过期、第三次记 `unavailable`；候选没送达主会话时不会过期

「没人接的消息后来去哪了」必须有确定答案，否则丢任务只是时间问题。

## 六、执行层：状态机与两套时钟

### Ticket stage（自上而下，首条命中即生效）

| Stage | 条件 |
| --- | --- |
| person / delivery | Input 投递失败，2s 起翻倍重试到 1 分钟 |
| person / answer | 有 Attention 待人回答 |
| person / review | 最新 Report 是 `ready` |
| person / blocked, failed | 最新 Report 是 blocked/failed 且无人消息 |
| working / queued | 没有 Assignment 或还在 pending |
| idle | 最新 Report 是 `waiting`，或 Assignment 已结束 |
| working | 其余 |

`person` 开头意味着必须有人介入才能继续。Report 一共六种：`progress`、`waiting`、`ready`、`blocked`、`failed`、`dropped`。

### 并发与后台任务

- 每个 Ticket 从 launch 起占一个 worker slot，turn 期间持续占用
- 并发上限之外**额外留一个 slot 给人的消息或状态请求**：新工作永远挡不住人继续已有工单
- 前台 shell 命令 5 秒后转后台，Worker 就能在下一步收新消息
- turn 结束时若还有后台任务，Ticket 保持 working、不报 waiting；任务完成在同一 slot 唤醒
- 后台任务最多 30 分钟，超时 kill shell job 并报 waiting；subagent 允许继续
- 交接给人（ready / 提问 / blocked / failed）立即释放 slot

### 已读判定与恢复

Input 只有被 Session 取进历史（`user/message` 事件）、且随后有 Report 或 turn 结束，才算 `inputsRead`。被取消的 step 声称拿过但没进历史的不算。这个判定决定重启后要不要重新投递。

恢复路径有三条：

- **retry**：结束当前 Assignment，在同一个 Session、目录、分支、PR 上起一个新的
- **restart**：运行中的 Assignment 记 "host restarted"，新 Assignment 带一条 recovery note——要求 Executor 先查目录、git 历史、GitHub，再决定是否重复外部动作，按最老 Ticket 优先
- **interrupted**：重启时按存储中的 Reports 和 Inputs 重建状态，未取进历史的消息保留

退避参数很具体：relay / delivery 失败 2 秒后重试，之后翻倍到 1 分钟；模型供应商或网络的瞬时失败（408 / 429 / 5xx、连接拒绝重置超时）递增退避重试三次；同类工作连续三次失败才在总览里报系统问题；GitHub 的 404 也重试——因为它可能只是 Agent 丢了私有库权限。

## 七、上下文当缓存：预算是 API 契约

`orchestrator_eval` 返回的是**上下文，不是指令**。评估指令放在 `prompts/admission.md`，规则放在 `runtime/policy`——把策略从提示词里拆出来，策略变更才能触发「作废进行中的 Eval」这类系统行为。

预算全都带硬数字：

| 项 | 值 |
| --- | --- |
| 单次评估带入的 Trigger | 最多 4,000 字符 |
| related tickets | 最多 8 个 |
| Thread 窗口 | 前 5 条 + 两侧各 5 条 |
| 普通消息 | 约 400 字符；紧邻两侧 1,200 |
| 其余消息 | 只给 50 字符 stub |
| 文本分页 | 默认 4,000 UTF-16，上限 8,000 |
| 列表分页 | 默认 20，上限 50 |

展开走 `orchestrator_eval_read`；高频信息内联，长内容截断后留续读入口（spill），每个对象内联"下一跳"ID，可以顺着消息 → Thread → Session → 旧任务一路找回。

我更愿意把这一节读成：**上下文预算被当成 API 契约来管，有硬上限、有分页、有展开接口**，而不是在提示词里写"请注意简洁"。这是提示词工程和系统工程的分界线，也是 dsh 的 spill / compaction 子系统在上层被怎么用掉的。

## 八、支撑层：让「常驻」成立的三件事

**存算分离**：Agent Loop 的计算在云端，状态落在单文件 SQLite，代码仓库和工具链留在用户机器。进程重启、设备离线都能恢复。

**持久化 effect 队列**：`assessment`、`launch`、`delivery`、`relay`、`notice`、`reply` 六类，各有并发度与退避策略。原则是"先存后做"——决定之后要做的中继、投递、启动，先落盘再执行。`launch` 遇到瞬时失败从 5 秒起翻倍到 300 秒重试三次；失败的 turn 在 15 / 30 / 60 秒后收到续接消息。投递按 request id 幂等，重启不重发。

**巡检**：`Passes` 每 2 秒一轮，跑到期的 effect 再 `evaluateDue`；`HealthBoard` 每个部件一条健康记录、唯一写者，某类连续失败三次即报错；另起独立会话做外部 Watchdog，判断各 Worker **有没有实质进展、是不是陷入无效循环**。「卡住了」和「在思考」从接口层看一模一样，只能靠语义判断。

## 九、三处我认为最值得抄的取舍

1. **授权与上下文解耦**。Mandate 管"能不能干、干到什么程度"，Subscription 管"能看到什么"。很多 Agent 框架把两者混在一起，结果订阅一条消息就等于给了权限，越权很难收口。
2. **一致性收敛到单进程**。同步 Engine + 每命令一事务 + 副作用入队提交后执行，避开了分布式事务。代价是 Router 成了单点，但这对研究原型是合理的取舍——先把正确性做对，再谈水平扩展。
3. **能力隔离落在类型和工具清单上**。角色 `Pick` 决定谁能调哪个方法，Preset 白名单决定 Worker 有哪些工具。都不依赖模型"记得自己是调度器"。

反面也要说清楚：Router 单点、存储无界增长、多 Worker 冲突只做到"互相看得见"没有仲裁、权限面靠 `danger-full-access` 加运维纪律撑着，这些都不是遗漏，是原型阶段明确没做的事。实验也只测调度、不测真实编码质量，别把 p95 从 29.5 分钟降到 15.7 分钟读成"编码能力翻倍"。

## 十、如果要自己搭：最小骨架

把上面收敛成可照着实现的结构，大概是这个形状：

```
Source(幂等读位置)
  → Intake: 存一次、挂 Thread、扇出订阅者
  → Thread: 单 Eval 队列，期间 Trigger 合批
  → Gate(确定性规则) → Assessment(模型)
  → Decision(带 reason 码)
  → Ticket(Mandate 不可变, 自定义状态)
  → Executor(独立 Session + 独立目录)
  → Outbox(幂等回执)

旁路:
  Store        单文件状态，唯一写者
  Effects      持久化队列，先存后做
  Passes       周期巡检 + 外部语义 Watchdog
```

三个必须先想清楚的问题：**Thread 的边界由谁定义**（决定评估的一致性）、**Ticket 的状态是否独立于会话**（决定能否长期存活）、**副作用怎么出事务**（决定重启后会不会重复执行）。这三个答完，剩下的都是工程量的事。

## 延伸阅读

- DeepSeek Harness：deepseek.com/harness
- 运行时仓库：github.com/deepseek-ai/deepseek-harness（docs/subsystems 下有各子系统实现说明）
- Super-agent 原型：github.com/deepseek-ai/dsh-superagent-prototype（docs/000–008）

---

## 关注公众号

更多 AI Agent 面试题在公众号持续更新。微信扫码关注 **FullStack 研发派**，后台回复「题库」，可以领取完整目录。

<img src="assets/wechat-qr.jpg" alt="FullStack 研发派" width="220" />
