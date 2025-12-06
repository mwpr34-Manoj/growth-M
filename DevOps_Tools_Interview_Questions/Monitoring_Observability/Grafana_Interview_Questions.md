# Grafana Interview Questions & Answers

## 🎨 **Grafana Fundamentals**

### 1. What is Grafana and what are its key features?

**Answer:**
Grafana is an open-source analytics and visualization platform that allows you to query, visualize, alert on, and understand metrics from various data sources.

**Key Features:**
- **Data Source Integration**: Supports 50+ data sources (Prometheus, InfluxDB, Elasticsearch, etc.)
- **Visualization**: Rich visualization options (graphs, tables, heatmaps, etc.)
- **Dashboards**: Create and share dashboards
- **Alerting**: Set up alerts based on metrics
- **Templating**: Dynamic dashboards with variables
- **Annotations**: Mark events on graphs
- **User Management**: Role-based access control

**Use Cases:**
- Infrastructure monitoring
- Application performance monitoring
- Business metrics visualization
- Time-series data analysis

---

### 2. How do you install and configure Grafana?

**Answer:**
**Installation:**

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get install -y software-properties-common
sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
sudo apt-get update
sudo apt-get install grafana

# Start Grafana
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```

**Docker:**
```bash
docker run -d -p 3000:3000 grafana/grafana
```

**Configuration:**
- Default URL: `http://localhost:3000`
- Default credentials: admin/admin
- Configuration file: `/etc/grafana/grafana.ini`

---

### 3. How do you add data sources in Grafana?

**Answer:**
**Adding Prometheus:**
1. Go to Configuration → Data Sources
2. Add data source → Prometheus
3. Configure:
   - URL: `http://prometheus:9090`
   - Access: Server (default)
4. Save & Test

**Adding Other Data Sources:**
- **InfluxDB**: Time-series database
- **Elasticsearch**: Log analytics
- **CloudWatch**: AWS metrics
- **Azure Monitor**: Azure metrics
- **MySQL/PostgreSQL**: SQL databases

**Configuration Example:**
```yaml
# grafana.ini
[datasources]
prometheus.url = http://prometheus:9090
```

---

### 4. How do you create dashboards in Grafana?

**Answer:**
**Creating Dashboard:**
1. Go to Dashboards → New Dashboard
2. Add Panel → Choose visualization type
3. Configure query (PromQL, SQL, etc.)
4. Customize visualization
5. Save dashboard

**Panel Types:**
- **Graph**: Time-series graphs
- **Stat**: Single stat visualization
- **Table**: Tabular data
- **Heatmap**: Heatmap visualization
- **Gauge**: Gauge visualization
- **Bar Gauge**: Bar gauge
- **Pie Chart**: Pie chart

**Query Example (Prometheus):**
```promql
rate(http_requests_total[5m])
```

---

### 5. How do you use variables in Grafana dashboards?

**Answer:**
**Creating Variables:**
1. Dashboard Settings → Variables
2. Add variable
3. Configure:
   - Name: `instance`
   - Type: Query
   - Query: `label_values(up, instance)`

**Using Variables:**
```promql
# In query
http_requests_total{instance="$instance"}

# In panel title
Requests for $instance
```

**Variable Types:**
- **Query**: From data source query
- **Custom**: Manual list
- **Text**: Text input
- **Constant**: Fixed value
- **Interval**: Time interval

---

### 6. How do you set up alerting in Grafana?

**Answer:**
**Creating Alert:**
1. Edit panel → Alert tab
2. Create alert rule
3. Configure:
   - Condition: `WHEN avg() OF query(A, 5m, now) IS BELOW 100`
   - Evaluate every: 1m
   - For: 5m
4. Add notification channels

**Alert Rules:**
```yaml
# Alert configuration
- alert: HighErrorRate
  expr: rate(http_requests_total{status="500"}[5m]) > 0.05
  for: 5m
  annotations:
    summary: "High error rate"
```

**Notification Channels:**
- Email
- Slack
- PagerDuty
- Webhook
- Teams

---

### 7. How do you organize dashboards in Grafana?

**Answer:**
**Dashboard Organization:**
- **Folders**: Organize dashboards
- **Tags**: Tag dashboards for filtering
- **Favorites**: Mark as favorite
- **Playlists**: Auto-rotate dashboards

**Best Practices:**
- Use folders for teams/environments
- Tag dashboards appropriately
- Use consistent naming
- Share dashboards with teams

---

### 8. How do you use Grafana with Prometheus?

**Answer:**
**Integration:**
1. Add Prometheus as data source
2. Use PromQL in queries
3. Create dashboards with Prometheus metrics

**Example Queries:**
```promql
# CPU usage
100 - (avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory usage
(node_memory_MemTotal_bytes - node_memory_MemFree_bytes) / node_memory_MemTotal_bytes * 100

# Request rate
rate(http_requests_total[5m])
```

---

### 9. How do you implement user management and security in Grafana?

**Answer:**
**User Management:**
- **Users**: Individual user accounts
- **Organizations**: Multi-tenant support
- **Teams**: Group users
- **Roles**: Admin, Editor, Viewer

**Authentication:**
- **LDAP**: LDAP integration
- **OAuth**: Google, GitHub, etc.
- **SAML**: SAML SSO
- **Auth Proxy**: Reverse proxy auth

**Permissions:**
- **Admin**: Full access
- **Editor**: Create/edit dashboards
- **Viewer**: View only

---

### 10. How do you optimize Grafana performance?

**Answer:**
**Optimization Strategies:**
1. **Query Optimization**: Optimize data source queries
2. **Refresh Intervals**: Set appropriate refresh rates
3. **Time Ranges**: Limit time ranges
4. **Panel Limits**: Limit panels per dashboard
5. **Caching**: Enable query caching
6. **Database**: Use appropriate database backend

---

## 📝 **Best Practices**

1. **Organize dashboards**: Use folders and tags
2. **Optimize queries**: Efficient data source queries
3. **Use variables**: Dynamic dashboards
4. **Set up alerts**: Proactive monitoring
5. **Documentation**: Document dashboards
6. **Version control**: Export dashboards as JSON
7. **Permissions**: Use proper access control
8. **Performance**: Optimize for speed
9. **Templates**: Use dashboard templates
10. **Backup**: Regular dashboard backups

---

**Good luck with your Grafana interview preparation!**
