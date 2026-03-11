# Kubernetes 部署说明（dev → prod，必须使用 K8s）

部署方式**必须**为 dev（测试）→ prod（生产）两环境，通过 `.gitlab-ci.yml` 的 dev_deploy / prod_deploy 调用 `scripts/dev_deploy.sh`、`scripts/prod_deploy.sh`，使用模板 `dev_deployment.yaml.tpl`（及可选 prod 模板）经 `envsubst` 替换 `${CI_PROJECT_NAME}` 后 `kubectl apply`。

## 前置条件

- Runner 已配置 `kubectl` 且可访问 dev/prod 集群；context 分别为 `kubernetes-admin-dev@kubernetes`、`kubernetes-admin-prod@kubernetes`。
- 命名空间 `api-server` 已存在；拉取私有镜像的 Secret `docker-registry` 已在命名空间中创建。
- ConfigMap `${CI_PROJECT_NAME}-env` 可由部署脚本在首次部署时从 `.env.example` 创建（脚本内判断不存在则 `kubectl create configmap ... --from-env-file=.env.example -n api-server`）。

## 镜像与模板

- 镜像：**docker.dic.hillstonenet.com/private/${CI_PROJECT_NAME}:latest**（模板中已写死，与 CI 推送的 registry.dic.hillstonenet.com 对应同一镜像）。
- Dev 模板：见 [dev_deployment.yaml.tpl](dev_deployment.yaml.tpl)。含 Deployment、Service、Ingress；变量 `${CI_PROJECT_NAME}`；Ingress host `${CI_PROJECT_NAME}.apistest.dic.hillstonenet.com`，ingressClassName `api-server`。

## 部署脚本流程（dev_deploy.sh）

1. `kubectl config use-context kubernetes-admin-dev@kubernetes`
2. 若 `.env.example` 无 `ENV=dev`，则 `sed -i '1i ENV=dev' .env.example`
3. 若 ConfigMap `${CI_PROJECT_NAME}-env` 不存在，则 `kubectl create configmap ${CI_PROJECT_NAME}-env --from-env-file=.env.example -n api-server`
4. `envsubst < <模板路径> > deployment.yaml`（模板路径可为项目内 `k8s/dev_deployment.yaml.tpl` 或 Runner 固定路径 `/.flaskserver/dev_deployment.yaml.tpl`）
5. `kubectl apply -f deployment.yaml`
6. `kubectl rollout restart deployment ${CI_PROJECT_NAME} -n api-server`

prod_deploy.sh 同理，切换 context 到 prod，ENV=prod，可选 prod 专用模板（如不同 Ingress host）。

## 使用通用占位符模板（可选）

若使用占位符模板（如 deployment-template.yaml，变量 APP_NAME、NAMESPACE、IMAGE 等），可手动替换或 `envsubst` 后 apply；仅更新镜像时：`kubectl set image deployment/<APP_NAME> <APP_NAME>=<IMAGE>:<TAG> -n <NAMESPACE>`，`kubectl rollout status ...`。

## 常用命令

```bash
# 查看部署与 Pod
kubectl get deployment,po -n <namespace> -l app=<APP_NAME>

# 查看日志
kubectl logs -f deployment/<APP_NAME> -n <namespace>

# 重启部署（拉取新镜像需先 set image 或更新 manifest 后 apply）
kubectl rollout restart deployment/<APP_NAME> -n <namespace>
```
