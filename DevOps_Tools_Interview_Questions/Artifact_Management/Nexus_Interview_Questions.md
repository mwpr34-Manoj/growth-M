# Nexus Repository Interview Questions & Answers

## 📦 **Nexus Fundamentals**

### 1. What is Nexus Repository and what are its features?

**Answer:**
Nexus Repository is a repository manager for artifacts and dependencies.

**Key Features:**
- **Multiple Formats**: Maven, npm, Docker, PyPI, etc.
- **Proxy Repositories**: Cache remote repositories
- **Hosted Repositories**: Store your artifacts
- **Group Repositories**: Aggregate multiple repositories
- **Security**: Access control and security scanning
- **High Availability**: HA support

**Repository Types:**
- **Proxy**: Proxy remote repositories
- **Hosted**: Store your artifacts
- **Group**: Aggregate repositories

---

### 2. How do you install and configure Nexus?

**Answer:**
**Installation:**
```bash
# Download
wget https://download.sonatype.com/nexus/3/latest-unix.tar.gz
tar -xzf latest-unix.tar.gz
cd nexus-3.x.x/bin
./nexus start
```

**Access:**
- Default URL: `http://localhost:8081`
- Default admin password: Check `sonatype-work/nexus3/admin.password`

**Configuration:**
- Configuration files: `nexus-3.x.x/etc/nexus.properties`
- Data directory: `sonatype-work/nexus3/`

---

### 3. How do you create and manage repositories in Nexus?

**Answer:**
**Creating Repository:**
1. Administration → Repositories → Create repository
2. Choose format (Maven, npm, Docker, etc.)
3. Choose type (Proxy, Hosted, Group)
4. Configure settings
5. Save

**Maven Repository Example:**
- **Proxy**: `maven-central` (proxy to Maven Central)
- **Hosted**: `maven-releases`, `maven-snapshots`
- **Group**: `maven-public` (group of above)

**Docker Repository:**
- **Hosted**: `docker-hosted` (store Docker images)
- **Proxy**: `docker-proxy` (proxy Docker Hub)
- **Group**: `docker-group` (aggregate)

---

### 4. How do you configure Maven to use Nexus?

**Answer:**
**settings.xml:**
```xml
<settings>
  <servers>
    <server>
      <id>nexus</id>
      <username>admin</username>
      <password>password</password>
    </server>
  </servers>
  
  <mirrors>
    <mirror>
      <id>nexus</id>
      <mirrorOf>*</mirrorOf>
      <url>http://nexus:8081/repository/maven-public/</url>
    </mirror>
  </mirrors>
</settings>
```

**Deploy to Nexus:**
```xml
<!-- pom.xml -->
<distributionManagement>
  <repository>
    <id>nexus</id>
    <url>http://nexus:8081/repository/maven-releases/</url>
  </repository>
  <snapshotRepository>
    <id>nexus</id>
    <url>http://nexus:8081/repository/maven-snapshots/</url>
  </snapshotRepository>
</distributionManagement>
```

---

### 5. How do you configure Docker to use Nexus?

**Answer:**
**Docker Configuration:**
```bash
# Login to Nexus
docker login nexus:8083 -u admin -p password

# Tag image
docker tag myapp:latest nexus:8083/docker-hosted/myapp:latest

# Push image
docker push nexus:8083/docker-hosted/myapp:latest

# Pull image
docker pull nexus:8083/docker-hosted/myapp:latest
```

**Docker daemon.json:**
```json
{
  "insecure-registries": ["nexus:8083"]
}
```

---

### 6. How do you manage security in Nexus?

**Answer:**
**User Management:**
- Create users
- Assign roles
- Set permissions

**Roles:**
- **nx-admin**: Full access
- **nx-repository-admin**: Repository management
- **nx-repository-view**: View repositories

**Realms:**
- **Local Authentication**: Built-in users
- **LDAP**: LDAP integration
- **SAML**: SAML SSO

---

## 📝 **Best Practices**

1. **Repository Organization**: Use proper repository structure
2. **Security**: Enable authentication
3. **Backup**: Regular backups
4. **Cleanup Policies**: Remove old artifacts
5. **Monitoring**: Monitor repository usage
6. **High Availability**: Use HA setup
7. **SSL/TLS**: Use HTTPS
8. **Access Control**: Proper permissions

---

**Good luck with your Nexus interview preparation! 📦**
