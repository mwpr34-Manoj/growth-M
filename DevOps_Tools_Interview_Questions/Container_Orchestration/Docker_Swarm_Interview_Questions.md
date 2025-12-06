# Docker Swarm Interview Questions & Answers

## 🐳 **Docker Swarm Fundamentals**

### 1. What is Docker Swarm and how does it differ from Kubernetes?

**Answer:**
Docker Swarm is Docker's native clustering and orchestration solution.

**Key Differences:**

| Feature | Docker Swarm | Kubernetes |
|---------|--------------|------------|
| **Complexity** | Simpler | More complex |
| **Learning Curve** | Easier | Steeper |
| **Features** | Basic orchestration | Advanced features |
| **Scaling** | Good | Excellent |
| **Networking** | Simpler | More advanced |

**When to Use:**
- **Swarm**: Simpler deployments, Docker-native
- **Kubernetes**: Complex requirements, advanced features

---

### 2. How do you initialize a Docker Swarm?

**Answer:**
**Initialize Swarm:**
```bash
# Initialize swarm
docker swarm init

# Get join token for workers
docker swarm join-token worker

# Get join token for managers
docker swarm join-token manager
```

**Join Nodes:**
```bash
# On worker node
docker swarm join --token <token> <manager-ip>:2377
```

---

### 3. How do you deploy services in Docker Swarm?

**Answer:**
**Create Service:**
```bash
# Create service
docker service create --name web --replicas 3 -p 80:80 nginx

# Scale service
docker service scale web=5

# Update service
docker service update --image nginx:alpine web

# List services
docker service ls

# Inspect service
docker service inspect web
```

**Service Definition:**
```yaml
version: '3.8'
services:
  web:
    image: nginx
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
    ports:
      - "80:80"
```

---

### 4. How do you manage Docker Swarm?

**Answer:**
**Swarm Management:**
```bash
# List nodes
docker node ls

# Inspect node
docker node inspect <node-id>

# Remove node
docker node rm <node-id>

# Update node
docker node update --availability drain <node-id>
```

**Service Management:**
```bash
# Service logs
docker service logs web

# Service ps
docker service ps web

# Rollback service
docker service rollback web
```

---

## 📝 **Best Practices**

1. **High Availability**: Use multiple managers
2. **Health Checks**: Configure health checks
3. **Secrets**: Use Docker secrets
4. **Networking**: Use overlay networks
5. **Monitoring**: Monitor swarm cluster

---

**Good luck with your Docker Swarm interview preparation! 🐳**
