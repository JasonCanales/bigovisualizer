#!/bin/bash

# -------------------------------
# Big-O Visualizer Dynamic Deployment Script
# -------------------------------
# - Prompts for commit message
# - Updates backend via AWS SAM
# - Syncs frontend to S3
# - Invalidates CloudFront cache
# -------------------------------

# Settings
S3_BUCKET="jasoncanales-bigovisualizer"
CLOUDFRONT_DIST_ID="E192HU619WNWHB"

# Prompt for commit message
read -rp "🔧 Enter a brief Git commit message: " COMMIT_MSG

# Commit to Git
echo "📦 Committing changes to Git..."
git add .
git commit -m "$COMMIT_MSG"

# Push to GitHub
echo "🚀 Pushing to GitHub..."
git push

# Deploy backend via AWS SAM
echo "🔁 Deploying Lambda backend..."
cd bigovisualizer || exit
sam deploy --no-confirm-changeset --no-fail-on-empty-changeset
cd ..

# Sync frontend to S3
echo "📡 Syncing frontend to S3..."
aws s3 sync frontend/ s3://$S3_BUCKET --delete

# Invalidate CloudFront cache
echo "🧹 Invalidating CloudFront cache..."
aws cloudfront create-invalidation \
  --distribution-id "$CLOUDFRONT_DIST_ID" \
  --paths "/*"

echo "✅ Deployment complete!"
echo "🌐 Live site: https://$CLOUDFRONT_DIST_ID.cloudfront.net"