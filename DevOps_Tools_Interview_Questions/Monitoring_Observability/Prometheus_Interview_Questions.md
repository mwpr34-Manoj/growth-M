# Prometheus Interview Questions & Answers

## 🚀 **Prometheus Fundamentals**

### 1. What is Prometheus and what are its key features?

**Answer:**
Prometheus is an open-source monitoring and alerting toolkit designed for reliability and scalability. It was originally built at SoundCloud and is now a CNCF project.

**Key Features:**
- **Time-series database**: Stores metrics as time-series data
- **Pull-based model**: Scrapes metrics from targets
- **Multi-dimensional data model**: Metrics identified by name and key-value pairs
- **PromQL**: Powerful query language for selecting and aggregating time-series data
- **Service discovery**: Automatically discovers targets
- **Alerting**: Integrated alerting with Alertmanager
- **Visualization**: Works with Grafana and other tools

**Architecture:**
- **Prometheus Server**: Scrapes and stores time-series data
- **Exporters**: Expose metrics from various systems
- **Pushgateway**: For short-lived jobs
- **Alertmanager**: Handles alerts
- **Client Libraries**: For instrumenting applications

---

### 2. How do you install and configure Prometheus?

**Answer:**
**Installation:**

**Linux:**
```bash
# Download
wget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz
tar xvfz prometheus-2.45.0.linux-amd64.tar.gz
cd prometheus-2.45.0.linux-amd64

# Run
./prometheus --config.file=prometheus.yml
```

**Docker:**
```bash
docker run -d \
  -p 9090:9090 \
  -v /path/to/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus
```

**Configuration (prometheus.yml):**
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['localhost:9100']
```

---

### 3. What is the Prometheus data model?

**Answer:**
Prometheus stores all data as time-series, identified by a metric name and key-value pairs (labels).

**Metric Format:**
```
<metric_name>{<label_name>=<label_value>, ...} <value> [<timestamp>]
```

**Example:**
```
http_requests_total{method="GET", status="200", endpoint="/api"} 100 1609459200000
http_requests_total{method="POST", status="500", endpoint="/api"} 5 1609459200000
```

**Metric Types:**
1. **Counter**: Monotonically increasing value (requests_total)
2. **Gauge**: Value that can go up or down (memory_usage)
3. **Histogram**: Samples observations and counts them in buckets (request_duration_seconds)
4. **Summary**: Similar to histogram, calculates quantiles (request_duration_seconds)

---

### 4. What is PromQL and how do you write queries?

**Answer:**
PromQL (Prometheus Query Language) is used to select and aggregate time-series data.

**Basic Queries:**
```promql
# Select metric
http_requests_total

# Filter by label
http_requests_total{method="GET"}

# Multiple label filters
http_requests_total{method="GET", status="200"}

# Range vector (last 5 minutes)
http_requests_total[5m]

# Rate (per second rate)
rate(http_requests_total[5m])

# Increase (total increase over time)
increase(http_requests_total[1h])
```

**Aggregation:**
```promql
# Sum
sum(http_requests_total)

# Average
avg(cpu_usage)

# Count
count(http_requests_total)

# Group by
sum(http_requests_total) by (method)

# Top 5
topk(5, http_requests_total)
```

**Functions:**
```promql
# Rate
rate(http_requests_total[5m])

# Increase
increase(http_requests_total[1h])

# Histogram quantile
histogram_quantile(0.95, http_request_duration_seconds_bucket)

# Time functions
time()
timestamp(http_requests_total)
```

---

### 5. How do you instrument applications with Prometheus?

**Answer:**
Use client libraries to expose metrics from applications.

**Python Example:**
```python
from prometheus_client import Counter, Histogram, start_http_server
import time

# Define metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')

# Instrument code
@REQUEST_DURATION.time()
def handle_request(method, endpoint):
    REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()
    # ... handle request

# Expose metrics
start_http_server(8000)
```

**Node.js Example:**
```javascript
const prometheus = require('prom-client');

// Create metrics
const httpRequestDuration = new prometheus.Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration',
  labelNames: ['method', 'route']
});

// Instrument
app.use((req, res, next) => {
  const end = httpRequestDuration.startTimer({ method: req.method, route: req.route });
  res.on('finish', () => end());
  next();
});
```

---

### 6. What are Prometheus exporters and how do you use them?

**Answer:**
Exporters expose metrics from systems that don't natively support Prometheus.

**Common Exporters:**
- **node_exporter**: System metrics (CPU, memory, disk)
- **blackbox_exporter**: Probes endpoints (HTTP, TCP, ICMP)
- **mysqld_exporter**: MySQL metrics
- **postgres_exporter**: PostgreSQL metrics
- **nginx_exporter**: Nginx metrics

**Using node_exporter:**
```bash
# Download and run
wget https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz
tar xvfz node_exporter-1.6.1.linux-amd64.tar.gz
./node_exporter
```

**Configure Prometheus:**
```yaml
scrape_configs:
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['localhost:9100']
```

---

### 7. How do you set up alerting with Prometheus?

**Answer:**
Prometheus uses Alertmanager for alerting.

**Alert Rules (alerts.yml):**
```yaml
groups:
  - name: example
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status="500"}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} errors per second"

      - alert: InstanceDown
        expr: up == 0
        for: 1m
        labels:
          severity: warning
        annotations:
          summary: "Instance {{ $labels.instance }} is down"
```

**Prometheus Configuration:**
```yaml
rule_files:
  - "alerts.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093
```

**Alertmanager Configuration:**
```yaml
route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h
  receiver: 'web.hook'
receivers:
  - name: 'web.hook'
    webhook_configs:
      - url: 'http://127.0.0.1:5001/'
```

---

### 8. How do you use service discovery in Prometheus?

**Answer:**
Service discovery automatically discovers targets.

**Static Configuration:**
```yaml
scrape_configs:
  - job_name: 'static'
    static_configs:
      - targets: ['host1:9100', 'host2:9100']
```

**File-based Discovery:**
```yaml
scrape_configs:
  - job_name: 'file-sd'
    file_sd_configs:
      - files:
          - 'targets.json'
```

**targets.json:**
```json
[
  {
    "targets": ["host1:9100"],
    "labels": {
      "env": "production",
      "job": "node-exporter"
    }
  }
]
```

**Kubernetes Service Discovery:**
```yaml
scrape_configs:
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
```

---

### 9. How do you use Pushgateway in Prometheus?

**Answer:**
Pushgateway is used for short-lived jobs that can't be scraped.

**Using Pushgateway:**
```bash
# Start Pushgateway
docker run -d -p 9091:9091 prom/pushgateway

# Push metrics
echo "some_metric 3.14" | curl --data-binary @- http://pushgateway:9091/metrics/job/my_job/instance/my_instance
```

**From Application:**
```python
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

registry = CollectorRegistry()
g = Gauge('job_last_success_unixtime', 'Last time job succeeded', registry=registry)
g.set_to_current_time()
push_to_gateway('pushgateway:9091', job='batch_job', registry=registry)
```

**Prometheus Configuration:**
```yaml
scrape_configs:
  - job_name: 'pushgateway'
    honor_labels: true
    static_configs:
      - targets: ['pushgateway:9091']
```

---

### 10. How do you optimize Prometheus performance?

**Answer:**
**Optimization Strategies:**

1. **Retention Configuration:**
```yaml
# prometheus.yml
global:
  storage.tsdb.retention.time: 15d
  storage.tsdb.retention.size: 10GB
```

2. **Scrape Interval:**
```yaml
global:
  scrape_interval: 15s  # Adjust based on needs
```

3. **Cardinality Management:**
- Limit label cardinality
- Use recording rules for expensive queries
- Remove unnecessary labels

4. **Recording Rules:**
```yaml
# recording_rules.yml
groups:
  - name: example
    interval: 30s
    rules:
      - record: job:http_requests:rate5m
        expr: rate(http_requests_total[5m])
```

5. **Remote Write:**
```yaml
remote_write:
  - url: http://remote-storage:9090/api/v1/write
```

---

## 📝 **Best Practices**

1. **Naming conventions**: Use consistent metric names
2. **Label cardinality**: Keep label values limited
3. **Recording rules**: Pre-compute expensive queries
4. **Alerting**: Set up meaningful alerts
5. **Monitoring**: Monitor Prometheus itself
6. **Retention**: Configure appropriate retention
7. **High availability**: Run multiple Prometheus instances
8. **Documentation**: Document metrics and alerts
9. **Testing**: Test alert rules
10. **Backup**: Backup Prometheus data

---

**Good luck with your Prometheus interview preparation!**
