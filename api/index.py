import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.ocr import OCRService
from app.services.llm import LLMService
from app.utils.confidence import calculate_confidence
from app.utils.file_utils import validate_file
import json
from typing import Dict, Any

def handler(event, context):
    """Vercel serverless function handler"""
    try:
        # Only handle POST requests to /api/v1/extract
        if event.get('httpMethod') != 'POST':
            return {
                'statusCode': 405,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Method not allowed'})
            }

        # Check if this is the extract endpoint
        path = event.get('path', '')
        if not path.endswith('/api/v1/extract'):
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Endpoint not found'})
            }

        # Get the file from the request
        if 'body' not in event or not event['body']:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'No file provided'})
            }

        # For Vercel, file handling is more complex
        # This is a simplified version - you might need to adjust based on how Vercel handles multipart
        return {
            'statusCode': 501,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'File upload not implemented for Vercel deployment'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }

# For local testing
if __name__ == '__main__':
    print("This is a Vercel serverless function. Deploy to Vercel to test.")