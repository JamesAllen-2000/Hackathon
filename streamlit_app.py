import streamlit as st
import requests
import json
import time
import base64
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Browser Test Automation POC",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for live monitoring
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.screenshot-container {
    border: 2px solid #e0e0e0;
    border-radius: 10px;
    padding: 10px;
    background-color: #f9f9f9;
    margin: 10px 0;
}
.step-indicator {
    background-color: #4CAF50;
    color: white;
    padding: 5px 10px;
    border-radius: 15px;
    font-size: 0.8rem;
    margin: 5px 0;
}
.live-status {
    background-color: #2196F3;
    color: white;
    padding: 10px;
    border-radius: 5px;
    text-align: center;
    margin: 10px 0;
}
.success {
    background-color: #d4edda;
    color: #155724;
    padding: 0.5rem;
    border-radius: 0.25rem;
}
.error {
    background-color: #f8d7da;
    color: #721c24;
    padding: 0.5rem;
    border-radius: 0.25rem;
}
.warning {
    background-color: #fff3cd;
    color: #856404;
    padding: 0.5rem;
    border-radius: 0.25rem;
}
.passed {
    background-color: #d1edff;
    color: #0c5460;
    padding: 0.5rem;
    border-radius: 0.25rem;
    font-weight: bold;
}
.failed {
    background-color: #f8d7da;
    color: #721c24;
    padding: 0.5rem;
    border-radius: 0.25rem;
    font-weight: bold;
}
.partial {
    background-color: #fff3cd;
    color: #856404;
    padding: 0.5rem;
    border-radius: 0.25rem;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


# API Configuration
API_BASE_URL = "http://localhost:7860"

def call_test_api(test_data):
    """Call the test execution API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/run-test",
            json=test_data,
            timeout=300
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API call failed: {str(e)}")
        return None

def check_api_health():
    """Check if the API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

# Initialize session state for live monitoring
if 'screenshots' not in st.session_state:
    st.session_state.screenshots = []
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'test_status' not in st.session_state:
    st.session_state.test_status = "Ready"
if 'execution_log' not in st.session_state:
    st.session_state.execution_log = []
#Sidebar
with st.sidebar:
    st.header(" Test Configuration")
    
    # Test details
    test_url = st.text_input(
        "🌐 Target URL",
        placeholder="https://example.com",
        help="The website URL where the test will be executed"
    )
    
    test_title = st.text_input(
        "📋 Test Title",
        placeholder="Login functionality test",
        help="A descriptive title for your test case"
    )
    
    expected_outcome = st.text_area(
        "🎯 Expected Outcome",
        placeholder="User should be successfully logged in...",
        help="Describe what should happen if the test passes"
    )
    
    st.subheader("📋 Test Steps")
    st.info("Add up to 10 test steps. Leave unused steps empty.")
    
    # Create step inputs
    steps = {}
    for i in range(1, 11):
        step_value = st.text_input(
            f"Step {i}",
            key=f"step_{i}",
            placeholder=f"e.g., Enter username as 'testuser'" if i == 1 else "",
            help=f"Define action for step {i}"
        )
        if step_value.strip():
            steps[f"step{i}"] = step_value
            
    st.markdown("---")

    st.subheader(" AI Model")
    st.info("Using Google Gemini Flash for browser automation")
    
    st.subheader(" Current Test Status")
    st.info(f"Status: {st.session_state.test_status}")
    if st.session_state.current_step > 0:
        st.info(f"Screenshots: {len(st.session_state.screenshots)}")
# Main title
st.markdown('<h1 class="main-header"> Browser Test Automation POC</h1>', unsafe_allow_html=True)
st.markdown("---")

# Check API health
if not check_api_health():
    st.error("⚠️ API server is not running. Please start the API server first.")
    st.code("python api.py")
    st.stop()
else:
    st.success("✅ API server is running")

# Create three columns: Test Config, Live Monitor, Results
col_monitor, col_results = st.columns([1.2, 1])

with col_monitor:
    st.header(" Live Execution Monitor")
    
    status_placeholder = st.empty()
    status_placeholder.markdown(f'<div class="live-status">Status: {st.session_state.test_status}</div>', unsafe_allow_html=True)
    
    step_placeholder = st.empty()
    if st.session_state.current_step > 0:
        step_placeholder.markdown(f'<div class="step-indicator">Current Step: {st.session_state.current_step}</div>', unsafe_allow_html=True)
    
    screenshot_placeholder = st.empty()
    
    if st.session_state.screenshots:
        latest_screenshot = st.session_state.screenshots[-1]
        try:
            screenshot_data = base64.b64decode(latest_screenshot)
            screenshot_placeholder.image(
                screenshot_data, 
                caption=f"Step {len(st.session_state.screenshots)} - Live Browser View",
                use_column_width=True
            )
        except Exception as e:
            screenshot_placeholder.error(f"Error displaying screenshot: {str(e)}")
    else:
        screenshot_placeholder.info(" Screenshots will appear here during test execution")
    
    if len(st.session_state.screenshots) > 1:
        st.subheader("📸 Screenshot History")
        for i, screenshot in enumerate(st.session_state.screenshots[:-1], 1):
            with st.expander(f"Step {i} Screenshot"):
                try:
                    screenshot_data = base64.b64decode(screenshot)
                    st.image(screenshot_data, caption=f"Step {i}", use_column_width=True)
                except Exception as e:
                    st.error(f"Error displaying screenshot {i}: {str(e)}")

with col_results:
    st.header(" Test Execution & Results")
    
    with st.expander("📄 Example Test Payload"):
        st.json({
            "URL": "https://example.com/login",
            "Title": "User Login Test",
            "Steps": {
                "step1": "Enter username as 'testuser'",
                "step2": "Enter password as 'password123'",
            },
            "Expected_Outcome": "User must be able to log in successfully"
        })
    
    if st.button(" Execute Test with Live Monitoring", type="primary", use_container_width=True):
        if not test_url or not test_title or not expected_outcome:
            st.error("Please fill in all required fields in the sidebar (URL, Title, Expected Outcome)")
        elif not steps:
            st.error("Please add at least one test step in the sidebar")
        else:
            st.session_state.screenshots = []
            st.session_state.current_step = 0
            st.session_state.test_status = "Executing..."
            st.session_state.execution_log = []
            
            test_data = {
                "URL": test_url,
                "Title": test_title,
                "Steps": steps,
                "Expected_Outcome": expected_outcome
            }
            
            with st.expander("📤 Request Payload"):
                st.json(test_data)
            
            with st.spinner(" Executing test with live monitoring..."):
                result = call_test_api(test_data)
            
            if result:
                if 'screenshots' in result and result['screenshots']:
                    st.session_state.screenshots = result['screenshots']
                    st.session_state.current_step = len(result['screenshots'])
                
                st.session_state.test_status = result.get('status', 'completed').upper()
                st.session_state.execution_log = result.get('execution_log', [])
                
                st.success("✅ Test execution completed!")
                
                st.subheader("📊 Test Results")
                
                status = result.get("status", "unknown")
                if status == "passed":
                    st.markdown('<div class="passed">✅ TEST PASSED</div>', unsafe_allow_html=True)
                elif status == "failed":
                    st.markdown('<div class="failed">❌ TEST FAILED</div>', unsafe_allow_html=True)
                elif status == "partial":
                    st.markdown('<div class="partial">⚠️ TEST PARTIAL</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="warning">⚠️ TEST STATUS UNKNOWN</div>', unsafe_allow_html=True)
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Test ID", result.get("test_id", "N/A"))
                    st.metric("Screenshots Captured", len(result.get("screenshots", [])))
                
                with col_b:
                    st.metric("Execution Time", f"{result.get('execution_time_seconds', 0):.2f}s")
                    st.metric("Status", status.upper())
                
                st.subheader("🎯 Expected vs Actual Outcome")
                col_exp, col_act = st.columns(2)
                with col_exp:
                    st.text_area("Expected Outcome", result.get("expected_outcome", ""), disabled=True, key="expected_out")
                with col_act:
                    st.text_area("Actual Outcome", result.get("actual_outcome", ""), disabled=True, key="actual_out")
                
                st.subheader("🔍 Comparison Analysis")
                st.text_area("Analysis", result.get("comparison_result", ""), disabled=True, key="comparison")
                
                st.subheader("📋 Execution Log")
                for i, log_entry in enumerate(result.get("execution_log", []), 1):
                    st.text(f"{i:2d}. {log_entry}")
                
                st.subheader("💾 Download Results")
                result_json = json.dumps(result, indent=2)
                st.download_button(
                    label="📥 Download Test Results (JSON)",
                    data=result_json,
                    file_name=f"test_results_{result.get('test_id', 'unknown')}.json",
                    mime="application/json"
                )
            
            st.rerun()

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center;'>Built with ❤️ using Gemini</div>", unsafe_allow_html=True)
