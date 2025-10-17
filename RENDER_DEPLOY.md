# 🚀 Deploy to Render.com - Complete Guide

## 🎯 Why Render.com?

✅ **NO credit card required**  
✅ **750 hours/month FREE** (enough for 24/7 operation)  
✅ **Easy deployment** (similar to Heroku)  
✅ **Background workers** (perfect for automation)  
✅ **Simple setup** (5 minutes!)

---

## 📋 Prerequisites

Before deployment, make sure you have:
- ✅ LinkedIn OAuth credentials (access token)
- ✅ Gemini API key
- ✅ GitHub account
- ✅ All environment variables in `.env` file

---

## 🚀 Quick Deployment (5 Minutes)

### Step 1: Prepare Your Code

Run the automated deployment script:
```powershell
.\deploy_to_render.ps1
```

This script will:
- ✅ Initialize Git repository
- ✅ Create `.gitignore`
- ✅ Commit your code
- ✅ Show deployment instructions

---

### Step 2: Create GitHub Repository

1. **Go to GitHub:** https://github.com/new
2. **Repository name:** `linkedin-automation`
3. **Visibility:** Private (recommended)
4. **Click:** "Create repository"

---

### Step 3: Push Code to GitHub

Replace `YOUR_USERNAME` with your GitHub username:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/linkedin-automation.git
git branch -M main
git push -u origin main
```

---

### Step 4: Deploy to Render.com

1. **Sign up at Render.com**
   - Go to: https://render.com
   - Click "Get Started for Free"
   - Sign up with **GitHub** (easiest option)
   - **NO credit card required!**

2. **Create New Background Worker**
   - Click "New +" button
   - Select "Background Worker"
   - Connect your GitHub repository
   - Select: `linkedin-automation`

3. **Configure Service**
   
   **Basic Settings:**
   - **Name:** `linkedin-automation`
   - **Environment:** `Python 3`
   - **Region:** Choose closest to you
   - **Branch:** `main`
   - **Plan:** `Free` (750 hours/month)

   **Build Settings:**
   - **Build Command:** `pip install -r requirements-minimal.txt`
   - **Start Command:** `python main.py --mode auto`

4. **Add Environment Variables**
   
   Click "Advanced" → "Add Environment Variable"
   
   Add these from your `.env` file:
   
   | Key | Value (from your .env) |
   |-----|------------------------|
   | `LINKEDIN_CLIENT_ID` | Your LinkedIn client ID |
   | `LINKEDIN_CLIENT_SECRET` | Your LinkedIn client secret |
   | `LINKEDIN_ACCESS_TOKEN` | Your LinkedIn access token |
   | `LINKEDIN_USER_ID` | Your LinkedIn user ID |
   | `GEMINI_API_KEY` | Your Gemini API key |
   | `AI_PROVIDER` | `gemini` |
   | `AI_MODEL` | `gemini-2.5-flash` |
   | `PYTHONUNBUFFERED` | `1` |

   **💡 Tip:** Copy values exactly from your `.env` file!

5. **Deploy!**
   - Click "Create Background Worker"
   - Render will automatically:
     - Clone your repository
     - Install dependencies
     - Start your automation
   - **Deployment time:** 2-3 minutes

---

## 📊 Monitor Your Deployment

### View Logs
1. Go to: https://dashboard.render.com
2. Click on your service: `linkedin-automation`
3. Click "Logs" tab
4. You'll see:
   - Scraping activity
   - Post generation
   - Scheduling status
   - Any errors

### Check Status
- **Green dot** = Running ✅
- **Yellow dot** = Building 🔄
- **Red dot** = Error ❌

---

## 🔧 Common Issues & Solutions

### Issue 1: Deployment Fails During Build

**Error:** `Could not find a version that satisfies the requirement...`

**Solution:**
```powershell
# Update requirements-minimal.txt to use exact versions
# Already done in your project!
```

---

### Issue 2: Worker Keeps Restarting

**Error:** Worker crashes and restarts repeatedly

**Solution:**
1. Check logs for errors
2. Verify all environment variables are set correctly
3. Make sure LinkedIn access token is valid (60 days)

---

### Issue 3: Service Sleeps After 15 Minutes

**Note:** This is normal for free tier!

**What happens:**
- Render spins down service after 15 min of inactivity
- It automatically wakes up when scheduled to post
- This saves your free hours

**To prevent sleeping:**
- Upgrade to paid plan ($7/month)
- Or accept occasional wake-up delays (usually < 30 seconds)

---

## ⚙️ Configuration

### Render.yaml (Auto-Configuration)

Your project includes `render.yaml` for automatic deployment:

```yaml
services:
  - type: worker
    name: linkedin-automation
    env: python
    plan: free
    buildCommand: pip install -r requirements-minimal.txt
    startCommand: python main.py --mode auto
```

**To use auto-deployment:**
1. In Render dashboard, click "New +" → "Blueprint"
2. Connect repository
3. Render reads `render.yaml` and auto-configures everything!

---

## 🔄 Update Your Deployment

### When You Make Code Changes:

```powershell
# Commit changes
git add .
git commit -m "Update automation"
git push origin main
```

**Render automatically:**
- Detects the push
- Rebuilds your service
- Deploys new version
- Zero downtime! ✨

---

## 📈 Free Tier Limits

**Render Free Tier:**
- ✅ 750 hours/month
- ✅ 512 MB RAM
- ✅ Shared CPU
- ✅ Perfect for this project!

**How long will it run?**
- **24/7 operation:** ~31 days (750 hours = 31.25 days)
- **Your automation:** Runs continuously, posts daily at 9 PM
- **Sleep mode:** Service sleeps after 15 min inactivity (saves hours)

**💡 Optimization:**
To make free tier last longer, modify `main.py` to:
- Run only 1 hour before posting time
- Post and then exit
- Saves ~90% of hours!

---

## 🎯 Next Steps After Deployment

### 1. Test Your Deployment

Wait 2-3 minutes after deployment, then:

1. **Check logs** to see if automation started
2. **Verify LinkedIn post** will be created at 9 PM
3. **Monitor for 24 hours** to ensure stability

### 2. Renew LinkedIn Token (Every 60 Days)

Your LinkedIn access token expires in 60 days:

```powershell
# When token expires (in 60 days), run:
python scripts/linkedin_oauth.py

# Then update on Render:
# 1. Go to dashboard.render.com
# 2. Click your service
# 3. Click "Environment"
# 4. Update LINKEDIN_ACCESS_TOKEN
# 5. Click "Save Changes"
```

### 3. Monitor Performance

Check Render dashboard weekly:
- View logs for any errors
- Monitor resource usage
- Check deployment status

---

## 🆘 Support & Resources

**Render Documentation:**
- Getting Started: https://render.com/docs
- Background Workers: https://render.com/docs/background-workers
- Environment Variables: https://render.com/docs/environment-variables

**Your Project Documentation:**
- `README.md` - Project overview
- `QUICKSTART.md` - Local setup guide
- `FREE_DEPLOYMENT_OPTIONS.md` - Alternative platforms
- `docs/troubleshooting.md` - Common issues

**Need Help?**
- Render Community: https://community.render.com
- Render Support: support@render.com

---

## 🎉 Success Checklist

Before you finish, verify:

- ✅ Service is deployed and running (green dot)
- ✅ Logs show automation started
- ✅ All environment variables are set
- ✅ No errors in logs
- ✅ Service scheduled to post at 9 PM daily
- ✅ GitHub repository is up to date
- ✅ Deployment auto-updates on git push

---

## 💰 Cost Comparison

| Platform | Cost | Credit Card? | Hours/Month |
|----------|------|--------------|-------------|
| **Render** | **FREE** | **NO** ✅ | **750** |
| Heroku | FREE | YES ⚠️ | 1000 |
| Railway | FREE | NO ✅ | 500 |
| Your Laptop | FREE | NO ✅ | Unlimited* |

*Laptop must be on at posting time

---

## 🚀 You're All Set!

Your LinkedIn automation is now:
- ✅ Running 24/7 on Render.com
- ✅ Scraping news daily
- ✅ Generating AI posts
- ✅ Posting at 9 PM automatically
- ✅ Tracking engagement
- ✅ All for FREE! (no credit card)

**Enjoy your automated LinkedIn presence!** 🎉

---

## 📝 Quick Reference

**Dashboard:** https://dashboard.render.com  
**Your Service:** `linkedin-automation`  
**Logs:** Dashboard → Service → Logs  
**Update Env Vars:** Dashboard → Service → Environment  
**Redeploy:** Dashboard → Service → Manual Deploy  

**Local Commands:**
```powershell
.\deploy_to_render.ps1  # Prepare deployment
git push origin main    # Auto-deploy updates
```

---

**Questions?** Check `docs/troubleshooting.md` or Render documentation!
