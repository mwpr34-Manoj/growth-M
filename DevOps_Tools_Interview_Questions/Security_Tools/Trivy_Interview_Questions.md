# Trivy Interview Questions & Answers

## 🔍 **Trivy Fundamentals**

### 1. What is Trivy and what does it do?

**Answer:**
Trivy is a comprehensive security scanner for containers, filesystems, and Git repositories.

**Key Features:**
- **Vulnerability Scanning**: Find security vulnerabilities
- **Container Scanning**: Scan container images
- **Filesystem Scanning**: Scan local filesystems
- **Git Repository Scanning**: Scan Git repos
- **SBOM Generation**: Software Bill of Materials
- **License Scanning**: Detect licenses

**Supported Targets:**
- Container images
- Filesystems
- Git repositories
- Kubernetes clusters

---

### 2. How do you install and use Trivy?

**Answer:**
**Installation:**
```bash
# Using package manager
sudo apt-get install wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy
```

**Basic Usage:**
```bash
# Scan container image
trivy image nginx:latest

# Scan filesystem
trivy fs /path/to/directory

# Scan Git repository
trivy repo https://github.com/user/repo

# Scan with severity filter
trivy image --severity HIGH,CRITICAL nginx:latest
```

---

### 3. How do you integrate Trivy in CI/CD pipelines?

**Answer:**
**GitHub Actions:**
```yaml
- name: Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: 'myapp:latest'
    format: 'sarif'
    output: 'trivy-results.sarif'
```

**Jenkins:**
```groovy
stage('Security Scan') {
    steps {
        sh 'trivy image myapp:latest'
    }
}
```

---

### 4. How do you use Trivy for Kubernetes scanning?

**Answer:**
```bash
# Scan Kubernetes cluster
trivy k8s cluster

# Scan specific namespace
trivy k8s cluster --namespace production

# Scan with report
trivy k8s cluster --format json --output report.json
```

---

## 📝 **Best Practices**

1. **Regular Scanning**: Scan in CI/CD pipelines
2. **Severity Filtering**: Focus on HIGH/CRITICAL
3. **Fix Vulnerabilities**: Update dependencies
4. **SBOM Generation**: Generate SBOMs
5. **Integration**: Integrate with CI/CD

---

**Good luck with your Trivy interview preparation! 🔍**
