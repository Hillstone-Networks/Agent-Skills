# Dev 环境 K8s 部署模板（使用 envsubst 替换 ${CI_PROJECT_NAME}）
# 在 GitLab CI 的 dev_deploy 中执行：envsubst < dev_deployment.yaml.tpl > deployment.yaml && kubectl apply -f deployment.yaml
# 命名空间 api-server；镜像 docker.dic.hillstonenet.com/private/${CI_PROJECT_NAME}:latest；ConfigMap ${CI_PROJECT_NAME}-env
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${CI_PROJECT_NAME}
  namespace: api-server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ${CI_PROJECT_NAME}
  template:
    metadata:
      labels:
        app: ${CI_PROJECT_NAME}
    spec:
      dnsPolicy: "None"
      dnsConfig:
        nameservers:
          - 10.86.249.24
          - 10.86.249.42
      imagePullSecrets:
        - name: docker-registry
      containers:
        - name: ${CI_PROJECT_NAME}
          image: docker.dic.hillstonenet.com/private/${CI_PROJECT_NAME}:latest
          imagePullPolicy: Always
          envFrom:
            - configMapRef:
                name: ${CI_PROJECT_NAME}-env
          env:
            - name: SERVICE_NAME
              value: ${CI_PROJECT_NAME}
            - name: PROJECT_ID
              value: ${CI_PROJECT_NAME}
          ports:
            - containerPort: 5000
---
apiVersion: v1
kind: Service
metadata:
  name: ${CI_PROJECT_NAME}
  namespace: api-server
spec:
  selector:
    app: ${CI_PROJECT_NAME}
  ports:
    - protocol: TCP
      port: 5000
      targetPort: 5000
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ${CI_PROJECT_NAME}-ingress
  namespace: api-server
  annotations:
    nginx.ingress.kubernetes.io/proxy-body-size: "20m"
spec:
  ingressClassName: api-server
  rules:
    - host: ${CI_PROJECT_NAME}.apistest.dic.hillstonenet.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: ${CI_PROJECT_NAME}
                port:
                  number: 5000
