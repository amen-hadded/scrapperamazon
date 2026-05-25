# Pre-Publication Checklist ✅

Follow this checklist before publishing scrapperAmazon to GitHub and PyPI.

## Step 1: Update Personal Information

- [ ] Open `setup.py`
  - [ ] Change `author="Your Name"` to your name
  - [ ] Change `author_email="your.email@example.com"` to your email
  - [ ] Change URL from `yourusername` to your GitHub username

- [ ] Open `pyproject.toml`
  - [ ] Change author name and email
  - [ ] Update GitHub URLs with your username

- [ ] Open `README.md`
  - [ ] Update GitHub URLs with your username
  - [ ] Review features list
  - [ ] Update contact information

- [ ] Open `WINDOWS_GUIDE.md`
  - [ ] Update GitHub issue URL with your username

- [ ] Open `PUBLISHING.md`
  - [ ] Update GitHub URLs with your username

- [ ] Open `LICENSE`
  - [ ] Change copyright year if needed
  - [ ] Change name to your name

## Step 2: Verify Project Files

- [ ] Check `requirements.txt` - all dependencies listed
- [ ] Check `setup.py` - correct package name
- [ ] Check `pyproject.toml` - matches setup.py
- [ ] Check `MANIFEST.in` - includes necessary files
- [ ] Check `.gitignore` - covers all temporary files

## Step 3: Test Installation Locally

```bash
# In project directory
pip install -e .

# Test the command
scrapperAmazon --version
scrapperAmazon list-countries
scrapperAmazon scrape --help
```

- [ ] Installation works without errors
- [ ] Commands execute successfully
- [ ] Help text displays correctly

## Step 4: Set Up GitHub

- [ ] Created GitHub account (if needed)
- [ ] Created new repository named `scrapperAmazon`
- [ ] Repository is set to Public
- [ ] Repository has a description

## Step 5: Push to GitHub

```bash
cd scrapperAmazon
git init
git add .
git commit -m "Initial commit: Add scrapperAmazon CLI tool"
git remote add origin https://github.com/yourusername/scrapperAmazon.git
git branch -M main
git push -u origin main
```

- [ ] Repository initialized with git
- [ ] All files committed
- [ ] Pushed to GitHub successfully
- [ ] Files visible on GitHub.com

## Step 6: Set Up GitHub Actions

- [ ] Checked `.github/workflows/` directory exists
- [ ] Files `python-package.yml` and `publish.yml` present
- [ ] Actions tab shows workflows

## Step 7: Set Up PyPI

- [ ] Created PyPI account (https://pypi.org)
- [ ] Verified email address
- [ ] Created API token
- [ ] Token has "Entire repository" scope

## Step 8: Configure GitHub Secrets

1. Go to GitHub repository
2. Settings → Secrets and variables → Actions
3. New repository secret:
   - [ ] Name: `PYPI_API_TOKEN`
   - [ ] Value: Your PyPI token
   - [ ] Add secret

## Step 9: Create First Release

On GitHub:

1. Click "Releases"
2. Click "Create a new release"
3. Tag: `v1.0.0`
4. Release title: `Version 1.0.0`
5. Add description (copy from README)
6. Publish release

- [ ] First release created
- [ ] GitHub Actions started automatically
- [ ] Check Actions tab for build status

## Step 10: Verify PyPI Publication

```bash
# Create test environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from PyPI
pip install scrapperAmazon

# Test
scrapperAmazon --version

# Clean up
deactivate
```

- [ ] Package installs from PyPI without errors
- [ ] Commands work after PyPI installation
- [ ] Ready for public use!

## Step 11: Final Documentation Review

- [ ] README.md is complete and accurate
- [ ] QUICKSTART.md covers basic usage
- [ ] WINDOWS_GUIDE.md has clear steps
- [ ] PUBLISHING.md explains deployment
- [ ] CONTRIBUTING.md welcomes contributors
- [ ] Examples are working and documented
- [ ] All links in docs point to correct URLs

## Step 12: Post-Publication

After successful publication:

- [ ] Create a GitHub Pages site (optional)
- [ ] Share on social media/dev communities
- [ ] Monitor issues and pull requests
- [ ] Respond to user questions
- [ ] Plan next feature releases
- [ ] Update CHANGELOG with versions

## Testing Checklist

Before publishing, test these scenarios:

- [ ] `pip install -e .` works
- [ ] `pip install scrapperAmazon` works (after PyPI publication)
- [ ] `scrapperAmazon --version` outputs version
- [ ] `scrapperAmazon --help` shows help text
- [ ] `scrapperAmazon list-countries` lists countries
- [ ] `scrapperAmazon scrape -q "test"` executes
- [ ] Python examples run without errors
- [ ] CSV output files are created with proper format

## Deployment Commands Reference

```bash
# Local development
pip install -e .

# Test after installation
scrapperAmazon --version

# Push code to GitHub
git add .
git commit -m "message"
git push origin main

# Create a release (triggers PyPI publication)
git tag v1.0.0
git push origin v1.0.0

# Or use GitHub UI:
# Go to Releases → Create new release

# After PyPI publication, users can install with:
pip install scrapperAmazon
```

## Common Mistakes to Avoid

❌ **DON'T:**

- Leave "Your Name" in setup.py
- Forget to update GitHub URLs
- Push without testing locally first
- Publish without setting GitHub Secrets
- Use private repository (should be Public)
- Skip writing documentation

✅ **DO:**

- Test locally before publishing
- Update all author information
- Set up GitHub Secrets correctly
- Keep version numbers consistent
- Document everything well
- Respond to user feedback

## Quick Reference

| File             | What to Update            |
| ---------------- | ------------------------- |
| setup.py         | author, author_email, url |
| pyproject.toml   | author, urls              |
| README.md        | GitHub URLs, contact      |
| LICENSE          | copyright year and name   |
| WINDOWS_GUIDE.md | GitHub URLs               |
| PUBLISHING.md    | GitHub URLs               |

## Success Indicators

When everything is set up correctly:

✅ GitHub repository exists and is public
✅ Code is pushed to main branch
✅ GitHub Actions workflows are active
✅ Package appears on PyPI
✅ `pip install scrapperAmazon` works
✅ CLI commands are functional
✅ Documentation is complete

## Support

If you encounter issues:

1. Check GitHub Actions logs for errors
2. Review setup.py and pyproject.toml syntax
3. Verify PyPI API token is correct
4. Check that dependencies are listed
5. Review error messages carefully

## Next Releases

For future releases:

1. Update version in setup.py and **init**.py
2. Update CHANGELOG.md
3. Create git tag: `git tag vX.X.X`
4. Push tag: `git push origin vX.X.X`
5. Create release on GitHub
6. GitHub Actions handles PyPI publication

---

**Estimated Time**: 30-45 minutes
**Difficulty**: Beginner-Friendly
**Result**: Production-Ready Package Published to PyPI! 🎉
