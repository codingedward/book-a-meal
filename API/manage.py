import os

app = create_app(config_name=os.getenv('APP_MODE'))


if __name__ == '__main__':
    manager.run()
