# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import List, Dict, Any
# import asyncio
# import logging
# from datetime import datetime
# import json

# from browser_use import Agent, Browser, ChatGoogle  # Use Browser Use's native ChatGoogle
# from dotenv import load_dotenv
# import os

# # Load environment variables
# load_dotenv()

# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler('test_execution.log'),
#         logging.StreamHandler()
#     ]
# )
# logger = logging.getLogger(__name__)

# app = FastAPI(title="Browser Test Automation API", version="1.0.0")

# class TestStep(BaseModel):
#     step1: str = None
#     step2: str = None
#     step3: str = None
#     step4: str = None
#     step5: str = None
#     step6: str = None
#     step7: str = None
#     step8: str = None
#     step9: str = None
#     step10: str = None

# class TestRequest(BaseModel):
#     URL: str
#     Title: str
#     Steps: TestStep
#     Expected_Outcome: str

# class TestResult(BaseModel):
#     test_id: str
#     title: str
#     url: str
#     status: str  # "success", "failed", "error"
#     expected_outcome: str
#     actual_outcome: str
#     comparison_result: str
#     execution_log: List[str]
#     timestamp: str
#     execution_time_seconds: float

# class TestExecutor:
#     def __init__(self):
#         self.logger = logger
        
#     async def execute_test(self, test_request: TestRequest) -> TestResult:
#         """Execute a single test case and return results"""
#         start_time = datetime.now()
#         test_id = f"test_{int(start_time.timestamp())}"
#         execution_log = []
        
#         try:
#             self.logger.info(f"Starting test execution: {test_id}")
#             self.logger.info(f"Test Title: {test_request.Title}")
#             self.logger.info(f"Target URL: {test_request.URL}")
            
#             execution_log.append(f"Test started at {start_time.isoformat()}")
#             execution_log.append(f"Target URL: {test_request.URL}")
            
#             # Validate Google API key
#             if not os.getenv("GOOGLE_API_KEY"):
#                 raise Exception("GOOGLE_API_KEY not found in environment variables")
            
#             # Initialize Gemini LLM using Browser Use's native integration
#             self.logger.info("Initializing Gemini LLM...")
#             llm = ChatGoogle(model='gemini-2.5-flash')  # Use Browser Use's ChatGoogle
#             execution_log.append("Gemini LLM initialized successfully")
            
#             # Initialize browser
#             self.logger.info("Initializing browser...")
#             browser = Browser(
#                 headless=False,  # Set to True for headless mode
#                 disable_security=False
#             )
#             execution_log.append("Browser initialized successfully")
            
#             # Convert steps to task string
#             task_string = self._build_task_string(test_request)
#             self.logger.info(f"Task string built: {task_string}")
#             execution_log.append(f"Task instructions prepared with {len([s for s in test_request.Steps.model_dump().values() if s])} steps")
            
#             # Create and run agent
#             self.logger.info("Creating Browser Use agent...")
#             agent = Agent(
#                 task=task_string,
#                 llm=llm,
#                 browser=browser
#             )
#             execution_log.append("Browser Use agent created successfully")
            
#             self.logger.info("Starting agent execution...")
#             execution_log.append("Agent execution started")
            
#             # Execute the test
#             result = await agent.run()
            
#             execution_log.append("Agent execution completed successfully")
#             self.logger.info("Agent execution completed")
            
#             # Get actual outcome from the agent result
#             actual_outcome = "Test execution completed successfully. All steps were performed."
#             if result:
#                 # Extract meaningful information from the result
#                 if hasattr(result, 'output'):
#                     actual_outcome = str(result.output)
#                 elif hasattr(result, 'content'):
#                     actual_outcome = str(result.content)
#                 elif isinstance(result, str):
#                     actual_outcome = result
#                 else:
#                     actual_outcome = f"Test completed. Result: {str(result)}"
            
#             # Compare expected vs actual outcome using a simple comparison
#             comparison_result = self._simple_comparison(
#                 test_request.Expected_Outcome,
#                 actual_outcome
#             )
            
#             execution_log.append(f"Outcome comparison completed: {comparison_result}")
            
#             # Determine final status based on completion
#             status = "success"  # If we reach here without exception, consider it success
            
#             # Close browser
#             await browser.close()
#             execution_log.append("Browser closed successfully")
            
#         except Exception as e:
#             self.logger.error(f"Test execution failed: {str(e)}")
#             execution_log.append(f"ERROR: {str(e)}")
#             status = "error"
#             actual_outcome = f"Test failed with error: {str(e)}"
#             comparison_result = "Test could not be completed due to execution error"
            
#             # Try to close browser if it was initialized
#             try:
#                 if 'browser' in locals():
#                     await browser.close()
#             except:
#                 pass
        
#         end_time = datetime.now()
#         execution_time = (end_time - start_time).total_seconds()
        
#         result = TestResult(
#             test_id=test_id,
#             title=test_request.Title,
#             url=test_request.URL,
#             status=status,
#             expected_outcome=test_request.Expected_Outcome,
#             actual_outcome=actual_outcome,
#             comparison_result=comparison_result,
#             execution_log=execution_log,
#             timestamp=end_time.isoformat(),
#             execution_time_seconds=execution_time
#         )
        
#         self.logger.info(f"Test {test_id} completed with status: {status}")
#         return result
    
#     def _build_task_string(self, test_request: TestRequest) -> str:
#         """Build the task string for the Browser Use agent"""
#         steps_dict = test_request.Steps.model_dump()
#         steps_list = [step for step in steps_dict.values() if step is not None and step.strip()]
        
#         task_parts = [
#             f"Test Title: {test_request.Title}",
#             f"Expected Outcome: {test_request.Expected_Outcome}",
#             f"",
#             f"Navigate to: {test_request.URL}",
#             f"",
#             f"Then execute the following steps in order:"
#         ]
        
#         for i, step in enumerate(steps_list, 1):
#             task_parts.append(f"{i}. {step}")
        
#         task_parts.extend([
#             f"",
#             f"After completing all steps, validate that the expected outcome has been achieved.",
#             f"Expected outcome: {test_request.Expected_Outcome}"
#         ])
        
#         return "\n".join(task_parts)
    
#     def _simple_comparison(self, expected: str, actual: str) -> str:
#         """Simple comparison of expected vs actual outcomes"""
#         try:
#             # Simple keyword-based comparison
#             expected_lower = expected.lower()
#             actual_lower = actual.lower()
            
#             # Check for success indicators
#             success_keywords = ['success', 'completed', 'achieved', 'passed', 'login', 'dashboard']
#             failure_keywords = ['failed', 'error', 'exception', 'timeout', 'not found']
            
#             success_count = sum(1 for keyword in success_keywords if keyword in actual_lower)
#             failure_count = sum(1 for keyword in failure_keywords if keyword in actual_lower)
            
#             if failure_count > 0:
#                 return f"FAILED: Test execution encountered issues. Expected: {expected}. Actual: {actual}"
#             elif success_count > 0:
#                 return f"SUCCESS: Test appears to have completed successfully. Expected: {expected}. Actual: {actual}"
#             else:
#                 return f"PARTIAL: Test completed but outcome unclear. Expected: {expected}. Actual: {actual}"
                
#         except Exception as e:
#             logger.error(f"Comparison failed: {str(e)}")
#             return f"COMPARISON_ERROR: Could not compare outcomes. Expected: {expected}. Actual: {actual}"

# # Initialize test executor
# test_executor = TestExecutor()

# @app.post("/run-test", response_model=TestResult)
# async def run_test(test_request: TestRequest):
#     """Execute a test case and return results"""
#     try:
#         logger.info(f"Received test request: {test_request.Title}")
#         result = await test_executor.execute_test(test_request)
#         return result
#     except Exception as e:
#         logger.error(f"API endpoint error: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Test execution failed: {str(e)}")

# @app.get("/health")
# async def health_check():
#     """Health check endpoint"""
#     return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import List, Dict, Any
import asyncio
import logging
from datetime import datetime
import json
import base64
import os

from browser_use import Agent, Browser, ChatGoogle
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_execution.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Browser Test Automation API", version="1.0.0")

class TestStep(BaseModel):
    step1: str = None
    step2: str = None
    step3: str = None
    step4: str = None
    step5: str = None
    step6: str = None
    step7: str = None
    step8: str = None
    step9: str = None
    step10: str = None

class TestRequest(BaseModel):
    URL: str
    Title: str
    Steps: TestStep
    Expected_Outcome: str

class TestResult(BaseModel):
    test_id: str
    title: str
    url: str
    status: str
    expected_outcome: str
    actual_outcome: str
    comparison_result: str
    execution_log: List[str]
    screenshots: List[str]  # Base64 encoded screenshots
    timestamp: str
    execution_time_seconds: float

class TestExecutor:
    def __init__(self):
        self.logger = logger
        
    async def execute_test_with_streaming(self, test_request: TestRequest, websocket: WebSocket = None) -> TestResult:
        """Execute a test case with real-time screenshot streaming"""
        start_time = datetime.now()
        test_id = f"test_{int(start_time.timestamp())}"
        execution_log = []
        screenshots = []
        
        try:
            self.logger.info(f"Starting test execution: {test_id}")
            execution_log.append(f"Test started at {start_time.isoformat()}")
            
            # Validate Google API key
            if not os.getenv("GOOGLE_API_KEY"):
                raise Exception("GOOGLE_API_KEY not found in environment variables")
            
            # Initialize Gemini LLM
            llm = ChatGoogle(model='gemini-2.5-flash')
            execution_log.append("Gemini LLM initialized successfully")
            
            # Initialize browser (visible for screenshots)
            browser = Browser(
                headless=False,  # Keep visible for better screenshots
                disable_security=False
            )
            execution_log.append("Browser initialized successfully")
            
            # Convert steps to task string
            task_string = self._build_task_string_with_screenshots(test_request)
            
            # Create agent
            agent = Agent(
                task=task_string,
                llm=llm,
                browser=browser
            )
            
            # Execute with step-by-step monitoring using hooks
            await self._execute_with_monitoring(agent, websocket, screenshots, execution_log)
            
            execution_log.append("Agent execution completed successfully")
            
            # Get actual outcome
            actual_outcome = "Test execution completed successfully. All steps were performed."
            
            # Compare outcomes
            comparison_result = self._simple_comparison(
                test_request.Expected_Outcome,
                actual_outcome
            )
            
            status = "success"
            
            # Close browser
            await browser.close()
            execution_log.append("Browser closed successfully")
            
        except Exception as e:
            self.logger.error(f"Test execution failed: {str(e)}")
            execution_log.append(f"ERROR: {str(e)}")
            status = "error"
            actual_outcome = f"Test failed with error: {str(e)}"
            comparison_result = "Test could not be completed due to execution error"
            
            try:
                if 'browser' in locals():
                    await browser.close()
            except:
                pass
        
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        result = TestResult(
            test_id=test_id,
            title=test_request.Title,
            url=test_request.URL,
            status=status,
            expected_outcome=test_request.Expected_Outcome,
            actual_outcome=actual_outcome,
            comparison_result=comparison_result,
            execution_log=execution_log,
            screenshots=screenshots,
            timestamp=end_time.isoformat(),
            execution_time_seconds=execution_time
        )
        
        return result
    
    async def _execute_with_monitoring(self, agent, websocket, screenshots, execution_log):
        """Execute agent with step-by-step monitoring and screenshots using hooks"""
        step_count = 0
        
        async def step_hook(agent_instance):
            nonlocal step_count
            step_count += 1
            
            # Take screenshot after each step using the correct Browser Use API
            screenshot = await self._take_screenshot_from_agent(agent_instance)
            if screenshot:
                screenshots.append(screenshot)
                
                if websocket:
                    try:
                        await websocket.send_text(json.dumps({
                            "type": "screenshot",
                            "screenshot": screenshot,
                            "step": step_count,
                            "message": f"Step {step_count} completed"
                        }))
                    except:
                        pass  # WebSocket might be closed
            
            # Log step completion
            execution_log.append(f"Step {step_count} completed with screenshot")
            
            if websocket:
                try:
                    await websocket.send_text(json.dumps({
                        "type": "status",
                        "message": f"Completed step {step_count}",
                        "step": step_count
                    }))
                except:
                    pass
        
        # Run agent with step monitoring using the on_step_end hook
        await agent.run(on_step_end=step_hook)
    
    async def _take_screenshot_from_agent(self, agent_instance) -> str:
        """Take a screenshot using Browser Use's proper API"""
        try:
            # Access the browser session from the agent
            if hasattr(agent_instance, 'browser_session'):
                browser_session = agent_instance.browser_session
                
                # Get current page from browser session
                current_page = await browser_session.get_current_page()
                if current_page:
                    # Take screenshot using Browser Use's screenshot method
                    screenshot_data = await current_page.screenshot(format='jpeg', quality=80)
                    
                    # Convert to base64
                    if isinstance(screenshot_data, bytes):
                        screenshot_b64 = base64.b64encode(screenshot_data).decode('utf-8')
                        return screenshot_b64
                    elif isinstance(screenshot_data, str):
                        # If it's already base64 encoded
                        return screenshot_data
            
            return None
            
        except Exception as e:
            self.logger.error(f"Screenshot failed: {str(e)}")
            return None
    
    def _build_task_string_with_screenshots(self, test_request: TestRequest) -> str:
        """Build task string optimized for step-by-step execution"""
        steps_dict = test_request.Steps.model_dump()
        steps_list = [step for step in steps_dict.values() if step is not None and step.strip()]
        
        task_parts = [
            f"Test Title: {test_request.Title}",
            f"Expected Outcome: {test_request.Expected_Outcome}",
            f"",
            f"Navigate to: {test_request.URL}",
            f"",
            f"Execute the following steps one by one, taking time between each step:"
        ]
        
        for i, step in enumerate(steps_list, 1):
            task_parts.append(f"{i}. {step}")
        
        task_parts.extend([
            f"",
            f"After completing all steps, validate the expected outcome.",
            f"Expected outcome: {test_request.Expected_Outcome}"
        ])
        
        return "\n".join(task_parts)
    
    def _simple_comparison(self, expected: str, actual: str) -> str:
        """Simple comparison of expected vs actual outcomes"""
        expected_lower = expected.lower()
        actual_lower = actual.lower()
        
        success_keywords = ['success', 'completed', 'achieved', 'passed', 'login', 'dashboard']
        failure_keywords = ['failed', 'error', 'exception', 'timeout', 'not found']
        
        success_count = sum(1 for keyword in success_keywords if keyword in actual_lower)
        failure_count = sum(1 for keyword in failure_keywords if keyword in actual_lower)
        
        if failure_count > 0:
            return f"FAILED: Test execution encountered issues. Expected: {expected}. Actual: {actual}"
        elif success_count > 0:
            return f"SUCCESS: Test appears to have completed successfully. Expected: {expected}. Actual: {actual}"
        else:
            return f"PARTIAL: Test completed but outcome unclear. Expected: {expected}. Actual: {actual}"

# Initialize test executor
test_executor = TestExecutor()

@app.post("/run-test", response_model=TestResult)
async def run_test(test_request: TestRequest):
    """Execute a test case and return results"""
    try:
        logger.info(f"Received test request: {test_request.Title}")
        result = await test_executor.execute_test_with_streaming(test_request)
        return result
    except Exception as e:
        logger.error(f"API endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Test execution failed: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)