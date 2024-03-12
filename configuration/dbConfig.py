# apps/dbConfig.py

TORTOISE_ORM = {
    "connections": {
        # "mysql://root:lzs@localhost:3306/water_manager",
        "default": {
            'engine': 'tortoise.backends.mysql',
            'credentials': {
                'host': 'localhost',
                'port': '3306',
                'user': 'root',
                'password': 'lzs',
                'database': 'eduSystem',
                'minsize': 1,
                'maxsize': 5,
                'charset': 'utf8mb4',
                'echo': True
            }
        }
    },
    "apps": {
        "models": {
            "models": ["pojo.entity", "aerich.models"],
            # 指定模型所在的路径
            "default_connection": "default",
        }
    },
    "use_tz": False,  # 是否使用时区
    "check_schema_every_startup": True,  # 每次启动时检查表结构
    'timezone': 'Asia/Shanghai',
}
