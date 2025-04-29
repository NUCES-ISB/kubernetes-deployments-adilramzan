import pytest
import json
from app.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test the index route returns correct message"""
    response = client.get('/')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert 'message' in data
    assert data['message'] == 'Welcome to Flask Kubernetes Demo'
    assert data['status'] == 'active'

def test_health_endpoint(client):
    """Test the health check endpoint"""
    response = client.get('/health')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'healthy'

def test_db_test_with_mock(monkeypatch, client):
    """Test the database endpoint with mocked connection"""
    
    
    class MockCursor:
        def execute(self, query):
            pass
            
        def fetchone(self):
            return {'count': 5}
            
        def close(self):
            pass
    
    class MockConnection:
        def __init__(self):
            self.autocommit = False
            
        def cursor(self, cursor_factory=None):
            return MockCursor()
            
        def close(self):
            pass
    
    # Patch the database connection function
    monkeypatch.setattr('app.app.get_db_connection', lambda: MockConnection())
    
    response = client.get('/db-test')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert data['database_connection'] == 'successful'
    assert data['message_count'] == 5

def test_get_messages_with_mock(monkeypatch, client):
    """Test the get messages endpoint with mocked data"""
    
    mock_messages = [
        {"id": 1, "message": "Test message 1", "created_at": "2023-01-01T12:00:00"},
        {"id": 2, "message": "Test message 2", "created_at": "2023-01-02T12:00:00"}
    ]
    
    class MockCursor:
        def execute(self, query):
            pass
            
        def fetchall(self):
            return mock_messages
            
        def close(self):
            pass
    
    class MockConnection:
        def __init__(self):
            self.autocommit = False
            
        def cursor(self, cursor_factory=None):
            return MockCursor()
            
        def close(self):
            pass
    
    # Patch the database connection function
    monkeypatch.setattr('app.app.get_db_connection', lambda: MockConnection())
    
    response = client.get('/messages')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert data['count'] == 2
    assert len(data['messages']) == 2
    assert data['messages'][0]['id'] == 1
    
def test_create_message_with_mock(monkeypatch, client):
    """Test the create message endpoint with mocked connection"""
    
    class MockCursor:
        def execute(self, query, params):
            pass
            
        def fetchone(self):
            return {"id": 3, "message": "New message", "created_at": "2023-01-03T12:00:00"}
            
        def close(self):
            pass
    
    class MockConnection:
        def __init__(self):
            self.autocommit = False
            
        def cursor(self, cursor_factory=None):
            return MockCursor()
            
        def close(self):
            pass
    
    # Patch the database connection function
    monkeypatch.setattr('app.app.get_db_connection', lambda: MockConnection())
    
    # Test creating a new message
    response = client.post('/messages', 
                         data=json.dumps({'message': 'New message'}),
                         content_type='application/json')
    data = json.loads(response.data)
    
    assert response.status_code == 201
    assert data['status'] == 'success'
    assert data['data']['id'] == 3
    assert data['data']['message'] == 'New message'

def test_create_message_invalid_data(client):
    """Test creating a message with invalid data"""
    # Test with missing message field
    response = client.post('/messages', 
                         data=json.dumps({}),
                         content_type='application/json')
    data = json.loads(response.data)
    
    assert response.status_code == 400
    assert data['status'] == 'error'
    assert 'Message field is required' in data['error']
