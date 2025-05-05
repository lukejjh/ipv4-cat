# ipv4-cat

ipv4-cat is the daemon that runs [ipv4.cat](https://about.ipv4.cat), a service I created some years ago to "cat" your public IP address out to the terminal, agnostic of OS or port; just using a good old-fashioned TCP connection, paired with ubiquitous utilities such as `ftp`, `telnet`, `nc` and `curl`. It's designed to be lightweight, flexible and easy to deploy.

ipv4.cat was previously cobbled together using a few different parts including some shell scripts, iptables rules, a custom systemd unit file, and of course, a few lines of Python.  You can read more about it at my original post [here](https://www.linkedin.com/pulse/introducing-ipv4cat-worlds-fastest-way-ascertain-ip-from-humberdross/).

However, I thought it'd be a fun vibe code exercise to improve some of its functionality, Dockerise it, release it and make it easily deployable by anyone who'd like to run it themselves.

## Installation (server)

To build the image and run the container, run:

```
git clone https://github.com/lukejjh/ipv4-cat.git
cd ipv4-cat
docker compose up -d
```

ipv4-cat will attempt to listen on all available ports on the host. Chances are, you'll have some processes already listening on ports. If you're interested in covering those with ipv4-cat, logs will warn you of ports it was unable to bind to. Just run:

```
$ docker logs ipv4-cat

2025-05-06 04:22:09 +1000 - INFO - Starting ipv4-cat service...
2025-05-06 04:22:17 +1000 - WARNING - Failed to bind to the following ports: [22, 53]
```

You can also identify and kill off listening ports with `ss -tlpn` and `systemctl disable --now <service>`, but just make sure they're nothing you need! If you need to, you can use iptables to selectively redirect ports for services such as SSH based on source IP.

## Monitoring

If you're feeling a bit nosy and would like to watch new connections as they come in, you can update `docker-compose.yml` with `LOG_LEVEL=DEBUG`, then:

```
$ docker compose down && docker compose up -d
$ docker logs ipv4-cat -f

2025-05-06 04:22:09 +1000 - INFO - Starting ipv4-cat service...
2025-05-06 04:22:17 +1000 - DEBUG - New connection: 1.2.3.4:29256 => 45.32.245.199:21
2025-05-06 04:22:18 +1000 - DEBUG - New connection: 1.2.3.4:29257 => 45.32.245.199:80
2025-05-06 04:22:18 +1000 - DEBUG - New connection: 1.2.3.4:29258 => 45.32.245.199:443
2025-05-06 04:22:18 +1000 - DEBUG - New connection: 1.2.3.4:29259 => 45.32.245.199:445
```

## Usage examples (clients)

```
$ ftp ipv4.cat
Connected to ipv4.cat.
1.2.3.4
Connection closed by remote host.
```
```
$ nc ipv4.cat 80
1.2.3.4
```

Substitute _ipv4.cat_ with your own domain or IP.