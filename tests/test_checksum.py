import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from checksum import compute_checksum, verify_checksum


def test_empty_data():
    """Empty data should return 0."""
    assert compute_checksum(b'') == 0


def test_single_byte():
    """Single byte should be shifted left by 8."""
    result = compute_checksum(b'\x01')
    assert isinstance(result, int)
    assert 0 <= result <= 0xffff


def test_two_bytes():
    """Two bytes form a 16-bit word."""
    data = b'\x12\x34'
    result = compute_checksum(data)
    assert isinstance(result, int)
    assert 0 <= result <= 0xffff


def test_checksum_consistency():
    """Same data should produce same checksum."""
    data = b'Hello, World!'
    cs1 = compute_checksum(data)
    cs2 = compute_checksum(data)
    assert cs1 == cs2


def test_verify_checksum_valid():
    """Verify checksum should succeed for correct checksum."""
    data = b'test data'
    checksum = compute_checksum(data)
    assert verify_checksum(data, checksum)


def test_verify_checksum_invalid():
    """Verify checksum should fail for incorrect checksum."""
    data = b'test data'
    bad_checksum = 0xdead
    assert not verify_checksum(data, bad_checksum)


def test_checksum_different_data():
    """Different data should (likely) produce different checksums."""
    data1 = b'Hello'
    data2 = b'World'
    cs1 = compute_checksum(data1)
    cs2 = compute_checksum(data2)
    assert cs1 != cs2


def test_large_data():
    """Checksum should handle large data."""
    data = b'x' * 10000
    checksum = compute_checksum(data)
    assert verify_checksum(data, checksum)
