# Deployment Manifest: Solaris Wealth Advisors

## Template
- **Source Template**: CAPACITI Phase 2
- **Target Environment**: DEV
- **AWS Region**: eu-west-1
- **AWS Account**: 536580886816

## Pre-Deployment Checks
- [ ] Site builds without errors
- [ ] All images load (Unsplash URLs accessible)
- [ ] HTML validates (W3C)
- [ ] CSS validates
- [ ] Mobile responsive verified
- [ ] Accessibility check passed

## Deployment Commands

### 1. Sync site files to S3
```bash
aws s3 sync ./stage-2-site-generation/ s3://3-0-site-builder-deployed-sites-dev/staging/solaris-wealth-advisors/ \
  --delete \
  --exclude "index.html" \
  --cache-control "max-age=31536000, immutable" \
  --profile Tebogo-dev
```

### 2. Upload index.html (no-cache)
```bash
aws s3 cp ./stage-2-site-generation/index.html s3://3-0-site-builder-deployed-sites-dev/staging/solaris-wealth-advisors/index.html \
  --cache-control "no-cache, no-store, must-revalidate" \
  --content-type "text/html" \
  --profile Tebogo-dev
```

### 3. Invalidate CloudFront cache
```bash
aws cloudfront create-invalidation \
  --distribution-id STAGING_DISTRIBUTION \
  --paths "/*" \
  --profile Tebogo-dev
```

## Post-Deployment Verification
- [ ] Staging URL returns 200: `https://dev.solaris-wealth-advisors.preview.example.com`
- [ ] Page title matches: "Solaris Wealth Advisors — Clarity in every financial decision"
- [ ] CSS loads with correct content-type
- [ ] No mixed content warnings
- [ ] No console errors

## Rollback Plan
If deployment fails or verification checks do not pass:
1. Identify the last known good deployment in S3 versioning
2. Restore previous version of `index.html` and assets
3. Invalidate CloudFront cache again
4. Re-run post-deployment verification
