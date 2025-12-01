import socket
import sys
import random
from packet import DataPacket, AckPacket
from constants import SERVER_PORT

class SimpleFTPServer:
    """Go-Back-N receiver."""
    
    def __init__(self, port, output_file, loss_prob):
        self.port = port
        self.output_file = output_file
        self.loss_prob = loss_prob
        self.expected_seq = 0
        self.sock = None
        self.file = None
        self.running = False
    
    def start(self):
        """Bind socket and open output file."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', self.port))
        self.sock.settimeout(0.5)
        self.file = open(self.output_file, 'wb')
        self.running = True
        print(f"Server listening on port {self.port}")
    
    def run(self):
        """Main receive loop."""
        try:
            while self.running:
                try:
                    raw, addr = self.sock.recvfrom(65535)
                    self._handle_packet(raw, addr)
                except socket.timeout:
                    pass
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()
    
    def _handle_packet(self, raw, addr):
        """Process received packet with loss simulation."""
        if random.random() <= self.loss_prob:
            # Extract sequence number from packet for loss output
            if len(raw) >= 4:
                import struct
                seq_num = struct.unpack('!I', raw[:4])[0]
                print(f"Packet loss, sequence number = {seq_num}")
            return
        
        pkt = DataPacket.deserialize(raw)
        if pkt is None:
            return
        
        # Detect new transfer: if we get segment 0 and expected is way ahead, reset
        if pkt.seq_num == 0 and self.expected_seq > 100:
            self.expected_seq = 0
        
        if pkt.seq_num == self.expected_seq:
            self.file.write(pkt.data)
            self.file.flush()
            self._send_ack(pkt.seq_num, addr)
            self.expected_seq += 1
    
    def _send_ack(self, ack_seq, addr):
        """Send ACK packet."""
        ack = AckPacket(ack_seq)
        self.sock.sendto(ack.serialize(), addr)
    
    def stop(self):
        """Cleanup."""
        self.running = False
        if self.file:
            self.file.close()
        if self.sock:
            self.sock.close()


def main():
    if len(sys.argv) != 4:
        print("Usage: python server.py <port> <output_file> <loss_probability>")
        sys.exit(1)
    
    port = int(sys.argv[1])
    output_file = sys.argv[2]
    loss_prob = float(sys.argv[3])
    
    if not (0 < loss_prob < 1):
        print("Error: loss probability must be in (0, 1)")
        sys.exit(1)
    
    server = SimpleFTPServer(port, output_file, loss_prob)
    server.start()
    server.run()


if __name__ == "__main__":
    main()
