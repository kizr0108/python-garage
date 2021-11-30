import os
import platform

PC_OS = 'Windows'

# ---------- 環境変数 ---------- #
if platform.system() == PC_OS:
    from dotenv import load_dotenv
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)
BT_USER = os.environ['BT_USER']
MAIL_ACCOUNT = os.environ['MAIL_ACCOUNT']
LINE_TOKEN = os.environ['LINE_TOKEN']
