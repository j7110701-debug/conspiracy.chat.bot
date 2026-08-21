# 🚀 Deploy to Railway (5 Minutes)

## The Easiest Way: One-Click Deploy

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new?githubRepo=j7110701-debug/conspiracy.chat.bot)

**Click the button above and you're done!** Railway will:
1. ✅ Fork/clone your repo
2. ✅ Build with Dockerfile
3. ✅ Deploy automatically
4. ✅ Give you a live URL

---

## Manual Deploy (If button doesn't work)

### Step 1: Create Railway Account
```bash
# Go to https://railway.app and sign up with GitHub
```

### Step 2: Install Railway CLI
```bash
# macOS
brew install railway

# Windows (with npm)
npm install -g @railway/cli

# Linux
npm install -g @railway/cli
```

### Step 3: Deploy Your App
```bash
# Navigate to your project folder
cd /path/to/conspiracy.chat.bot

# Login to Railway
railway login
# (Opens browser for authentication)

# Deploy
railway up
# Watch the magic happen! ✨
```

### Step 4: Set API Keys
After deployment completes:

```bash
# Add your environment variables
railway variables add OPENAI_API_KEY=sk-your-key-here

# Or use the dashboard: https://railway.app/dashboard
# → Your Project → Variables tab
# → Add: OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.
```

### Step 5: Get Your Live URL
```bash
railway logs
# Look for the deployment URL at the top
# Example: https://conspiracy-bot-production.up.railway.app

# Open it!
open https://your-url.up.railway.app/ui
```

---

## Environment Variables Needed

Add these in Railway Dashboard → Variables:

```
OPENAI_API_KEY=sk-your-key
ANTHROPIC_API_KEY=sk-ant-your-key
ANTHROPIC_MODEL=claude-3-opus-20240229
LLAMA_MODEL_PATH=/path/to/model.gguf
PORT=8000
```

**Only need one backend?** Just add that one API key. Others are optional.

---

## Verify Deployment

```bash
# Check logs
railway logs

# See your app info
railway status

# View all variables
railway variables
```

---

## Your Live App

Once deployed, you'll have:

✅ **Web UI**: `https://your-url.up.railway.app/ui`
✅ **API**: `https://your-url.up.railway.app/think`
✅ **API Docs**: `https://your-url.up.railway.app/docs`
✅ **Health Check**: `https://your-url.up.railway.app/`

---

## Troubleshooting

### "Command not found: railway"
```bash
npm install -g @railway/cli
railway login
```

### "Deployment failed"
```bash
railway logs  # Check what went wrong
```

### "API key not working"
1. Go to Railway Dashboard
2. Click your project
3. Go to Variables tab
4. Make sure keys are correct
5. Railway will auto-redeploy

### "App keeps crashing"
```bash
railway logs --tail 100  # See last 100 lines
```

---

## Costs

**Railway Pricing:**
- $5/month free credit (usually enough for hobby projects)
- Pay-as-you-go after that (~$0.13/hour)
- Perfect for testing!

---

## Custom Domain (Optional)

In Railway Dashboard → Your Project → Settings → Domains:
1. Add your custom domain
2. Update your domain DNS settings
3. Done! Your app is at your domain

---

## Auto-Deploy from GitHub

Your app will **automatically redeploy** whenever you push to GitHub!

```bash
# Make changes locally
git add .
git commit -m "Update app"
git push origin main

# Railway automatically redeploys! ✅
```

---

## Next Steps

1. ✅ Click deploy button OR run `railway up`
2. ✅ Add API keys in Railway Dashboard
3. ✅ Visit your live URL
4. ✅ Share it with the world! 🌍

---

**Need help?** Railway docs: https://docs.railway.app
