def compute_checksum(data):
    if len(data) == 0:
        return 0
    
    checksum = 0
    for i in range(0, len(data), 2):
        if i + 1 < len(data):
            word = (data[i] << 8) | data[i + 1]
        else:
            word = (data[i] << 8)
        checksum += word
        checksum = (checksum & 0xffff) + (checksum >> 16)
    
    checksum = (checksum & 0xffff) + (checksum >> 16)
    return (~checksum) & 0xffff


def verify_checksum(data, checksum):
    return compute_checksum(data) == checksum
