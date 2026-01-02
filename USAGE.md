# Usage Guide

This guide shows you how to interact with the Slack Copilot bot.

## Getting Started

Once the bot is running and added to your Slack workspace, you can interact with it in several ways:

### 1. Direct Mentions

Mention the bot in any channel where it's been invited:

```
@slack-copilot how do I find all files larger than 100MB?
@slack-copilot what's the best way to compress a directory?
@slack-copilot how can I monitor disk usage in real-time?
```

### 2. Explain Commands

Ask the bot to explain what a specific command does:

```
@slack-copilot explain tar -xzvf archive.tar.gz
@slack-copilot explain docker-compose up -d
@slack-copilot explain find . -type f -name "*.log" -mtime +7 -delete
```

### 3. Slash Commands

Use the `/copilot` slash command:

```
/copilot how do I list all running processes?
/copilot explain kubectl get pods -n production
```

## Example Conversations

### Example 1: Getting Command Suggestions

**You:** `@slack-copilot how do I search for text in files?`

**Bot:** 
```
To search for text in files, you can use the grep command:

grep "search_text" filename

For searching recursively in directories:
grep -r "search_text" /path/to/directory

For case-insensitive search:
grep -i "search_text" filename
```

### Example 2: Explaining a Complex Command

**You:** `@slack-copilot explain docker run -d -p 8080:80 --name web nginx`

**Bot:**
```
This command runs a Docker container with the following options:

- 'docker run': Creates and starts a new container
- '-d': Runs the container in detached mode (in the background)
- '-p 8080:80': Maps port 8080 on the host to port 80 in the container
- '--name web': Names the container "web"
- 'nginx': Uses the nginx image

The command starts an nginx web server in the background, accessible on port 8080.
```

### Example 3: Git Commands

**You:** `@slack-copilot how do I undo the last commit but keep the changes?`

**Bot:**
```
To undo the last commit but keep your changes:

git reset --soft HEAD~1

This will:
- Remove the last commit from the git history
- Keep all the changes staged and ready to commit again
- Allow you to modify and recommit if needed

If you want to unstage the changes as well:
git reset HEAD~1
```

### Example 4: System Administration

**You:** `@slack-copilot how can I find which process is using a specific port?`

**Bot:**
```
To find which process is using a specific port, use one of these commands:

On Linux:
sudo lsof -i :PORT_NUMBER
# or
sudo netstat -tulpn | grep :PORT_NUMBER
# or
sudo ss -tulpn | grep :PORT_NUMBER

Example for port 8080:
sudo lsof -i :8080

This will show the PID and name of the process using that port.
```

## Tips for Best Results

### 1. Be Specific
❌ Bad: `@slack-copilot files`
✅ Good: `@slack-copilot how do I find all PDF files in my home directory?`

### 2. Provide Context
❌ Bad: `@slack-copilot compress`
✅ Good: `@slack-copilot how do I compress a folder with tar and gzip?`

### 3. Ask for Explanations
When you encounter an unfamiliar command, ask the bot to explain it:
```
@slack-copilot explain awk '{print $1}' file.txt
```

### 4. Break Down Complex Tasks
For complex tasks, ask step by step:
```
@slack-copilot how do I backup a MySQL database?
@slack-copilot explain mysqldump -u root -p database_name > backup.sql
```

## Common Use Cases

### Development

```
@slack-copilot how do I run a Python HTTP server?
@slack-copilot how do I check my Node.js version?
@slack-copilot explain npm ci
```

### DevOps

```
@slack-copilot how do I check docker container logs?
@slack-copilot how do I restart a systemd service?
@slack-copilot explain kubectl apply -f deployment.yaml
```

### System Administration

```
@slack-copilot how do I check disk space usage?
@slack-copilot how do I find large files?
@slack-copilot how do I monitor CPU usage in real-time?
```

### Git Operations

```
@slack-copilot how do I create a new branch?
@slack-copilot how do I merge branches?
@slack-copilot explain git rebase -i HEAD~3
```

## Channel Best Practices

### 1. Dedicated Channel
Consider creating a dedicated channel like `#copilot-help` where team members can:
- Ask command-related questions
- Share useful commands
- Learn from each other's questions

### 2. Public vs Private
- Use in public channels for knowledge sharing
- Use in private messages for personal queries

### 3. Team Learning
- Team members can learn from others' questions
- Build a searchable history of commands
- Reduce repetitive questions to senior developers

## Limitations

The bot has some limitations to be aware of:

1. **GitHub Copilot CLI Required**: The bot needs GitHub Copilot CLI to be installed and authenticated on the server
2. **Command Suggestions Only**: The bot suggests commands but doesn't execute them
3. **Context Awareness**: The bot doesn't have context about your specific system or project
4. **Rate Limits**: Subject to GitHub Copilot API rate limits

## Troubleshooting

### Bot Doesn't Respond

1. **Check if bot is online**: Look for the green dot next to the bot's name
2. **Verify bot is in the channel**: Invite the bot if needed: `/invite @slack-copilot`
3. **Check permissions**: Ensure the bot has permission to read and write messages

### Incorrect or Unhelpful Responses

1. **Rephrase your question**: Try asking in a different way
2. **Add more context**: Provide more details about what you're trying to do
3. **Break down the task**: Ask about smaller, specific parts of the task

### Error Messages

If you see error messages:
- `❌ GitHub CLI not found`: Contact your administrator to install GitHub CLI
- `❌ Error executing Copilot CLI`: The server may have connectivity issues
- `No response from Copilot CLI`: Try rephrasing your question

## Privacy and Security

- The bot processes your questions on the server
- Questions are sent to GitHub Copilot API
- Don't include sensitive information (passwords, API keys) in your questions
- All interactions are logged for troubleshooting

## Getting Help

If you need help with the bot:
1. Check this usage guide
2. Ask in your team's support channel
3. Contact your system administrator
4. Report issues on GitHub: https://github.com/coolestowl/slack-copilot/issues

## Feedback

We welcome feedback! If you have suggestions for improving the bot:
- Open an issue on GitHub
- Share your ideas with the team
- Contribute to the project (see CONTRIBUTING.md)
