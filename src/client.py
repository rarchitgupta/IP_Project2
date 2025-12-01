import socket
import sys
import time
import struct
from packet import DataPacket, AckPacket
from constants import HEADER_SIZE

class SimpleFTPClient:
    """Go-Back-N sender."""
    
    def __init__(self, host, port, input_file, window_size, mss):
        self.host = host
        self.port = port
        self.input_file = input_file
        self.window_size = window_size
        self.mss = mss
        
        self.sock = None
        self.file = None
        self.segments = []
        self.base = 0
        self.next_seq = 0
        self.timer = None
        self.timeout_interval = 0.5
        self.ack_buffer = b''
    
    def start(self):
        """Resolve host, create socket, open file."""
        addr_info = socket.getaddrinfo(self.host, self.port, 0, socket.SOCK_DGRAM)[0]
        self.sock = socket.socket(addr_info[0], socket.SOCK_DGRAM)
        self.sock.setblocking(False)
        self.server_addr = addr_info[4]
        
        self.file = open(self.input_file, 'rb')
        self._segment_file()
    
    def _segment_file(self):
        """Read file and create MSS-sized segments."""
        buffer = b''
        while True:
            chunk = self.file.read(1024)
            if not chunk:
                if buffer:
                    self.segments.append(buffer)
                break
            
            buffer += chunk
            while len(buffer) >= self.mss:
                self.segments.append(buffer[:self.mss])
                buffer = buffer[self.mss:]
    
    def run(self):
        """Main send loop with timeout handling."""
        try:
            while self.base < len(self.segments):
                self._send_phase()
                self._receive_phase()
                self._timeout_phase()
        finally:
            self.stop()
    
    def _send_phase(self):
        """Send packets if window has space."""
        while self.next_seq < self.base + self.window_size and self.next_seq < len(self.segments):
            pkt = DataPacket(self.next_seq, self.segments[self.next_seq])
            self.sock.sendto(pkt.serialize(), self.server_addr)
            
            if self.next_seq == self.base:
                self.timer = time.time()
            
            self.next_seq += 1
    
    def _receive_phase(self):
        """Non-blocking ACK reception with buffering."""
        try:
            chunk, _ = self.sock.recvfrom(1024)
            if chunk:
                self.ack_buffer += chunk
        except (BlockingIOError, socket.error):
            pass
        
        while len(self.ack_buffer) >= HEADER_SIZE:
            raw = self.ack_buffer[:HEADER_SIZE]
            self.ack_buffer = self.ack_buffer[HEADER_SIZE:]
            
            ack = AckPacket.deserialize(raw)
            if ack and ack.ack_seq >= self.base:
                self.base = ack.ack_seq + 1
                if self.base == self.next_seq:
                    self.timer = None
                else:
                    self.timer = time.time()
    
    def _timeout_phase(self):
        """Detect timeout and retransmit."""
        if self.timer is not None and time.time() - self.timer > self.timeout_interval:
            print(f"Timeout, sequence number = {self.base}")
            for seq in range(self.base, self.next_seq):
                pkt = DataPacket(seq, self.segments[seq])
                self.sock.sendto(pkt.serialize(), self.server_addr)
            self.timer = time.time()
    
    def stop(self):
        """Cleanup."""
        if self.file:
            self.file.close()
        if self.sock:
            self.sock.close()


def main():
    if len(sys.argv) != 6:
        print("Usage: python client.py <server_host> <server_port> <input_file> <window_size> <mss>")
        sys.exit(1)
    
    host = sys.argv[1]
    port = int(sys.argv[2])
    input_file = sys.argv[3]
    window_size = int(sys.argv[4])
    mss = int(sys.argv[5])
    
    client = SimpleFTPClient(host, port, input_file, window_size, mss)
    client.start()
    client.run()


if __name__ == "__main__":
    main()
