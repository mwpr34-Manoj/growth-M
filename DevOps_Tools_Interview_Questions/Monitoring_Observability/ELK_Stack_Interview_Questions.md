# ELK Stack Interview Questions & Answers

## 📊 **ELK Stack Fundamentals**

### 1. What is the ELK Stack and what are its components?

**Answer:**
ELK Stack is a collection of three open-source tools for log management and analysis:
- **Elasticsearch**: Search and analytics engine
- **Logstash**: Data processing pipeline
- **Kibana**: Visualization and dashboarding

**Modern Stack (Elastic Stack):**
- **Elasticsearch**: NoSQL database and search engine
- **Logstash/Beats**: Data collection
- **Kibana**: Visualization
- **Beats**: Lightweight data shippers

**Key Features:**
- Centralized logging
- Real-time search and analysis
- Scalable architecture
- Rich visualizations
- Full-text search

---

### 2. What is Elasticsearch and how does it work?

**Answer:**
Elasticsearch is a distributed, RESTful search and analytics engine built on Apache Lucene.

**Key Concepts:**
- **Index**: Collection of documents (like database)
- **Document**: JSON object (like row)
- **Type**: Category of document (deprecated in 7.x)
- **Shard**: Horizontal partition of data
- **Replica**: Copy of shard for redundancy

**Architecture:**
- **Cluster**: Collection of nodes
- **Node**: Single server instance
- **Master Node**: Manages cluster
- **Data Node**: Stores data
- **Ingest Node**: Processes data

**Installation:**
```bash
# Download and install
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.10.0-linux-x86_64.tar.gz
tar -xzf elasticsearch-8.10.0-linux-x86_64.tar.gz
cd elasticsearch-8.10.0
./bin/elasticsearch
```

---

### 3. What is Logstash and how do you configure it?

**Answer:**
Logstash is a data processing pipeline that ingests, transforms, and outputs data.

**Pipeline Structure:**
- **Input**: Data ingestion
- **Filter**: Data transformation
- **Output**: Data destination

**Configuration Example:**
```ruby
# logstash.conf
input {
  file {
    path => "/var/log/app.log"
    start_position => "beginning"
  }
}

filter {
  grok {
    match => { "message" => "%{COMBINEDAPACHELOG}" }
  }
  date {
    match => [ "timestamp", "dd/MMM/yyyy:HH:mm:ss Z" ]
  }
}

output {
  elasticsearch {
    hosts => ["http://localhost:9200"]
    index => "logs-%{+YYYY.MM.dd}"
  }
}
```

**Running Logstash:**
```bash
bin/logstash -f logstash.conf
```

---

### 4. What is Kibana and how do you use it?

**Answer:**
Kibana is a visualization and dashboarding tool for Elasticsearch.

**Key Features:**
- **Discover**: Explore data
- **Visualize**: Create visualizations
- **Dashboard**: Combine visualizations
- **Dev Tools**: Query Elasticsearch
- **Management**: Index management

**Installation:**
```bash
# Download and install
wget https://artifacts.elastic.co/downloads/kibana/kibana-8.10.0-linux-x86_64.tar.gz
tar -xzf kibana-8.10.0-linux-x86_64.tar.gz
cd kibana-8.10.0
./bin/kibana
```

**Access:**
- Default URL: `http://localhost:5601`

---

### 5. What are Beats and what types are available?

**Answer:**
Beats are lightweight data shippers that send data to Elasticsearch or Logstash.

**Types of Beats:**
- **Filebeat**: Log files
- **Metricbeat**: System and service metrics
- **Packetbeat**: Network packet analysis
- **Heartbeat**: Uptime monitoring
- **Auditbeat**: Audit data
- **Winlogbeat**: Windows event logs

**Filebeat Example:**
```yaml
# filebeat.yml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /var/log/*.log

output.elasticsearch:
  hosts: ["localhost:9200"]
```

---

### 6. How do you query data in Elasticsearch?

**Answer:**
**REST API Queries:**
```bash
# Search all documents
curl -X GET "localhost:9200/_search?pretty"

# Search specific index
curl -X GET "localhost:9200/logs-*/_search?pretty"

# Query DSL
curl -X GET "localhost:9200/logs/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "message": "error"
    }
  }
}'
```

**Query Types:**
- **Match**: Full-text search
- **Term**: Exact match
- **Range**: Range queries
- **Bool**: Boolean combinations
- **Aggregations**: Data analysis

---

### 7. How do you create visualizations in Kibana?

**Answer:**
**Creating Visualization:**
1. Go to Visualize → Create visualization
2. Choose visualization type
3. Select index pattern
4. Configure metrics and buckets
5. Save visualization

**Visualization Types:**
- **Area Chart**: Area visualization
- **Data Table**: Tabular data
- **Line Chart**: Line graph
- **Pie Chart**: Pie chart
- **Vertical Bar Chart**: Bar chart
- **Heat Map**: Heatmap
- **Metric**: Single metric

---

### 8. How do you set up log parsing with Logstash?

**Answer:**
**Grok Patterns:**
```ruby
filter {
  grok {
    match => { "message" => "%{IP:client} %{WORD:method} %{URIPATHPARAM:request}" }
  }
}
```

**Common Patterns:**
- `%{IP:ip}`: IP address
- `%{WORD:word}`: Word
- `%{NUMBER:num}`: Number
- `%{TIMESTAMP_ISO8601:timestamp}`: Timestamp
- `%{COMBINEDAPACHELOG}`: Apache combined log

**Date Parsing:**
```ruby
filter {
  date {
    match => [ "timestamp", "dd/MMM/yyyy:HH:mm:ss Z" ]
  }
}
```

---

### 9. How do you optimize Elasticsearch performance?

**Answer:**
**Optimization Strategies:**
1. **Index Templates**: Standardize index structure
2. **Shard Management**: Appropriate shard count
3. **Refresh Interval**: Adjust refresh rate
4. **Bulk Operations**: Use bulk API
5. **Mapping**: Optimize field mappings
6. **Index Lifecycle**: Use ILM policies

**Index Lifecycle Management:**
```json
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": {
            "max_size": "50GB"
          }
        }
      },
      "delete": {
        "min_age": "30d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

---

### 10. How do you secure the ELK Stack?

**Answer:**
**Security Features:**
- **X-Pack Security**: Authentication and authorization
- **TLS/SSL**: Encrypt communications
- **Role-Based Access**: Control user permissions
- **Audit Logging**: Track access

**Configuration:**
```yaml
# elasticsearch.yml
xpack.security.enabled: true
xpack.security.transport.ssl.enabled: true
```

---

## 📝 **Best Practices**

1. **Index Management**: Use index templates and ILM
2. **Log Parsing**: Proper grok patterns
3. **Performance**: Optimize queries and shards
4. **Security**: Enable X-Pack security
5. **Monitoring**: Monitor Elasticsearch cluster
6. **Backup**: Regular snapshots
7. **Documentation**: Document log formats
8. **Retention**: Set appropriate retention
9. **Scaling**: Plan for horizontal scaling
10. **Testing**: Test configurations

---

**Good luck with your ELK Stack interview preparation!**
