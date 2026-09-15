# CLAUDE.md

Claude Code 自动加载的项目指令。完整的 agent harness 见 [AGENTS.md](AGENTS.md)。

## MCP 约束：Linear 只能用个人 workspace

**本项目只允许使用 `mcp__linear-personal__*`。**

本机配置了两个 Linear MCP，指向同一个 URL 但持有各自独立的 OAuth 凭据：

| server | workspace | 本项目 |
|---|---|---|
| `linear-company` | **公司** | 🚫 禁止使用 |
| `linear-personal` | **个人** | ✅ 唯一允许 |

两个名字都显式标了归属，不存在没后缀的歧义条目 —— 看到 `mcp__linear-company__*` 就是公司的，本项目一律不碰。

具体说，在本项目里不要用公司 workspace 做任何事：不建 issue、不改 issue、不读公司数据、不把本项目的任何信息写进去。混淆个人项目与公司项目不可接受。

分不清某个 Linear 工具属于哪个 workspace 时，**停下来问，不要猜**。

## Linear 条目归 microduck-rebuild team

本项目的 issue 与 project 必须建在个人 workspace 的 **`microduck-rebuild`** team（identifier `MDR`）下，编号形如 `MDR-1`。

⚠️ **Linear 的 issue 前缀取自 team key，不是 project**。建到别的 team（比如个人的通用 team `Raphael`）会拿到错误的前缀，而且 Linear 不支持改单个 issue 的前缀 —— 只能整条迁移到目标 team 重新编号。建之前先确认 team。

新任务挂在 `microduck-rebuild` project 下。阶段主干任务用「阶段 N · xxx」命名；研发中新发现的问题用普通标题，不要也编成阶段号，否则序号会乱。
