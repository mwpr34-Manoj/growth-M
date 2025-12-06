# Fluent Bit Interview Questions & Answers

## 📊 **Fluent Bit Fundamentals**

### 1. What is Fluent Bit and how does it differ from Fluentd?

**Answer:**
Fluent Bit is a lightweight, high-performance log processor and forwarder.

**Key Differences:**

| Feature | Fluent Bit | Fluentd |
|---------|-----------|---------|
| **Size** | ~450KB | ~40MB |
| **Performance** | Higher | Lower |
| **Memory** | Lower | Higher |
| **Use Case** | Edge/IoT, containers | Centralized logging |

**When to Use:**
- **Fluent Bit**: Containers, edge devices, resource-constrained
- **Fluentd**: Centralized logging, more features

---

### 2. How do you install and configure Fluent Bit?

**Answer:**
**Installation:**
```bash
# Ubuntu/Debian
wget -qO - https://packages.fluentbit.io/fluentbit.key | sudo apt-key add -
echo "deb https://packages.fluentbit.io/ubuntu focal main" | sudo tee /etc/apt/sources.list.d/fluent-bit.list
sudo apt-get update
sudo apt-get install fluent-bit
```

**Configuration:**
```ini
# fluent-bit.conf
[SERVICE]
    Flush        5
    Daemon       Off
    Log_Level    info

[INPUT]
    Name         tail
    Path         /var/log/app.log
    Parser       json

[OUTPUT]
    Name         elasticsearch
    Match        *
    Host         elasticsearch
    Port         9200
    Index        fluent-bit
```

**Running:**
```bash
fluent-bit -c fluent-bit.conf
```

---

### 3. How do you use Fluent Bit with Kubernetes?

**Answer:**
**DaemonSet Configuration:**
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluent-bit
spec:
  template:
    spec:
      containers:
      - name: fluent-bit
        image: fluent/fluent-bit:latest
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
```

---

## 📝 **Best Practices**

1. **Resource Usage**: Optimize for low resource usage
2. **Parsing**: Efficient log parsing
3. **Buffering**: Use buffering for reliability
4. **Filtering**: Filter at source
5. **Performance**: Monitor performance

---

**Good luck with your Fluent Bit interview preparation! 📊**
