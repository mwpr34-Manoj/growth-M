# Consul Interview Questions & Answers

## 🔧 **Consul Fundamentals**

### 1. What is Consul and what are its features?

**Answer:**
Consul is a service networking solution for service discovery, configuration, and segmentation.

**Key Features:**
- **Service Discovery**: Find services automatically
- **Health Checking**: Monitor service health
- **Key-Value Store**: Configuration storage
- **Multi-Datacenter**: Multi-DC support
- **Service Mesh**: Connect services securely

**Use Cases:**
- Service discovery
- Configuration management
- Service mesh
- Load balancing

---

### 2. How do you install and configure Consul?

**Answer:**
**Installation:**
```bash
# Download
wget https://releases.hashicorp.com/consul/1.17.0/consul_1.17.0_linux_amd64.zip
unzip consul_1.17.0_linux_amd64.zip
sudo mv consul /usr/local/bin/
```

**Start Consul:**
```bash
# Development mode
consul agent -dev

# Server mode
consul agent -server -bootstrap-expect=3 -data-dir=/tmp/consul
```

---

### 3. How do you use Consul for service discovery?

**Answer:**
**Service Registration:**
```json
{
  "ID": "web1",
  "Name": "web",
  "Tags": ["v1"],
  "Address": "10.0.0.1",
  "Port": 80,
  "Check": {
    "HTTP": "http://10.0.0.1:80/health",
    "Interval": "10s"
  }
}
```

**Register Service:**
```bash
consul services register service.json
```

**Query Services:**
```bash
# DNS query
dig @127.0.0.1 -p 8600 web.service.consul

# HTTP API
curl http://localhost:8500/v1/catalog/service/web
```

---

### 4. How do you use Consul KV store?

**Answer:**
**Key-Value Operations:**
```bash
# Put value
consul kv put app/config/database/host db.example.com

# Get value
consul kv get app/config/database/host

# List keys
consul kv get -recurse app/config/

# Delete key
consul kv delete app/config/database/host
```

---

## 📝 **Best Practices**

1. **High Availability**: Run multiple servers
2. **Security**: Enable ACLs
3. **Monitoring**: Monitor Consul cluster
4. **Backup**: Regular backups
5. **Documentation**: Document service definitions

---

**Good luck with your Consul interview preparation! 🔧**
