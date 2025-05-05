#!/usr/bin/env python3
import logging
import os
from twisted.internet import reactor, protocol

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
  level=getattr(logging, log_level),
  datefmt="%Y-%m-%d %H:%M:%S %z",
  format="%(asctime)s - %(levelname)s - %(message)s"
)

class EchoIP(protocol.Protocol):
  def connectionMade(self):
    remote_ip = self.transport.getPeer().host
    remote_port = self.transport.getPeer().port
    local_ip = self.transport.getHost().host
    local_port = self.transport.getHost().port

    logging.debug("New connection: %s:%s => %s:%s" % (remote_ip, remote_port, local_ip, local_port))

    self.transport.write((remote_ip + "\n").encode('utf-8'))
    self.transport.loseConnection()

port_min = 1
port_max = 65535

def main():
    logging.info("Starting ipv4-cat service...")

    factory = protocol.ServerFactory()
    factory.protocol = EchoIP

    failed_ports = []

    for port in range(port_min, port_max):
        try:
            reactor.listenTCP(port, factory)
        except Exception as e:
            failed_ports.append(port)

    if failed_ports:
        logging.warning(f"Failed to bind to the following ports: {failed_ports}")

    reactor.run()

if __name__ == "__main__":
  main()
