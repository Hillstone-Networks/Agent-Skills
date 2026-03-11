# 应用工厂与 Blueprint 自动注册示例（参考，需按项目包名调整）

def create_app(config_name: str = None):
    from flask import Flask
    from app.config import config_by_name
    from app.extensions import db  # 等扩展

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name or "development"])

    # 扩展初始化
    db.init_app(app)
    # 其他扩展 init_app(app)

    # 注册 Blueprint：可改为 register_all_blueprints(app)
    from app.routes import main_api
    app.register_blueprint(main_api.main_app)

    # 钩子
    @app.before_request
    def before_request_handler():
        # 解析 JWT，写入 g.current_user
        pass

    @app.after_request
    def after_request_handler(response):
        # 添加 X-Trace-Id 等响应头
        return response

    @app.teardown_request
    def teardown_request_handler(error=None):
        pass

    # 全局错误处理
    @app.errorhandler(Exception)
    def handle_exception(e):
        # 统一返回 {code, message, data}，记录 trace_id
        pass

    return app


def register_all_blueprints(flask_app):
    import os
    import importlib
    import inspect
    import logging

    views_path = os.path.join(os.path.dirname(__file__), "routes")
    for root, _dirs, files in os.walk(views_path):
        for name in sorted(files):
            if not name.endswith("_api.py"):
                continue
            if flask_app.config.get("DISABLEPATH") and name in flask_app.config["DISABLEPATH"]:
                continue
            app_name = name.rsplit("_", 1)[0] + "_app"
            base = os.path.splitext(name)[0]
            module_path = "app.routes." + base
            try:
                mod = importlib.import_module(module_path)
                if hasattr(mod, app_name):
                    flask_app.register_blueprint(getattr(mod, app_name))
            except Exception as e:
                logging.error("注册蓝图失败: %s - %s", name, e)
