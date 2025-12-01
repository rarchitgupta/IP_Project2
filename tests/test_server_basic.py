import sys
import os
import socket
import threading
import tempfile
import time
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from server import SimpleFTPServer
from packet import DataPacket


@pytest.fixture
def temp_files():
    """Create temporary file for output."""
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    output_file = temp_file.name
    temp_file.close()
    yield output_file
    if os.path.exists(output_file):
        os.remove(output_file)


@pytest.fixture
def test_port():
    return 17735


def test_server_initialization(temp_files, test_port):
    """Server should initialize without errors."""
    server = SimpleFTPServer(test_port, temp_files, 0.0)
    assert server.expected_seq == 0
    assert server.loss_prob == 0.0


def test_server_socket_binding(temp_files, test_port):
    """Server should bind to socket."""
    server = SimpleFTPServer(test_port, temp_files, 0.0)
    server.start()
    assert server.sock is not None
    server.stop()


def test_server_file_creation(temp_files, test_port):
    """Server should create output file."""
    server = SimpleFTPServer(test_port, temp_files, 0.0)
    server.start()
    assert os.path.exists(temp_files)
    server.stop()


def test_server_receives_data(temp_files, test_port):
    """Server should receive and write data."""
    server = SimpleFTPServer(test_port, temp_files, 0.0)
    server.start()
    
    def send_packets():
        time.sleep(0.1)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        pkt = DataPacket(0, b'Hello')
        sock.sendto(pkt.serialize(), ('127.0.0.1', test_port))
        sock.close()
        time.sleep(0.1)
        server.stop()
    
    sender = threading.Thread(target=send_packets)
    sender.start()
    server.run()
    sender.join()
    
    with open(temp_files, 'rb') as f:
        data = f.read()
    assert data == b'Hello'


def test_server_increments_expected_seq(temp_files, test_port):
    """Server should increment expected_seq on valid packet."""
    server = SimpleFTPServer(test_port, temp_files, 0.0)
    server.start()
    
    def send_packets():
        time.sleep(0.1)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        pkt1 = DataPacket(0, b'Pkt0')
        pkt2 = DataPacket(1, b'Pkt1')
        sock.sendto(pkt1.serialize(), ('127.0.0.1', test_port))
        time.sleep(0.05)
        sock.sendto(pkt2.serialize(), ('127.0.0.1', test_port))
        sock.close()
        time.sleep(0.1)
        server.stop()
    
    sender = threading.Thread(target=send_packets)
    sender.start()
    server.run()
    sender.join()
    
    with open(temp_files, 'rb') as f:
        data = f.read()
    assert data == b'Pkt0Pkt1'


def test_server_ignores_out_of_order(temp_files, test_port):
    """Server should ignore out-of-order packets."""
    server = SimpleFTPServer(test_port, temp_files, 0.0)
    server.start()
    
    def send_packets():
        time.sleep(0.1)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        pkt1 = DataPacket(1, b'Out')
        pkt0 = DataPacket(0, b'In')
        sock.sendto(pkt1.serialize(), ('127.0.0.1', test_port))
        time.sleep(0.05)
        sock.sendto(pkt0.serialize(), ('127.0.0.1', test_port))
        sock.close()
        time.sleep(0.1)
        server.stop()
    
    sender = threading.Thread(target=send_packets)
    sender.start()
    server.run()
    sender.join()
    
    with open(temp_files, 'rb') as f:
        data = f.read()
    assert data == b'In'
