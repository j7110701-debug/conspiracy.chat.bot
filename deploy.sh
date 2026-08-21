#!/bin/bash
# 🚀 Conspiracy Chat Bot - Railway Deployment Script
# This script automates the entire Railway deployment process

set -e  # Exit on any error

echo ""
echo "🚀 Conspiracy Chat Bot - Railway Deployment"
echo "========================================="
echo ""

# Check if railway is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

# Check if logged in
echo "🔐 Checking Railway authentication..."
if ! railway whoami &> /dev/null; then
    echo "📱 Opening Railway login in your browser..."
    railway login
fi

echo ""
echo "🔗 Linking project to Railway..."
railway link

echo ""
echo "📤 Deploying to Railway..."
echo "This may take 2-5 minutes. Grab a coffee! ☕"
echo ""

railway up --detach

echo ""
echo "✅ Deployment started!"
echo ""
echo "📊 Checking deployment status..."
sleep 5

echo ""
echo "🔍 Your deployment info:"
railway status

echo ""
echo "📝 Now you need to add your API keys:"
echo ""
echo "Option A: Using CLI"
echo "  railway variables add OPENAI_API_KEY=sk-your-key-here"
echo ""
echo "Option B: Using Dashboard"
echo "  1. Go to https://railway.app/dashboard"
echo "  2. Select your project"
echo "  3. Click 'Variables' tab"
echo "  4. Add: OPENAI_API_KEY, ANTHROPIC_API_KEY, etc."
echo ""

echo "📂 View logs anytime:"
echo "  railway logs"
echo ""

echo "🎉 Your app will be live soon! Check the logs:"
echo "  railway logs --tail 20"
echo ""
echo "Once deployed, open: https://your-railway-url.up.railway.app/ui"
echo ""
echo "Happy chatting! 🤖"
echo ""
