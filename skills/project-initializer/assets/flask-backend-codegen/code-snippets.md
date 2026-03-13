# 代码片段参考

生成路由、Service、Model 时可按以下模式套用，并替换资源名与字段。

## RequestParser（GET 列表分页）

```python
from flask_restful import reqparse

list_parser = reqparse.RequestParser()
list_parser.add_argument("page", type=int, default=1, location="args")
list_parser.add_argument("size", type=int, default=20, location="args")
# 其他筛选参数 location="args"
```

## RequestParser（POST/PUT body）

```python
create_parser = reqparse.RequestParser()
create_parser.add_argument("username", required=True, location="json")
create_parser.add_argument("email", location="json")
# location="json" 表示从请求体 JSON 解析
```

## Resource 示例（列表 + 详情）

```python
# app/routes/user_api.py
from flask import Blueprint
from flask_restful import Resource
from app.utils.api_util import Api, AppResponse, AppException
from app.permission import permission_required
from app.service import user_service

bp = Blueprint("user", __name__, url_prefix="/api/users")
api = Api(bp)

class UserListResource(Resource):
    @permission_required("user", "read")
    def get(self):
        args = list_parser.parse_args()
        page, size = args["page"], args["size"]
        list_data, total = user_service.get_list(page=page, size=size)
        return AppResponse(data={"page": page, "size": size, "list": list_data, "total": total})

class UserDetailResource(Resource):
    @permission_required("user", "read")
    def get(self, user_id: int):
        item = user_service.get_by_id(user_id)
        if not item:
            raise AppException(code=4001, message="用户不存在")
        return AppResponse(data=item)

api.add_resource(UserListResource, "/")
api.add_resource(UserDetailResource, "/<int:user_id>")
```

## Service 示例（不依赖 request/g）

```python
# app/service/user_service.py
from app.extensions import db
from app.models.user import User

def get_list(page: int = 1, size: int = 20) -> tuple[list, int]:
    query = User.query.filter_by(deleted_at=None)
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return [item.to_dict() for item in items], total

def get_by_id(user_id: int):
    user = User.query.get(user_id)
    return user.to_dict() if user else None
```

## Model 示例（通用字段）

```python
# app/models/user.py
from datetime import datetime
from app.extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)  # 软删除可选

    def to_dict(self):
        return {"id": self.id, "username": self.username}
```

## 测试方法命名

```python
# tests/test_api_user.py
def test_get_user_list_success_returns_pagination(client, auth_headers):
    ...

def test_get_user_detail_not_found_returns_4001(client, auth_headers):
    ...
```

## 权限策略（policies.py 中补充）

新增资源时在 `app/permission/policies.py` 中增加策略，例如：

- 资源名：`user`；操作：`read`、`create`、`update`、`delete`。
- 执行 `flask sync-permissions` 将策略同步到 Casbin。
