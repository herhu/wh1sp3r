#!/bin/bash

# CONFIGURATION
ENDPOINT_URL="https://use72hh2xh.execute-api.eu-north-1.amazonaws.com/transcribe"
RULE_NAME="whisper-warmup-http"
REGION="eu-north-1"

echo "⏰ Creating CloudWatch rule to trigger HTTP warm-up..."

aws events put-rule \
  --name "$RULE_NAME" \
  --schedule-expression "rate(5 minutes)" \
  --region "$REGION"

echo "📦 Creating Lambda target that calls your HTTP endpoint..."

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Create a lightweight Lambda that does an HTTP POST to your endpoint
HELPER_FUNCTION_NAME="warmupPinger"

aws lambda create-function --function-name "$HELPER_FUNCTION_NAME" \
  --runtime python3.10 \
  --role "arn:aws:iam::$ACCOUNT_ID:role/YourLambdaExecutionRole" \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://warmup_pinger.zip \
  --region "$REGION" || echo "🔁 Lambda may already exist."

aws events put-targets \
  --rule "$RULE_NAME" \
  --targets "[{\"Id\": \"1\", \"Arn\": \"arn:aws:lambda:$REGION:$ACCOUNT_ID:function:$HELPER_FUNCTION_NAME\"}]"

echo "🔐 Granting invoke permission to Events -> warmupPinger..."

aws lambda add-permission \
  --function-name "$HELPER_FUNCTION_NAME" \
  --statement-id "AllowExecutionFromEvents-$(date +%s)" \
  --action "lambda:InvokeFunction" \
  --principal events.amazonaws.com \
  --source-arn "arn:aws:events:$REGION:$ACCOUNT_ID:rule/$RULE_NAME"

echo "✅ Done: warm-up will POST to your Lambda every 5 minutes."
