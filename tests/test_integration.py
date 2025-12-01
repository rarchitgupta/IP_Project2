import sys
import os
import threading
import tempfile
import time
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from server import SimpleFTPServer
from client import SimpleFTPClient


@pytest.fixture
def temp_files():
    """Create temporary input and output files."""
    input_temp = tempfile.NamedTemporaryFile(delete=False)
    output_temp = tempfile.NamedTemporaryFile(delete=False)
    input_file = input_temp.name
    output_file = output_temp.name
    input_temp.close()
    output_temp.close()
    yield input_file, output_file
    for f in [input_file, output_file]:
        if os.path.exists(f):
            os.remove(f)


@pytest.fixture
def test_port():
    return 17736


def write_test_file(filepath, content, size=None):
    """Write content to file."""
    with open(filepath, 'wb') as f:
        if size:
            f.write(content * (size // len(content) + 1))
            f.seek(size)
            f.truncate()
        else:
            f.write(content)


def test_stop_and_wait_small_file(temp_files, test_port):
    """Stop-and-wait (N=1) should transfer small file correctly."""
    input_file, output_file = temp_files
    test_data = b'Hello, World!'
    write_test_file(input_file, test_data)
    
    server = SimpleFTPServer(test_port, output_file, 0.0)
    client = SimpleFTPClient('127.0.0.1', test_port, input_file, 1, 8)
    
    def run_server():
        server.start()
        server.run()
    
    def run_client():
        time.sleep(0.2)
        client.start()
        client.run()
    
    server_thread = threading.Thread(target=run_server)
    client_thread = threading.Thread(target=run_client)
    
    server_thread.start()
    client_thread.start()
    
    client_thread.join(timeout=5)
    server.stop()
    server_thread.join(timeout=1)
    
    with open(output_file, 'rb') as f:
        received = f.read()
    assert received == test_data


def test_window_size_greater_than_one(temp_files, test_port):
    """Window size > 1 should transfer data with pipelining."""
    input_file, output_file = temp_files
    test_data = b'x' * 500
    write_test_file(input_file, test_data)
    
    server = SimpleFTPServer(test_port, output_file, 0.0)
    client = SimpleFTPClient('127.0.0.1', test_port, input_file, 4, 100)
    
    def run_server():
        server.start()
        server.run()
    
    def run_client():
        time.sleep(0.2)
        client.start()
        client.run()
    
    server_thread = threading.Thread(target=run_server)
    client_thread = threading.Thread(target=run_client)
    
    server_thread.start()
    client_thread.start()
    
    client_thread.join(timeout=5)
    server.stop()
    server_thread.join(timeout=1)
    
    with open(output_file, 'rb') as f:
        received = f.read()
    assert received == test_data


def test_data_integrity(temp_files, test_port):
    """Transferred data should match original file."""
    input_file, output_file = temp_files
    test_data = b'The quick brown fox jumps over the lazy dog' * 10
    write_test_file(input_file, test_data)
    
    server = SimpleFTPServer(test_port, output_file, 0.0)
    client = SimpleFTPClient('127.0.0.1', test_port, input_file, 8, 64)
    
    def run_server():
        server.start()
        server.run()
    
    def run_client():
        time.sleep(0.2)
        client.start()
        client.run()
    
    server_thread = threading.Thread(target=run_server)
    client_thread = threading.Thread(target=run_client)
    
    server_thread.start()
    client_thread.start()
    
    client_thread.join(timeout=5)
    server.stop()
    server_thread.join(timeout=1)
    
    with open(output_file, 'rb') as f:
        received = f.read()
    assert received == test_data


def test_last_segment_less_than_mss(temp_files, test_port):
    """Last segment smaller than MSS should be handled correctly."""
    input_file, output_file = temp_files
    test_data = b'x' * 250
    write_test_file(input_file, test_data)
    
    server = SimpleFTPServer(test_port, output_file, 0.0)
    client = SimpleFTPClient('127.0.0.1', test_port, input_file, 2, 100)
    
    def run_server():
        server.start()
        server.run()
    
    def run_client():
        time.sleep(0.2)
        client.start()
        client.run()
    
    server_thread = threading.Thread(target=run_server)
    client_thread = threading.Thread(target=run_client)
    
    server_thread.start()
    client_thread.start()
    
    client_thread.join(timeout=5)
    server.stop()
    server_thread.join(timeout=1)
    
    with open(output_file, 'rb') as f:
        received = f.read()
    assert received == test_data
