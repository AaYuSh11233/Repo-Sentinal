# 🚀 PR Sentinel - Universal Repository Deployment Guide

This guide will help you deploy PR Sentinel to automatically handle **ALL** your current and future repositories without any manual webhook setup.

## 🎯 **Goal: Universal Repository Coverage**

Once deployed, PR Sentinel will automatically:
- ✅ Handle issues, PRs, discussions in ALL your repos
- ✅ Process security alerts from ALL your repos  
- ✅ Work with future repositories automatically
- ✅ No manual webhook configuration needed per repo

## 🏗️ **Deployment Options**

### **Option 1: Deploy to Cloud Platform (Recommended)**

#### **A. Deploy to Railway (Easiest)**

1. **Create Railway Account:**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy from GitHub:**
   ```bash
   # Push your code to GitHub first
   git add .
   git commit -m "Deploy PR Sentinel"
   git push origin main
   ```

3. **Connect to Railway:**
   - In Railway dashboard, click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your PR Sentinel repository

4. **Set Environment Variables:**
   - Go to your project → Variables
   - Add these variables:
   ```
   GITHUB_TOKEN=ghp_your_token_here
   WEBHOOK_SECRET=your_random_secret_here
   GEMINI_API_KEY=your_gemini_key_here
   HOST=0.0.0.0
   PORT=8000
   RELOAD=false
   ```

5. **Get Your Webhook URL:**
   - Railway will give you a URL like: `https://your-app.railway.app`
   - Your webhook URL will be: `https://your-app.railway.app/webhook`

#### **B. Deploy to Render (Alternative)**

1. **Create Render Account:**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create Web Service:**
   - Click "New Web Service"
   - Connect your GitHub repo
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python run.py`

3. **Set Environment Variables** (same as Railway)

4. **Get Your Webhook URL:**
   - Render will give you: `https://your-app.onrender.com`
   - Webhook URL: `https://your-app.onrender.com/webhook`

### **Option 2: Deploy to Your Own Server**

1. **Get a VPS** (DigitalOcean, AWS, etc.)

2. **Deploy with Docker:**
   ```bash
   # On your server
   git clone https://github.com/your-username/pr-sentinal.git
   cd pr-sentinal
   
   # Create .env file
   nano .env
   # Add your environment variables
   
   # Deploy with Docker
   docker-compose up -d
   ```

3. **Get Your Webhook URL:**
   - Your server IP/domain: `https://your-domain.com`
   - Webhook URL: `https://your-domain.com/webhook`

## 🔧 **Universal GitHub Webhook Setup**

Once you have your webhook URL, set up the **universal webhook**:

### **1. Create Organization-Level Webhook (Best Option)**

If you have a GitHub organization:

1. **Go to Organization Settings:**
   - Visit: `https://github.com/organizations/YOUR_ORG/settings/hooks`
   - Or: Your Org → Settings → Webhooks

2. **Add Organization Webhook:**
   - Click "Add webhook"
   - Payload URL: `https://your-app.railway.app/webhook`
   - Content type: `application/json`
   - Secret: Your `WEBHOOK_SECRET`
   - **Select events:**
     - ✅ Pull requests
     - ✅ Issues
     - ✅ Discussions
     - ✅ Code scanning alerts
     - ✅ Secret scanning alerts
     - ✅ Dependabot alerts
   - ✅ **Active**

### **2. Create User-Level Webhook (Alternative)**

If you don't have an organization:

1. **Go to User Settings:**
   - Visit: `https://github.com/settings/hooks`
   - Or: Your Profile → Settings → Webhooks

2. **Add User Webhook:**
   - Same configuration as above
   - This will cover all your personal repositories

### **3. GitHub App Approach (Most Powerful)**

For maximum control, create a GitHub App:

1. **Create GitHub App:**
   - Go to: `https://github.com/settings/apps/new`
   - App name: `PR Sentinel`
   - Homepage URL: Your webhook URL
   - Webhook URL: Your webhook URL
   - Webhook secret: Your `WEBHOOK_SECRET`

2. **Set Permissions:**
   - Repository permissions:
     - Issues: Read & Write
     - Pull requests: Read & Write
     - Contents: Read
     - Metadata: Read
   - Subscribe to events:
     - Pull requests
     - Issues
     - Discussions
     - Code scanning alerts
     - Secret scanning alerts
     - Dependabot alerts

3. **Install the App:**
   - Go to your app settings
   - Click "Install App"
   - Choose "All repositories" or select specific ones

## 🔑 **GitHub Token Setup**

### **For Organization/User Webhooks:**

1. **Create Personal Access Token:**
   - Go to: `https://github.com/settings/tokens`
   - Click "Generate new token (classic)"
   - Select scopes:
     - ✅ `repo` (Full control of private repositories)
     - ✅ `admin:org` (if using organization webhook)
     - ✅ `write:packages` (if needed)

2. **Use Token in Environment:**
   ```
   GITHUB_TOKEN=ghp_your_token_here
   ```

### **For GitHub App:**

1. **Generate App Installation Token:**
   - The app will handle authentication automatically
   - No personal access token needed

## 🧪 **Testing Universal Deployment**

### **1. Test with Existing Repository:**

1. **Create a test issue:**
   ```bash
   # In any of your repositories
   gh issue create --title "Test Universal Bot" --body "Testing if PR Sentinel works across all repos"
   ```

2. **Create a test PR:**
   ```bash
   # Create a test branch and PR
   git checkout -b test-bot
   echo "# Test" > test.md
   git add test.md
   git commit -m "Test PR for bot"
   git push origin test-bot
   gh pr create --title "Test PR" --body "Testing PR Sentinel"
   ```

### **2. Test with New Repository:**

1. **Create a new repository:**
   ```bash
   gh repo create test-new-repo --public
   ```

2. **Add some content and create issues/PRs**
   - The bot should automatically handle them

### **3. Monitor Logs:**

Check your deployment logs:
- **Railway:** Project → Deployments → View logs
- **Render:** Service → Logs
- **Docker:** `docker-compose logs -f`

## 🔍 **Verification Checklist**

✅ **Bot is deployed and running**
- Health check: `https://your-app.railway.app/health`

✅ **Webhook is configured**
- Organization/User webhook is active
- Or GitHub App is installed

✅ **Environment variables set**
- `GITHUB_TOKEN` with proper permissions
- `WEBHOOK_SECRET` for security
- `GEMINI_API_KEY` for AI features

✅ **Test events work**
- Issues get AI responses
- PRs get code reviews
- Security alerts create issues

## 🚨 **Troubleshooting**

### **Webhook Not Receiving Events:**

1. **Check webhook delivery:**
   - Go to webhook settings
   - Click "Recent Deliveries"
   - Check for failed deliveries

2. **Verify URL accessibility:**
   ```bash
   curl https://your-app.railway.app/health
   ```

3. **Check bot logs for errors**

### **Bot Not Responding:**

1. **Check environment variables**
2. **Verify GitHub token permissions**
3. **Check Gemini API key**
4. **Review deployment logs**

### **Security Alerts Not Working:**

1. **Enable security features in repositories:**
   - Go to repo → Settings → Security
   - Enable "Dependency graph"
   - Enable "Dependabot alerts"
   - Enable "Code scanning"

## 🎉 **Success Indicators**

Once properly deployed, you should see:

1. **Automatic responses** to issues in any repository
2. **Code reviews** on pull requests across all repos
3. **Security issues** created for alerts
4. **No manual setup** needed for new repositories

## 📊 **Monitoring**

### **Set up monitoring:**

1. **Health checks:** Your platform should monitor the health endpoint
2. **Log monitoring:** Set up alerts for errors
3. **GitHub activity:** Monitor bot responses in your repositories

---

**🎯 Result:** Once deployed, PR Sentinel will automatically handle ALL your repositories (current and future) without any manual intervention! 