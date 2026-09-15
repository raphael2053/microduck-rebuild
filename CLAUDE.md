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
