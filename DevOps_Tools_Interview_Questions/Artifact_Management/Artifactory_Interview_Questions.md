# JFrog Artifactory Interview Questions & Answers

## 📦 **Artifactory Fundamentals**

### 1. What is JFrog Artifactory and what are its features?

**Answer:**
Artifactory is a universal repository manager supporting all major package formats.

**Key Features:**
- **Universal Support**: Maven, npm, Docker, PyPI, NuGet, etc.
- **Advanced Search**: Powerful artifact search
- **Build Integration**: CI/CD integration
- **Security Scanning**: Xray integration
- **High Availability**: HA support
- **Replication**: Multi-site replication

**Repository Types:**
- **Local**: Store your artifacts
- **Remote**: Proxy remote repositories
- **Virtual**: Aggregate repositories

---

### 2. How do you install and configure Artifactory?

**Answer:**
**Installation:**
```bash
# Download
wget https://releases.jfrog.io/artifactory/bintray/jfrog-artifactory-oss/[VERSION]/jfrog-artifactory-oss-[VERSION].zip
unzip jfrog-artifactory-oss-[VERSION].zip
cd artifactory-oss-[VERSION]/bin
./artifactory.sh start
```

**Access:**
- Default URL: `http://localhost:8081/artifactory`
- Default credentials: admin/password

---

### 3. How do you create repositories in Artifactory?

**Answer:**
**Creating Repository:**
1. Administration → Repositories → New
2. Choose package type
3. Choose repository type (Local/Remote/Virtual)
4. Configure settings
5. Save

**Maven Example:**
- **Local**: `libs-release-local`, `libs-snapshot-local`
- **Remote**: `remote-repos` (proxy Maven Central)
- **Virtual**: `libs-release` (aggregate)

---

### 4. How do you integrate Artifactory with Jenkins?

**Answer:**
**Jenkins Integration:**
```groovy
stage('Deploy to Artifactory') {
    steps {
        rtUpload (
            serverId: 'artifactory',
            spec: """{
                "files": [{
                    "pattern": "target/*.jar",
                    "target": "libs-snapshot-local"
                }]
            }"""
        )
    }
}
```

---

## 📝 **Best Practices**

1. **Repository Structure**: Organize repositories properly
2. **Security**: Enable authentication
3. **Cleanup**: Remove old artifacts
4. **Replication**: Set up replication
5. **Backup**: Regular backups

---

**Good luck with your Artifactory interview preparation! 📦**
