**classic fork + sync setup.**
You want:

A copy of a public repo in your account (your own remote)

Ability to sync changes from original

Ability to push your own changes to your own repo (not the original)

I’ll explain step by step like a senior dev 👇

🏗️ Step 1 — Fork the Repo on GitHub

Go to: https://github.com/outskill-git/GenAIEngineering-Cohort3

Click “Fork” (top-right corner)

GitHub will create a copy under your account → e.g.
https://github.com/YOUR-USERNAME/GenAIEngineering-Cohort3

This is now your own remote repo.

🏗️ Step 2 — Clone Your Fork Locally

In your machine:

git clone https://github.com/YOUR-USERNAME/GenAIEngineering-Cohort3.git
cd GenAIEngineering-Cohort3


This sets your local repo’s origin remote to your fork.

🏗️ Step 3 — Add the Original Repo as upstream Remote

This lets you pull updates from the original repo:

git remote add upstream https://github.com/outskill-git/GenAIEngineering-Cohort3.git


Check remotes:

git remote -v


You should see:

origin    https://github.com/YOUR-USERNAME/GenAIEngineering-Cohort3.git (fetch)
origin    https://github.com/YOUR-USERNAME/GenAIEngineering-Cohort3.git (push)
upstream  https://github.com/outskill-git/GenAIEngineering-Cohort3.git (fetch)
upstream  https://github.com/outskill-git/GenAIEngineering-Cohort3.git (push)

🏗️ Step 4 — Pull Updates from Original Repo

Whenever the original repo is updated:

git fetch upstream
git merge upstream/main   # or master, depending on branch name


**Or do it in one command:**

**git pull upstream main**


This merges the new changes into your local main branch.

**Then push to your fork (not original):**

**git push origin main**

🏗️ Step 5 — Push Your Changes to Your Fork Only

When you make changes locally:

git add .
git commit -m "Your changes"
git push origin main


This pushes to your own repo (origin) not to the original.

📝 Commands Summary
Action	Command
Clone your fork	git clone <your-fork-url>
Add original repo as upstream	git remote add upstream <original-url>
Fetch new changes from original	git fetch upstream
Merge updates into your main branch	git merge upstream/main
Push your changes to your fork	git push origin main
🧠 Visual Mental Model

origin → your fork (your remote)

upstream → original repo

You:

pull updates from upstream

push updates to origin

You never push directly to upstream.
