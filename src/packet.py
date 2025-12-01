import struct
from checksum import compute_checksum, verify_checksum

PACKET_TYPE_DATA = 0x5555
PACKET_TYPE_ACK = 0xaaaa
HEADER_SIZE = 8
MAX_PAYLOAD = 65535


class DataPacket:
    def __init__(self, seq_num, data):
        self.seq_num = seq_num
        self.data = data
        self.checksum = compute_checksum(data)
    
    def serialize(self):
        header = struct.pack('!IHH', self.seq_num, self.checksum, PACKET_TYPE_DATA)
        return header + self.data
    
    @staticmethod
    def deserialize(raw):
        if len(raw) < HEADER_SIZE:
            return None
        
        header = raw[:HEADER_SIZE]
        data = raw[HEADER_SIZE:]
        
        seq_num, checksum, pkt_type = struct.unpack('!IHH', header)
        
        if pkt_type != PACKET_TYPE_DATA:
            return None
        
        if not verify_checksum(data, checksum):
            return None
        
        return DataPacket(seq_num, data)


class AckPacket:
    def __init__(self, ack_seq):
        self.ack_seq = ack_seq
    
    def serialize(self):
        return struct.pack('!IHH', self.ack_seq, 0, PACKET_TYPE_ACK)
    
    @staticmethod
    def deserialize(raw):
        if len(raw) != HEADER_SIZE:
            return None
        
        ack_seq, checksum, pkt_type = struct.unpack('!IHH', raw)
        
        if pkt_type != PACKET_TYPE_ACK or checksum != 0:
            return None
        
        return AckPacket(ack_seq)
