#!/bin/bash
# Kubernetes 部署脚本示例（供 dev_deploy.sh / prod_deploy.sh 调用或参考）
# 使用前请设置环境变量或修改下方默认值；需已安装 kubectl 并配置好 kubeconfig

set -e

APP_NAME="${APP_NAME:-sn}"
NAMESPACE="${NAMESPACE:-api-server}"
IMAGE="${IMAGE:-registry.dic.hillstonenet.com/private/${APP_NAME}:latest}"
CONFIGMAP_ENV="${CONFIGMAP_ENV:-${APP_NAME}-env}"
IMAGE_PULL_SECRET="${IMAGE_PULL_SECRET:-docker-registry}"
CONTAINER_PORT="${CONTAINER_PORT:-5000}"

# 若集群拉取使用 docker.dic.hillstonenet.com，可覆盖 IMAGE，例如：
# export IMAGE=docker.dic.hillstonenet.com/private/${APP_NAME}:latest

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="${SCRIPT_DIR}/../assets/k8s"
MANIFEST="${TEMPLATE_DIR}/deployment-template.yaml"

if [[ ! -f "$MANIFEST" ]]; then
  echo "Template not found: $MANIFEST" >&2
  exit 1
fi

# 使用 envsubst 替换占位符并应用（若无 envsubst 可改用 sed 逐项替换）
export APP_NAME NAMESPACE IMAGE CONFIGMAP_ENV IMAGE_PULL_SECRET CONTAINER_PORT
envsubst '$APP_NAME $NAMESPACE $IMAGE $CONFIGMAP_ENV $IMAGE_PULL_SECRET $CONTAINER_PORT' < "$MANIFEST" | kubectl apply -f -

echo "Deployment and Service applied. Checking rollout..."
kubectl rollout status deployment/"${APP_NAME}" -n "${NAMESPACE}" --timeout=300s
