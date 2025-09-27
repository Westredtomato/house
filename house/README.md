适用于已安装所有依赖的环境；生成当前 Python 环境下的所有包（包括项目未直接使用的依赖）。会固定版本号（如 flask==2.0.1），适合生产环境。
pip freeze > requirements.txt



使用 pipreqs（仅生成项目实际使用的依赖）
pip install pipreqs

当前目录的依赖文件， . 表示当前目录 --force 覆盖已有文件， . 表示项目的根目录
pipreqs . --encoding=utf8 --force
