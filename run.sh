#!/bin/bash

# Change to the directory containing this script
cd "$(dirname "$0")"

# Run the Streamlit app
uv run streamlit run dashboard/app/main.py --browser.serverAddress=0.0.0.0 --server.port=8501 "$@"
