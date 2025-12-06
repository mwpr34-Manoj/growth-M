# etcd Interview Questions & Answers

## 🔧 **etcd Fundamentals**

### 1. What is etcd and what is it used for?

**Answer:**
etcd is a distributed, reliable key-value store for shared configuration and service discovery.

**Key Features:**
- **Distributed**: Runs across multiple nodes
- **Consistent**: Strong consistency
- **Reliable**: Data persistence
- **Fast**: Low latency

**Use Cases:**
- Kubernetes cluster state
- Service discovery
- Configuration management
- Distributed locking
- Leader election

---

### 2. How do you install and configure etcd?

**Answer:**
**Installation:**
```bash
# Download
wget https://github.com/etcd-io/etcd/releases/download/v3.5.9/etcd-v3.5.9-linux-amd64.tar.gz
tar -xzf etcd-v3.5.9-linux-amd64.tar.gz
cd etcd-v3.5.9-linux-amd64
```

**Start etcd:**
```bash
# Single node
./etcd

# With configuration
./etcd --name node1 \
  --data-dir /var/lib/etcd \
  --listen-client-urls http://0.0.0.0:2379 \
  --advertise-client-urls http://localhost:2379
```

---

### 3. How do you use etcd for key-value operations?

**Answer:**
**Basic Operations:**
```bash
# Set value
etcdctl put mykey "myvalue"

# Get value
etcdctl get mykey

# Delete key
etcdctl del mykey

# List keys
etcdctl get --prefix ""

# Watch key
etcdctl watch mykey
```

**Using API:**
```bash
# Set
curl -X PUT http://localhost:2379/v2/keys/mykey -d value="myvalue"

# Get
curl http://localhost:2379/v2/keys/mykey
```

---

### 4. How is etcd used in Kubernetes?

**Answer:**
etcd is the primary datastore for Kubernetes.

**Role in Kubernetes:**
- Stores cluster state
- Stores configuration
- Stores secrets (encrypted)
- Stores API objects

**Backup:**
```bash
# Backup etcd
ETCDCTL_API=3 etcdctl snapshot save /backup/etcd-snapshot.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key
```

---

## 📝 **Best Practices**

1. **High Availability**: Run multiple nodes
2. **Backup**: Regular backups
3. **Security**: Enable TLS
4. **Monitoring**: Monitor etcd health
5. **Performance**: Optimize configuration

---

**Good luck with your etcd interview preparation! 🔧**
