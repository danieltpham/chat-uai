import pytest
import httpx
import socket
import os

# Test server configuration - assumes server is already running
TEST_HOST = "127.0.0.1"
TEST_PORT = 8000  # Default FastAPI port from run.py
BASE_URL = f"http://{TEST_HOST}:{TEST_PORT}"

# Test configuration

def safe_json_response(response):
    """Safely get JSON from response, with better error messages"""
    try:
        return response.json()
    except Exception as e:
        print(f"Failed to parse JSON from response (status {response.status_code}): {response.text[:200]}")
        raise

def safe_request(client, method, url, **kwargs):
    """Make a request with retry logic for connection issues"""
    import time
    import json
    max_retries = 5
    
    for attempt in range(max_retries):
        try:
            response = getattr(client, method.lower())(url, **kwargs)
            
            # Validate response can be parsed as JSON for endpoints that should return JSON
            if response.headers.get("content-type", "").startswith("application/json"):
                try:
                    response.json()  # Test if JSON is valid
                except json.JSONDecodeError:
                    if attempt < max_retries - 1:
                        print(f"Invalid JSON response, retrying... (attempt {attempt + 1})")
                        time.sleep(1.0 * (attempt + 1))
                        continue
                    raise
            
            return response
            
        except (httpx.ReadError, httpx.ConnectError, httpx.TimeoutException) as e:
            if attempt < max_retries - 1:
                error_msg = str(e)
                if "forcibly closed" in error_msg or "connection" in error_msg.lower():
                    print(f"Connection issue, retrying... (attempt {attempt + 1}): {error_msg}")
                    time.sleep(1.0 * (attempt + 1))  # Exponential backoff
                    continue
            raise
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Request failed, retrying... (attempt {attempt + 1}): {e}")
                time.sleep(1.0 * (attempt + 1))
                continue
            raise
    
    raise Exception(f"Failed after {max_retries} attempts")

def is_server_running(host, port):
    """Check if server is running"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            return result == 0
    except:
        return False

@pytest.fixture(scope="session", autouse=True)
def verify_server():
    """Verify that the server is running before tests start"""
    if not is_server_running(TEST_HOST, TEST_PORT):
        pytest.exit(f"Server not running on {BASE_URL}. Please start the server first with: python run.py")
    
    # Test server health
    try:
        import httpx
        client = httpx.Client(base_url=BASE_URL, timeout=5.0)
        response = client.get("/health")
        if response.status_code != 200:
            pytest.exit(f"Server health check failed. Expected 200, got {response.status_code}")
        print(f"✓ Server is healthy at {BASE_URL}")
        client.close()
    except Exception as e:
        pytest.exit(f"Failed to connect to server at {BASE_URL}: {e}")

@pytest.fixture(scope="session")
def client():
    """Create an HTTP client for integration tests"""
    # Create a more resilient client configuration
    transport = httpx.HTTPTransport(
        retries=3,
        verify=False  # Disable SSL verification for local testing
    )
    
    return httpx.Client(
        base_url=BASE_URL, 
        timeout=httpx.Timeout(30.0, connect=10.0),
        limits=httpx.Limits(
            max_connections=10, 
            max_keepalive_connections=5,
            keepalive_expiry=30.0
        ),
        transport=transport,
        headers={"Connection": "keep-alive"}
    )

@pytest.fixture
def async_client():
    """Create an async HTTP client for integration tests"""
    return httpx.AsyncClient(base_url=BASE_URL, timeout=30.0)

class RetryClient:
    """Wrapper for httpx.Client with automatic retry logic"""
    
    def __init__(self, client):
        self.client = client
    
    def get(self, url, **kwargs):
        return safe_request(self.client, "GET", url, **kwargs)
    
    def post(self, url, **kwargs):
        return safe_request(self.client, "POST", url, **kwargs)
    
    def put(self, url, **kwargs):
        return safe_request(self.client, "PUT", url, **kwargs)
    
    def delete(self, url, **kwargs):
        return safe_request(self.client, "DELETE", url, **kwargs)
    
    def __getattr__(self, name):
        # Delegate other attributes to the wrapped client
        return getattr(self.client, name)

@pytest.fixture(scope="session")
def retry_client(client):
    """Create a client with automatic retry logic"""
    return RetryClient(client)

# For ORM and analytics tests - use in-memory database
@pytest.fixture
def db_session():
    """Create an in-memory database session for ORM tests"""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from backend.models.star_schema import Base
    
    # Create in-memory DuckDB for testing
    test_engine = create_engine("duckdb:///:memory:")
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    
    # Create tables
    Base.metadata.create_all(bind=test_engine)
    
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()