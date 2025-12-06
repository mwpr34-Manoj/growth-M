# Google Cloud Platform (GCP) Interview Questions & Answers

## ☁️ **GCP Fundamentals**

### 1. What is Google Cloud Platform and what are its main services?

**Answer:**
GCP is Google's cloud computing platform offering 100+ services.

**Main Service Categories:**
- **Compute**: Compute Engine, App Engine, Cloud Functions, GKE
- **Storage**: Cloud Storage, Persistent Disk, Filestore
- **Networking**: VPC, Cloud Load Balancing, Cloud CDN
- **Databases**: Cloud SQL, Cloud Spanner, Bigtable, Firestore
- **Security**: IAM, Cloud KMS, Security Command Center
- **Monitoring**: Cloud Monitoring, Cloud Logging, Trace
- **Management**: Cloud Deployment Manager, Cloud Build

---

### 2. Explain Compute Engine and its machine types.

**Answer:**
Compute Engine provides virtual machines in Google's infrastructure.

**Machine Types:**
- **General Purpose**: e2, n2 (balanced)
- **Compute Optimized**: c2 (high CPU)
- **Memory Optimized**: m2, m1 (high memory)
- **Shared Core**: f1, g1 (low cost)

**Features:**
- Preemptible VMs (discounted)
- Custom machine types
- Sustained use discounts
- Live migration

---

### 3. What is Google Kubernetes Engine (GKE)?

**Answer:**
GKE is a managed Kubernetes service.

**Features:**
- Managed control plane
- Auto-scaling
- Auto-repair
- Auto-upgrade
- Integrated with GCP services

**Cluster Types:**
- **Standard**: Full control
- **Autopilot**: Fully managed

---

### 4. Explain Cloud Storage and its storage classes.

**Answer:**
Cloud Storage is object storage service.

**Storage Classes:**
- **Standard**: Frequently accessed
- **Nearline**: Monthly access
- **Coldline**: Quarterly access
- **Archive**: Yearly access

**Features:**
- Lifecycle policies
- Versioning
- Encryption
- Access control

---

### 5. What is Cloud IAM and how does it work?

**Answer:**
Cloud IAM manages access control for GCP resources.

**Concepts:**
- **Members**: Users, groups, service accounts
- **Roles**: Collections of permissions
- **Policies**: Bindings of members to roles

**Predefined Roles:**
- **Owner**: Full control
- **Editor**: Can modify
- **Viewer**: Read-only

---

### 6. Explain Cloud Functions.

**Answer:**
Cloud Functions is a serverless execution environment.

**Features:**
- Event-driven
- Pay per execution
- Automatic scaling
- Multiple languages

**Triggers:**
- HTTP
- Cloud Storage
- Pub/Sub
- Firestore

---

## 📝 **Best Practices**

1. **Use IAM**: Proper access control
2. **Enable Monitoring**: Use Cloud Monitoring
3. **Use Labels**: Resource organization
4. **Cost Optimization**: Use appropriate resources
5. **Security**: Follow security best practices
6. **Backup**: Regular backups
7. **Networking**: Use VPC properly
8. **Documentation**: Document configurations

---

**Good luck with your GCP interview preparation! ☁️**
