# slack-copilot

一个集成了 GitHub Copilot CLI 的 Slack 机器人，可以直接在你的 Slack 工作区中提供 AI 驱动的命令建议和解释。

[English](README.md) | 简体中文

## 功能特性

- 🤖 **AI 命令建议**：使用 GitHub Copilot 获取命令行建议
- 📚 **命令解释**：理解任何命令的作用
- 💬 **Slack 集成**：通过提及或斜杠命令进行交互
- 🚀 **易于部署**：Docker 支持，可快速部署到服务器
- 🔧 **可配置**：基于环境变量的配置

## 前置要求

开始之前，请确保已安装以下软件：

- **Python 3.12+**
- **uv**（Python 包管理器）：[安装指南](https://github.com/astral-sh/uv)
- **GitHub Copilot CLI**：[安装指南](https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-in-the-command-line)
  ```bash
  # 安装 GitHub Copilot CLI
  # 参见：https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-in-the-command-line
  
  # 安装后将可以使用独立的 copilot CLI
  copilot --version
  ```

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/coolestowl/slack-copilot.git
cd slack-copilot
```

### 2. 设置 Slack 应用

1. 访问 [Slack API](https://api.slack.com/apps) 并创建新应用
2. 在应用设置中启用 Socket Mode
3. 添加以下 Bot Token Scopes：
   - `app_mentions:read`
   - `chat:write`
   - `commands`
4. 将应用安装到你的工作区
5. 复制 **Bot User OAuth Token**（以 `xoxb-` 开头）
6. 复制 **App-Level Token**（以 `xapp-` 开头）

### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 并添加你的 tokens
```

更新 `.env` 文件，添加你的 Slack tokens：
```env
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_APP_TOKEN=xapp-your-app-token-here
```

### 4. 安装依赖

```bash
uv sync
```

### 5. 运行机器人

```bash
uv run python main.py
```

## 使用方法

### 提及机器人

```
@slack-copilot 如何查找大文件？
@slack-copilot explain tar -xzvf file.tar.gz
```

### 使用斜杠命令

```
/copilot 如何列出所有进程？
/copilot explain docker-compose up -d
```

## 部署

### 使用 Docker

1. 构建 Docker 镜像：
```bash
docker build -t slack-copilot .
```

2. 运行容器：
```bash
docker run -d --name slack-copilot \
  -e SLACK_BOT_TOKEN=xoxb-your-token \
  -e SLACK_APP_TOKEN=xapp-your-token \
  slack-copilot
```

### 使用 Docker Compose

```bash
docker-compose up -d
```

详细的部署指南请参见 [DEPLOYMENT.md](DEPLOYMENT.md)。

## 项目结构

```
slack-copilot/
├── src/
│   └── slack_copilot/
│       ├── __init__.py      # 包初始化
│       ├── bot.py           # Slack 机器人实现
│       ├── config.py        # 配置管理
│       └── copilot.py       # GitHub Copilot CLI 集成
├── main.py                  # 应用程序入口
├── pyproject.toml           # 项目依赖和元数据
├── uv.lock                  # 依赖锁定文件
├── Dockerfile               # Docker 配置
├── docker-compose.yml       # Docker Compose 配置
├── .env.example             # 环境变量示例
└── README.md                # 本文件
```

## 配置

所有配置通过环境变量完成：

| 变量 | 说明 | 默认值 | 是否必需 |
|------|------|--------|---------|
| `SLACK_BOT_TOKEN` | Slack Bot User OAuth Token | - | 是 |
| `SLACK_APP_TOKEN` | Slack App-Level Token | - | 是 |
| `COPILOT_CLI_PATH` | Copilot CLI 可执行文件路径 | `copilot` | 否 |
| `PORT` | 服务器端口（预留） | `3000` | 否 |

## 开发

### 安装开发依赖

```bash
uv sync
```

### 运行开发模式

```bash
uv run python main.py
```

### 常用命令

```bash
# 安装依赖
make install

# 运行机器人
make run

# 构建 Docker 镜像
make build

# 使用 Docker 运行
make docker-run

# 查看 Docker 日志
make docker-logs

# 清理临时文件
make clean
```

## 故障排除

### 机器人不响应
- 确保 Socket Mode 在 Slack 应用中已启用
- 验证 `.env` 中的 tokens 是否正确
- 检查机器人是否已被邀请到频道

### "Copilot CLI not found" 错误
- 安装 GitHub Copilot CLI：https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-in-the-command-line
- 验证安装：`copilot --version`
- 认证：首次运行 `copilot` 时按照提示进行认证

### 权限错误
- 确保 Slack 应用具有所需的权限范围
- 如果添加了新的权限范围，需要重新安装应用到工作区

## 文档

- [README.md](README.md) - 项目概述和快速开始（英文）
- [README_CN.md](README_CN.md) - 项目概述和快速开始（中文）
- [USAGE.md](USAGE.md) - 详细使用指南
- [DEPLOYMENT.md](DEPLOYMENT.md) - 部署指南
- [CONTRIBUTING.md](CONTRIBUTING.md) - 贡献指南

## 许可证

详见 [LICENSE](LICENSE) 文件。

## 贡献

欢迎贡献！请随时提交 Pull Request。

详细的贡献指南请参见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 支持

如有问题或建议，请在 GitHub 上提出 issue：
https://github.com/coolestowl/slack-copilot/issues
