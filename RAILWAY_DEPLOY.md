# 🚀 Deploy to Railway.app - Complete Guide

## 🎯 Why Railway.app?

✅ **NO credit card required**  
✅ **$5 free credit per month** (~500 hours)  
✅ **Easiest deployment** (auto-detects everything!)  
✅ **Perfect for background workers**  
✅ **GitHub integration** (auto-deploy on push)

---

## 📋 Quick Deployment (3 Minutes!)

### Step 1: Sign Up on Railway.app

1. **Go to:** https://railway.app
2. **Click:** "Start a New Project" or "Login"
3. **Sign in with GitHub** (easiest option)
4. **Authorize Railway** to access your repositories
5. **NO credit card required!** ✅

---

### Step 2: Create New Project

1. **Click:** "New Project" button
2. **Select:** "Deploy from GitHub repo"
3. **Choose:** `HemanthKumar817/linkedin-automation`
4. **Click:** "Deploy Now"

**That's it!** Railway will automatically:
- ✅ Detect it's a Python project
- ✅ Install dependencies
- ✅ Start your automation

---

### Step 3: Add Environment Variables

1. **Click** on your deployed service
2. **Go to:** "Variables" tab
3. **Click:** "New Variable"
4. **Add these variables:**

```
LINKEDIN_CLIENT_ID = 86uql6iawlwk3n
LINKEDIN_CLIENT_SECRET = WPL_AP1.m47Q91JFrEAE4NRh.MohQRw==
LINKEDIN_ACCESS_TOKEN = [Your 60-day token from .env]
LINKEDIN_USER_ID = EkYPbxSoGN
GEMINI_API_KEY = AIzaSyB0xojkGJkwCGj4SjzB5VN1lAh7Qm4gWfQ
AI_PROVIDER = gemini
AI_MODEL = gemini-2.5-flash
PYTHONUNBUFFERED = 1
```

5. **Click:** "Add" for each variable
6. **Railway will auto-redeploy** with new variables!

---

### Step 4: Monitor Your Deployment

1. **View Logs:** Click "Deployments" → "View Logs"
2. **Check Status:** Should show "Active" with green indicator
3. **Monitor Usage:** Click "Usage" to see your free credit usage

---

## 📊 Railway.app Free Tier

**What You Get:**
- 💰 **$5 free credit per month**
- ⏱️ **~500 hours of runtime** (21 days of 24/7 operation)
- 💾 **512 MB RAM** (perfect for your bot)
- 🔄 **Auto-deploy on git push**
- 📊 **Built-in monitoring**

**Your LinkedIn Bot Usage:**
- Uses ~50-100 MB RAM
- Runs 24/7
- Posts once per day at 9 PM
- **Will fit perfectly in free tier!** ✅

---

## 🎛️ Railway Configuration Files

Your project includes:

### `railway.json`
```json
{
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r requirements-minimal.txt"
  },
  "deploy": {
    "startCommand": "python main.py --mode auto",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### `Procfile`
```
web: python main.py --mode auto
```

**Railway auto-detects these files!** No manual configuration needed.

---

## 🔄 Auto-Deploy on Git Push

Once deployed, any time you push to GitHub:

```powershell
git add .
git commit -m "Update automation"
git push origin main
```

**Railway automatically:**
1. Detects the push
2. Rebuilds your project
3. Redeploys with zero downtime
4. **No manual action needed!** ✨

---

## 📈 Monitor Your Bot

### View Logs
1. Go to Railway dashboard
2. Click on your service
3. Click "Deployments" → "View Logs"
4. See real-time logs:
   - Scraping activity
   - Post generation
   - LinkedIn posting
   - Any errors

### Check Usage
1. Click "Usage" tab
2. See:
   - **Credits used** (out of $5)
   - **RAM usage**
   - **CPU usage**
   - **Estimated time remaining**

---

## 🛠️ Troubleshooting

### Issue 1: Deployment Fails

**Check logs for errors:**
1. Click "Deployments"
2. Click on failed deployment
3. Read error message
4. Common fixes:
   - Verify `requirements-minimal.txt` exists
   - Check Python version compatibility
   - Ensure all files committed to GitHub

---

### Issue 2: Bot Not Posting

**Verify environment variables:**
1. Go to "Variables" tab
2. Check all variables are set correctly
3. Especially verify:
   - `LINKEDIN_ACCESS_TOKEN` (must be valid)
   - `GEMINI_API_KEY`
   - `AI_PROVIDER = gemini`

---

### Issue 3: Out of Credits

**If you run out of $5 free credit:**

**Option A: Optimize Usage**
- Run bot only 1-2 hours per day (instead of 24/7)
- Schedule to run only before posting time
- Saves 90% of credits!

**Option B: Upgrade to Hobby Plan** ($5/month)
- Unlimited hours
- Better resources
- Priority support

**Option C: Run Locally**
- Use Windows Task Scheduler
- Completely free
- Laptop must be on at posting time

---

## 🎯 Deployment Checklist

Before deploying, verify:

- ✅ Code pushed to GitHub
- ✅ `railway.json` file exists
- ✅ `Procfile` file exists
- ✅ `requirements-minimal.txt` file exists
- ✅ `.env` file contains all credentials (local only)
- ✅ LinkedIn access token is valid

After deploying, verify:

- ✅ Service shows "Active" status
- ✅ Logs show automation started
- ✅ No errors in logs
- ✅ All environment variables set
- ✅ Credits are being consumed normally

---

## 💡 Pro Tips

### 1. Optimize for Free Tier

Instead of running 24/7, modify scheduling:

```python
# Run only 8:00 PM - 10:00 PM daily
# = 2 hours/day × 30 days = 60 hours/month
# Your $5 credit lasts 8+ months!
```

### 2. Monitor Usage Weekly

Check Railway dashboard weekly:
- View credit usage
- Check for any errors
- Monitor performance

### 3. Renew LinkedIn Token

Your LinkedIn token expires in 60 days:

```powershell
# Every 60 days, run:
python scripts/linkedin_oauth.py

# Then update Railway variable:
# 1. Go to Railway dashboard
# 2. Click "Variables"
# 3. Update LINKEDIN_ACCESS_TOKEN
# 4. Auto-redeploys!
```

---

## 🆘 Need Help?

**Railway Documentation:**
- Getting Started: https://docs.railway.app/getting-started
- Environment Variables: https://docs.railway.app/develop/variables
- Deployment: https://docs.railway.app/deploy/deployments

**Your Project Docs:**
- `README.md` - Project overview
- `FREE_DEPLOYMENT_OPTIONS.md` - Platform comparison
- `docs/troubleshooting.md` - Common issues

**Railway Support:**
- Discord Community: https://discord.gg/railway
- Help Center: https://help.railway.app

---

## 🎉 Success!

Your LinkedIn automation is now:
- ✅ Running 24/7 on Railway.app
- ✅ Scraping news daily
- ✅ Generating AI posts with Gemini
- ✅ Posting at 9 PM automatically
- ✅ Tracking engagement
- ✅ All for FREE ($5 credit)!

---

## 📝 Quick Reference

**Dashboard:** https://railway.app/dashboard  
**Your Project:** `linkedin-automation`  
**View Logs:** Dashboard → Service → Deployments → View Logs  
**Update Variables:** Dashboard → Service → Variables  
**Check Usage:** Dashboard → Service → Usage  

**Local Commands:**
```powershell
git add .
git commit -m "Update"
git push origin main    # Auto-deploys to Railway!
```

---

**Enjoy your automated LinkedIn presence!** 🚀
