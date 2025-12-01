import sys
import os
import struct
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from packet import DataPacket, AckPacket, PACKET_TYPE_DATA, PACKET_TYPE_ACK


def test_data_packet_serialize_deserialize():
    """Serialize and deserialize should match."""
    seq = 42
    data = b'test payload'
    pkt = DataPacket(seq, data)
    
    serialized = pkt.serialize()
    deserialized = DataPacket.deserialize(serialized)
    
    assert deserialized is not None
    assert deserialized.seq_num == seq
    assert deserialized.data == data


def test_data_packet_type_in_header():
    """Packet type should be 0x5555."""
    pkt = DataPacket(0, b'data')
    serialized = pkt.serialize()
    _, _, pkt_type = struct.unpack('!IHH', serialized[:8])
    assert pkt_type == PACKET_TYPE_DATA


def test_data_packet_checksum_in_header():
    """Checksum should be in packet header."""
    data = b'test'
    pkt = DataPacket(0, data)
    assert pkt.checksum > 0


def test_data_packet_empty_payload():
    """Packet with empty payload should serialize."""
    pkt = DataPacket(1, b'')
    serialized = pkt.serialize()
    deserialized = DataPacket.deserialize(serialized)
    assert deserialized is not None
    assert deserialized.data == b''


def test_data_packet_large_payload():
    """Packet with large payload should serialize."""
    data = b'x' * 5000
    pkt = DataPacket(100, data)
    serialized = pkt.serialize()
    deserialized = DataPacket.deserialize(serialized)
    assert deserialized is not None
    assert deserialized.data == data


def test_data_packet_corrupted_checksum():
    """Packet with corrupted data should fail deserialization."""
    pkt = DataPacket(0, b'original')
    serialized = bytearray(pkt.serialize())
    serialized[-1] ^= 0xff
    result = DataPacket.deserialize(bytes(serialized))
    assert result is None


def test_data_packet_wrong_type():
    """Packet with wrong type should fail deserialization."""
    header = struct.pack('!IHH', 0, 0, PACKET_TYPE_ACK)
    result = DataPacket.deserialize(header)
    assert result is None


def test_ack_packet_serialize_deserialize():
    """Serialize and deserialize should match."""
    ack_seq = 99
    pkt = AckPacket(ack_seq)
    
    serialized = pkt.serialize()
    deserialized = AckPacket.deserialize(serialized)
    
    assert deserialized is not None
    assert deserialized.ack_seq == ack_seq


def test_ack_packet_type_in_header():
    """ACK packet type should be 0xaaaa."""
    pkt = AckPacket(0)
    serialized = pkt.serialize()
    _, _, pkt_type = struct.unpack('!IHH', serialized)
    assert pkt_type == PACKET_TYPE_ACK


def test_ack_packet_checksum_zero():
    """ACK packet checksum field should be zero."""
    pkt = AckPacket(0)
    serialized = pkt.serialize()
    _, checksum, _ = struct.unpack('!IHH', serialized)
    assert checksum == 0


def test_ack_packet_size():
    """ACK packet should be exactly 8 bytes."""
    pkt = AckPacket(0)
    serialized = pkt.serialize()
    assert len(serialized) == 8


def test_ack_packet_wrong_type():
    """ACK with wrong type should fail deserialization."""
    header = struct.pack('!IHH', 0, 0, PACKET_TYPE_DATA)
    result = AckPacket.deserialize(header)
    assert result is None


def test_ack_packet_wrong_checksum_field():
    """ACK with non-zero checksum field should fail."""
    header = struct.pack('!IHH', 0, 1, PACKET_TYPE_ACK)
    result = AckPacket.deserialize(header)
    assert result is None


def test_ack_packet_wrong_size():
    """ACK packet with wrong size should fail."""
    result = AckPacket.deserialize(b'short')
    assert result is None
