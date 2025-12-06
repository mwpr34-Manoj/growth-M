# Fluentd Interview Questions & Answers

## 📊 **Fluentd Fundamentals**

### 1. What is Fluentd and what does it do?

**Answer:**
Fluentd is an open-source data collector for unified logging.

**Key Features:**
- **Unified Logging**: Collect logs from various sources
- **Flexible Routing**: Route logs to multiple destinations
- **Plugin Architecture**: 500+ plugins
- **Reliable**: Buffering and retry mechanisms
- **Lightweight**: Low resource usage

**Use Cases:**
- Log aggregation
- Log forwarding
- Data pipeline
- Analytics

---

### 2. How do you install and configure Fluentd?

**Answer:**
**Installation:**
```bash
# Using gem
gem install fluentd

# Using package manager
curl -L https://toolbelt.treasuredata.com/sh/install-ubuntu-focal-td-agent4.sh | sh
```

**Configuration:**
```xml
# fluent.conf
<source>
  @type tail
  path /var/log/app.log
  pos_file /var/log/fluentd-app.log.pos
  tag app.log
  format json
</source>

<match app.**>
  @type elasticsearch
  host elasticsearch
  port 9200
  index_name fluentd
  type_name _doc
</match>
```

**Running:**
```bash
fluentd -c fluent.conf
```

---

### 3. How do you use Fluentd with Kubernetes?

**Answer:**
**DaemonSet Configuration:**
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
spec:
  template:
    spec:
      containers:
      - name: fluentd
        image: fluent/fluentd-kubernetes-daemonset:v1-debian-elasticsearch
        env:
        - name: FLUENT_ELASTICSEARCH_HOST
          value: "elasticsearch.logging"
```

---

## 📝 **Best Practices**

1. **Buffering**: Use buffering for reliability
2. **Parsing**: Proper log parsing
3. **Filtering**: Filter unnecessary logs
4. **Performance**: Optimize configuration
5. **Monitoring**: Monitor Fluentd itself

---

**Good luck with your Fluentd interview preparation! 📊**
