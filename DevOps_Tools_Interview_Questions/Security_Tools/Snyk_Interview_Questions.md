# Snyk Interview Questions & Answers

## 🔒 **Snyk Fundamentals**

### 1. What is Snyk and what does it do?

**Answer:**
Snyk is a developer security platform for finding and fixing vulnerabilities.

**Key Features:**
- **Vulnerability Scanning**: Find security vulnerabilities
- **License Compliance**: Check license issues
- **Container Scanning**: Scan container images
- **Infrastructure as Code**: Scan IaC files
- **CI/CD Integration**: Integrate with pipelines

**Supported Targets:**
- Code repositories
- Container images
- Kubernetes workloads
- Infrastructure as Code
- Open source dependencies

---

### 2. How do you install and use Snyk?

**Answer:**
**Installation:**
```bash
# Using npm
npm install -g snyk

# Using Homebrew
brew tap snyk/tap
brew install snyk
```

**Authentication:**
```bash
snyk auth
```

**Scanning:**
```bash
# Scan project
snyk test

# Scan container image
snyk container test nginx:latest

# Scan Kubernetes
snyk iac test k8s.yaml
```

---

### 3. How do you integrate Snyk in CI/CD?

**Answer:**
**GitHub Actions:**
```yaml
- name: Run Snyk to check for vulnerabilities
  uses: snyk/actions/node@master
  env:
    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

**Jenkins:**
```groovy
stage('Security Scan') {
    steps {
        sh 'snyk test'
    }
}
```

---

## 📝 **Best Practices**

1. **Regular Scanning**: Scan in CI/CD
2. **Fix Vulnerabilities**: Update dependencies
3. **License Compliance**: Check licenses
4. **Integration**: Integrate with workflows
5. **Monitoring**: Monitor for new vulnerabilities

---

**Good luck with your Snyk interview preparation! 🔒**
