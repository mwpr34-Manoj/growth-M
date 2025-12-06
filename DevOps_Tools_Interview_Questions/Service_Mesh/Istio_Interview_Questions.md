# Istio Service Mesh Interview Questions & Answers

## 🌐 **Istio Fundamentals**

### 1. What is Istio and what are its key features?

**Answer:**
Istio is an open-source service mesh that provides traffic management, security, and observability.

**Key Features:**
- **Traffic Management**: Load balancing, routing, circuit breaking
- **Security**: mTLS, authentication, authorization
- **Observability**: Metrics, logs, traces
- **Policy Enforcement**: Rate limiting, quotas

**Components:**
- **Envoy Proxy**: Sidecar proxy
- **Istiod**: Control plane
- **Pilot**: Traffic management
- **Citadel**: Security
- **Galley**: Configuration validation

---

### 2. How do you install Istio?

**Answer:**
**Installation:**
```bash
# Download
curl -L https://istio.io/downloadIstio | sh -
cd istio-1.19.0

# Install
istioctl install --set profile=default

# Verify
istioctl verify-install
```

**Enable Sidecar Injection:**
```bash
# Label namespace
kubectl label namespace default istio-injection=enabled
```

---

### 3. How do you configure traffic management in Istio?

**Answer:**
**VirtualService:**
```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
  - myapp
  http:
  - match:
    - uri:
        prefix: "/api"
    route:
    - destination:
        host: myapp
        subset: v1
      weight: 80
    - destination:
        host: myapp
        subset: v2
      weight: 20
```

**DestinationRule:**
```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: myapp
spec:
  host: myapp
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
```

---

### 4. How do you implement security in Istio?

**Answer:**
**mTLS:**
```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
spec:
  mtls:
    mode: STRICT
```

**Authorization:**
```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-get
spec:
  action: ALLOW
  rules:
  - to:
    - operation:
        methods: ["GET"]
```

---

## 📝 **Best Practices**

1. **Gradual Rollout**: Enable Istio gradually
2. **Monitoring**: Monitor service mesh
3. **Security**: Enable mTLS
4. **Performance**: Optimize proxy configuration
5. **Documentation**: Document policies

---

**Good luck with your Istio interview preparation! 🌐**
