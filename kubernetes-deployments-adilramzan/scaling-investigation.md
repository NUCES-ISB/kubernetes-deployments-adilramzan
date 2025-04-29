# Kubernetes Scaling Investigation and Testing

This document outlines steps to investigate and test the scaling capabilities of our Flask application deployment in Kubernetes.

## 1. Replica Count Settings

The Flask application deployment has the following scaling settings:

- **Default Replicas**: 3 (set in `flask-deployment.yaml`)
- **Minimum Replicas**: 1 (set via HPA)
- **Maximum Replicas**: 10 (set via HPA)
- **Target CPU Utilization**: 50% (set via HPA)

## 2. Manual Scaling Tests

Manual scaling allows direct control over the number of replicas. This is useful for:

- Pre-scaling before anticipated traffic spikes
- Ensuring minimum availability during maintenance
- Testing deployment behavior with different replica counts

### Steps to Test Manual Scaling:

1. Check current deployment status:

   ```
   kubectl get deployment flask-app
   ```

2. Scale up the deployment:

   ```
   kubectl scale deployment flask-app --replicas=5
   ```

3. Verify scaling up:

   ```
   kubectl get pods -l app=flask-app
   ```

4. Scale down the deployment:

   ```
   kubectl scale deployment flask-app --replicas=2
   ```

5. Verify scaling down:
   ```
   kubectl get pods -l app=flask-app
   ```

## 3. Horizontal Pod Autoscaler (HPA) Tests

The HPA automatically adjusts the number of replicas based on observed CPU utilization.

### Steps to Test Autoscaling:

1. Check current HPA status:

   ```
   kubectl get hpa flask-app-hpa
   ```

2. Generate load on the application:

   ```
   ./load-test.sh
   ```

3. Monitor the HPA during load test:

   ```
   kubectl get hpa flask-app-hpa -w
   ```

4. Check pod resource usage:
   ```
   kubectl top pods
   ```

## 4. Effects of Scaling

- **Increased Availability**: More replicas provide higher availability and fault tolerance
- **Improved Performance**: Load distribution across multiple replicas reduces response times
- **Resource Optimization**: HPA ensures resources are only used when needed
- **Cost Efficiency**: Automatically scaling down during low traffic periods reduces resource usage

## 5. Observing Scaling Effects

The following metrics should be observed before, during, and after scaling:

- Number of running pods
- CPU and memory utilization per pod
- Request latency
- Success rates of API calls

## 6. Important Commands for Investigation

```
# Get detailed info about the deployment
kubectl describe deployment flask-app

# Get HPA details
kubectl describe hpa flask-app-hpa

# Watch pods as they scale
kubectl get pods -l app=flask-app -w

# Monitor resource usage
kubectl top pods
```
