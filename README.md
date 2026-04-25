# GCP MCP Log Diagnostics

This project provides tools for diagnosing Google Cloud Platform (GCP) logs using the Model Context Protocol (MCP) and Google Gemini AI.

## Overview

- `diagnose.py`: A script that uses Gemini AI to analyze GCP logs fetched via MCP tools. It diagnoses issues, identifies root causes, and suggests fixes.
- `log_mcp_server.py`: An MCP server that exposes tools for fetching logs from GCP Cloud Logging.

## Prerequisites

- Python 3.8+
- Google Cloud Project with appropriate permissions for Cloud Logging
- Gemini API key

## Setup

1. Clone or download the project files.

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables in a `.env` file:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   Ensure your Google Cloud credentials are configured (e.g., via `gcloud auth application-default login`).

4. Run the diagnosis:
   ```
   python diagnose.py
   ```

## Usage

The `diagnose.py` script is configured to fetch the last 2 hours of ERROR and CRITICAL logs from Cloud Run and provide a diagnosis. You can modify the query in the script or extend it for other resource types.

## Dependencies

- `python-dotenv`: For loading environment variables
- `google-generativeai`: For interacting with Gemini AI
- `fastmcp`: For MCP client and server functionality
- `google-cloud-logging`: For accessing GCP Cloud Logging

## License

[Add license information if applicable]