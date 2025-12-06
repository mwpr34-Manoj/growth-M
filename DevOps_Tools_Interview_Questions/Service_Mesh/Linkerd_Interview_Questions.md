# Linkerd Interview Questions & Answers

## 🌐 **Linkerd Fundamentals**

### 1. What is Linkerd and how does it differ from Istio?

**Answer:**
Linkerd is a lightweight, ultralight service mesh for Kubernetes.

**Key Differences:**

| Feature | Linkerd | Istio |
|---------|---------|-------|
| **Size** | Lightweight | Heavier |
| **Complexity** | Simpler | More complex |
| **Performance** | Lower latency | Higher latency |
| **Learning Curve** | Easier | Steeper |

**When to Use:**
- **Linkerd**: Simpler deployments, lower overhead
- **Istio**: Advanced features, more control

---

### 2. How do you install Linkerd?

**Answer:**
**Installation:**
```bash
# Install CLI
curl --proto '=https' --tlsv1.2 -sSfL https://run.linkerd.io/install | sh

# Install Linkerd
linkerd install | kubectl apply -f -

# Verify
linkerd check
```

**Inject Sidecar:**
```bash
# Manual injection
kubectl get deployment myapp -o yaml | linkerd inject - | kubectl apply -f -

# Automatic injection
kubectl annotate namespace default linkerd.io/inject=enabled
```

---

### 3. How do you use Linkerd for observability?

**Answer:**
**View Metrics:**
```bash
# Install dashboard
linkerd viz install | kubectl apply -f -

# Access dashboard
linkerd viz dashboard
```

**Metrics:**
- Request rate
- Success rate
- Latency
- Traffic split

---

## 📝 **Best Practices**

1. **Gradual Rollout**: Enable gradually
2. **Monitoring**: Use Linkerd dashboard
3. **Security**: Enable mTLS
4. **Performance**: Monitor overhead
5. **Documentation**: Document policies

---

**Good luck with your Linkerd interview preparation! 🌐**
