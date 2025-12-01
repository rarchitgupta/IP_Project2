# Simple-FTP with Go-Back-N ARQ Protocol

Reliable file transfer over UDP using Go-Back-N Automatic Repeat Request.

## Quick Start

### Build & Test

```bash
make test    # All 32 tests pass
```

### Manual Run (Local Only)

```bash
# Terminal 1: Server
python3 src/server.py 7735 output.txt 0.05

# Terminal 2: Client (N=4, MSS=500)
python3 src/client.py 127.0.0.1 7735 input.txt 4 500

# Terminal 3: Verify
diff input.txt output.txt && echo "✓ Files match"
```

## Implementation Status

- ✅ **Phase 1-4**: Complete (core protocol, testing)

  - `src/checksum.py` - UDP-style 16-bit checksums
  - `src/packet.py` - DataPacket and AckPacket serialization
  - `src/server.py` - SimpleFTPServer (Go-Back-N receiver)
  - `src/client.py` - SimpleFTPClient (Go-Back-N sender)
  - `tests/` - 32 comprehensive tests (all passing)

- 📋 **Phase 5**: Experiments
  - **TASK1.md** - Effect of window size N on transfer delay
  - TASK2.md - Coming soon
  - TASK3.md - Coming soon

## Key Parameters (All Tunable)

- **N**: Window size (segments in flight)
- **MSS**: Maximum segment size (bytes per segment)
- **p**: Packet loss probability ∈ [0, 1]

## Task 1: Window Size Experiments

See **TASK1.md** for complete instructions.

Quick summary:

- Vary N ∈ {1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024}
- Fix MSS=500, p=0.05
- Measure transfer delay over 5 runs per N value
- Average results and plot
- Compare performance across different window sizes

## Protocol Details

**Go-Back-N ARQ**:

- Sliding window at sender (client)
- In-order delivery at receiver (server)
- Timeout-based retransmission of all unACKed segments
- Probabilistic packet loss simulation

**Packet Format**:

- Data packets: seq (32-bit) + checksum (16-bit) + type=0x5555 + data
- ACK packets: seq (32-bit) + checksum=0 + type=0xAAAA
- All in network byte order

## See Also

- `PROJECT2.md` - Full specification
- `TASK1.md` - Task 1 experiment guide (window size effects)
