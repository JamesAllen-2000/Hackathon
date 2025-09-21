---
title: Browser Test Automation POC
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
sdk_version: "4.21.0"
app_file: Dockerfile
pinned: false
---

# 🤖 Browser Test Automation POC

## Overview

This project is a **Browser Test Automation Proof of Concept** that leverages AI-powered browser automation to execute web application tests with real-time monitoring and comprehensive result analysis. Built for hackathon participation, this solution demonstrates modern web testing techniques using Google Gemini AI and provides an intuitive web interface for test configuration and execution.

## ✨ Features

- **AI-Powered Automation**: Uses Google Gemini 2.5 Flash for intelligent browser control
- **Real-time Monitoring**: Live screenshots and step-by-step progress tracking
- **Headless Browser Testing**: Executes tests without visible browser windows
- **Comprehensive Analysis**: Detailed comparison of expected vs actual outcomes
- **Web-based Interface**: User-friendly Streamlit frontend for test configuration
- **RESTful API**: FastAPI backend for scalable test execution
- **Export Capabilities**: Download test results in JSON format
- **Health Monitoring**: API status checking and error handling

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Streamlit UI   │───▶│   FastAPI API   │───▶│  AI Agent +     │
│  (Frontend)     │    │   (Backend)     │    │  Browser        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       ▼
         │                       │              ┌─────────────────┐
         │                       │              │ Target Website  │
         │                       │              └─────────────────┘
         │                       │
         │                       ▼
         │              ┌─────────────────┐
         └─────────────▶│ Screenshots &   │
                        │ Results         │
                        └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google API Key for Gemini AI
- Chrome/Chromium browser installed

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd Hackathon
```

### 2. Create Virtual Environment

#### Windows:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

#### macOS/Linux:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```bash
# Create .env file
touch .env
```

Add your Google API key to the `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

**To get a Google API key:**

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Create a new project
3. Generate an API key
4. Copy the key to your `.env` file

### 5. Run the Application

#### Terminal 1 - Start the API Server:

```bash
python api.py
```

The API server will start on `http://localhost:8000`

#### Terminal 2 - Start the Web Interface:

```bash
streamlit run streamlit_app.py
```

The web interface will open at `http://localhost:8501`

## 📖 Usage Guide

### 1. Configure Your Test

1. Open the Streamlit web interface
2. Fill in the test configuration in the sidebar:
   - **Target URL**: The website you want to test
   - **Test Title**: A descriptive name for your test
   - **Expected Outcome**: What should happen if the test passes
   - **Test Steps**: Add up to 10 specific actions (e.g., "Click login button", "Enter username as 'testuser'")

### 2. Execute the Test

1. Click "Execute Test with Live Monitoring"
2. Watch the real-time execution in the Live Monitor panel
3. View screenshots captured after each step
4. Review the comprehensive results analysis

### 3. Analyze Results

- **Test Status**: Passed/Failed/Partial with color coding
- **Execution Metrics**: Test ID, execution time, screenshot count
- **Outcome Comparison**: Expected vs actual results
- **Execution Log**: Step-by-step execution details
- **Screenshot Gallery**: Visual proof of test execution

## 🛠️ API Endpoints

### POST `/run-test`

Execute a test case with AI-powered browser automation.

**Request Body:**

```json
{
  "URL": "https://example.com/login",
  "Title": "User Login Test",
  "Steps": {
    "step1": "Enter username as 'testuser'",
    "step2": "Enter password as 'password123'",
    "step3": "Click login button"
  },
  "Expected_Outcome": "User should be successfully logged in"
}
```

**Response:**

```json
{
  "test_id": "test_1234567890",
  "title": "User Login Test",
  "url": "https://example.com/login",
  "status": "passed",
  "expected_outcome": "User should be successfully logged in",
  "actual_outcome": "Test execution completed successfully",
  "comparison_result": "SUCCESS: Test completed successfully",
  "execution_log": ["Test started at 2024-01-01T10:00:00", "..."],
  "screenshots": ["base64_encoded_screenshot_data"],
  "timestamp": "2024-01-01T10:05:00",
  "execution_time_seconds": 45.2
}
```

### GET `/health`

Check API server health status.

**Response:**

```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T10:00:00"
}
```

## 📁 Project Structure

```
Hackathon/
├── api.py                 # FastAPI backend server
├── streamlit_app.py       # Streamlit frontend interface
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── test_execution.log     # Execution logs
├── README.md             # This file
└── venv/                 # Virtual environment (created during setup)
```

## 🔧 Dependencies

- **browser-use**: AI-powered browser automation
- **fastapi**: Modern web framework for APIs
- **uvicorn**: ASGI server for FastAPI
- **streamlit**: Web framework for data science apps
- **python-dotenv**: Environment variable management
- **requests**: HTTP library for API calls
- **pydantic**: Data validation and settings

## 🎯 Use Cases

- **Web Application Testing**: Automated UI testing for web apps
- **Regression Testing**: Verify functionality after code changes
- **User Journey Testing**: End-to-end workflow validation
- **Cross-browser Testing**: Consistent behavior verification
- **Performance Monitoring**: Track execution times and success rates
- **Quality Assurance**: Automated testing for CI/CD pipelines

## 🚨 Troubleshooting

### Common Issues

1. **API Server Not Running**

   - Ensure the API server is started with `python api.py`
   - Check that port 8000 is not occupied by another process

2. **Google API Key Error**

   - Verify your `.env` file contains a valid `GOOGLE_API_KEY`
   - Ensure the API key has proper permissions for Gemini AI

3. **Browser Issues**

   - Make sure Chrome/Chromium is installed on your system
   - Check that the browser can be launched in headless mode

4. **Dependencies Issues**
   - Ensure you're using the correct Python version (3.8+)
   - Try reinstalling dependencies: `pip install -r requirements.txt --force-reinstall`

### Logs

Check the `test_execution.log` file for detailed execution logs and error messages.

## 🤝 Contributing

This project was developed for hackathon participation. For contributions or improvements:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is developed for hackathon purposes. Please check with the hackathon organizers for usage rights and licensing.

## 🏆 Hackathon Context

This Browser Test Automation POC demonstrates:

- **Innovation**: AI-powered browser automation using Google Gemini
- **Technical Excellence**: Modern web architecture with FastAPI and Streamlit
- **User Experience**: Intuitive interface for test configuration and monitoring
- **Scalability**: RESTful API design for enterprise integration
- **Real-world Application**: Practical solution for web application testing

---

**Built with ❤️ for GenAI Exchange Hackathon 2025**

_Leveraging AI to revolutionize web testing automation_
