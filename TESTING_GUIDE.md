# 🧪 PR Sentinel Testing Guide

This guide will help you test your PR Sentinel bot thoroughly.

## 🚀 **Quick Start Testing**

### 1. **Start the Bot**

```bash
# Make sure you're in the project directory
cd pr_sentinal

# Install dependencies (if not already done)
pip install -r requirements.txt

# Start the bot
python run.py
```

You should see:
```
🚀 Starting PR Sentinel...
📍 Host: 0.0.0.0
🔌 Port: 8000
🔄 Reload: false
✅ Configuration validated successfully
🚀 PR Sentinel is ready to receive webhooks!
```

### 2. **Test Health Endpoint**

Open your browser or use curl:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy", "service": "PR Sentinel"}
```

### 3. **Run Automated Tests**

```bash
python test_webhook.py
```

This will send test webhooks for:
- ✅ Issues
- ✅ Pull Requests  
- ✅ Discussions
- ✅ Security Alerts

## 🎯 **Manual Testing with Real GitHub Events**

### **Option 1: Use ngrok (Recommended)**

1. **Install ngrok:**
   ```bash
   # Download from https://ngrok.com/download
   # Or use npm: npm install -g ngrok
   ```

2. **Start ngrok tunnel:**
   ```bash
   ngrok http 8000
   ```

3. **Copy the HTTPS URL** (e.g., `https://abc123.ngrok.io`)

4. **Configure GitHub Webhook:**
   - Go to your repository → Settings → Webhooks
   - Click "Add webhook"
   - Payload URL: `https://abc123.ngrok.io/webhook`
   - Content type: `application/json`
   - Secret: Your `WEBHOOK_SECRET` from `.env`
   - Select events:
     - ✅ Pull requests
     - ✅ Issues
     - ✅ Discussions
     - ✅ Code scanning alerts
     - ✅ Secret scanning alerts
     - ✅ Dependabot alerts

5. **Test by creating real events:**
   - Create a new issue in your repo
   - Create a pull request
   - Start a discussion

### **Option 2: Use GitHub CLI (Alternative)**

1. **Install GitHub CLI:**
   ```bash
   # Windows
   winget install GitHub.cli
   
   # Or download from https://cli.github.com/
   ```

2. **Authenticate:**
   ```bash
   gh auth login
   ```

3. **Create test events:**
   ```bash
   # Create test issue
   gh issue create --title "Test Issue" --body "This is a test issue for PR Sentinel"
   
   # Create test PR
   gh pr create --title "Test PR" --body "This is a test PR for PR Sentinel"
   ```

## 🔍 **What to Look For**

### **When You Create an Issue:**

✅ **Bot should:**
- Post an AI-generated reply within 30 seconds
- Add "triage" label
- Close the issue if it's spam

### **When You Create a PR:**

✅ **Bot should:**
- Run code quality checks (ESLint, npm audit)
- Generate AI code review
- Post comprehensive comment with results
- Add "needs-review" label

### **When Security Alerts Trigger:**

✅ **Bot should:**
- Create a new security issue
- Include alert details
- Add "security" label

## 🐛 **Troubleshooting**

### **Bot Won't Start:**

1. **Check environment variables:**
   ```bash
   # Make sure .env file exists and has:
   GITHUB_TOKEN=your_token
   WEBHOOK_SECRET=your_secret
   GEMINI_API_KEY=your_key
   ```

2. **Check dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### **Webhooks Not Working:**

1. **Check ngrok tunnel:**
   - Make sure ngrok is running
   - Verify the URL in GitHub webhook settings

2. **Check bot logs:**
   - Look for incoming webhook requests
   - Check for signature verification errors

3. **Test webhook manually:**
   ```bash
   curl -X POST http://localhost:8000/webhook \
     -H "Content-Type: application/json" \
     -H "X-GitHub-Event: issues" \
     -d '{"test": "data"}'
   ```

### **AI Features Not Working:**

1. **Check Gemini API key:**
   - Verify `GEMINI_API_KEY` is set correctly
   - Test API key manually

2. **Check network connectivity:**
   - Bot needs internet access for Gemini API calls

## 📊 **Monitoring and Logs**

### **View Real-time Logs:**

The bot logs all activities. Watch for:
- `Processing {event} event`
- `Generating AI review`
- `Posting comment to PR`
- Any error messages

### **Check GitHub Activity:**

- Look for new comments on issues/PRs
- Check for new labels added
- Verify security issues created

## 🎉 **Success Indicators**

Your bot is working correctly when you see:

1. **In Bot Logs:**
   ```
   Processing issues event
   Generating AI reply
   Posting comment to issue
   Successfully processed issue #123
   ```

2. **In GitHub:**
   - New comments with AI-generated responses
   - Appropriate labels added
   - Security issues created for alerts

3. **In Test Script:**
   ```
   ✅ issues webhook sent - Status: 200
   ✅ pull_request webhook sent - Status: 200
   ✅ discussion webhook sent - Status: 200
   ✅ code_scanning_alert webhook sent - Status: 200
   ```

## 🚀 **Production Deployment**

Once testing is complete:

1. **Deploy to your server:**
   ```bash
   # Using Docker
   docker-compose up -d
   
   # Or directly
   python run.py
   ```

2. **Update GitHub webhook URL** to your production domain

3. **Monitor logs** for any issues

4. **Test with real repository events**

---

**Need help?** Check the logs for detailed error messages and ensure all environment variables are properly set. 