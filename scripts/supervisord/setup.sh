#!/usr/bin/env bash
set -euo pipefail

# 项目根目录：本脚本位于 <project>/scripts/supervisord/setup.sh
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

START_WEB="$PROJECT_DIR/start_web.sh"
PROGRAM_NAME="flask-dlt645"
SUPERVISOR_CONF_DIR="/etc/supervisor/conf.d"
SUPERVISOR_CONF="$SUPERVISOR_CONF_DIR/${PROGRAM_NAME}.conf"
LOG_DIR="/var/log/$PROGRAM_NAME"

echo "Project dir : $PROJECT_DIR"
echo "Start script: $START_WEB"

# 确保 start_web.sh 可执行
chmod +x "$START_WEB" "$SCRIPT_DIR/setup.sh"

# 确保日志目录存在
mkdir -p "$LOG_DIR"

# 安装 supervisor（如未安装）
if ! command -v supervisord >/dev/null 2>&1; then
    echo "supervisord not found, installing..."
    if command -v apt-get >/dev/null 2>&1; then
        apt-get update && apt-get install -y supervisor
    elif command -v yum >/dev/null 2>&1; then
        yum install -y supervisor
    else
        echo "No supported package manager found. Please install supervisor manually." >&2
        exit 1
    fi
fi

# 创建 conf.d 目录（supervisor 主配置通常 include 该目录）
mkdir -p "$SUPERVISOR_CONF_DIR"

# 写入 supervisord 程序配置：开机自启并运行 start_web.sh
cat > "$SUPERVISOR_CONF" <<EOF
[program:$PROGRAM_NAME]
command=$START_WEB
directory=$PROJECT_DIR
autostart=true
autorestart=true
startsecs=3
startretries=3
stopasgroup=true
killasgroup=true
user=root
stdout_logfile=$LOG_DIR/out.log
stderr_logfile=$LOG_DIR/err.log
stdout_logfile_maxbytes=10MB
stderr_logfile_maxbytes=10MB
EOF

echo "Wrote supervisor config: $SUPERVISOR_CONF"

# 重新加载 supervisor 配置并启动程序
if command -v supervisorctl >/dev/null 2>&1; then
    if supervisorctl status >/dev/null 2>&1; then
        supervisorctl reread
        supervisorctl update
        supervisorctl restart "$PROGRAM_NAME" || supervisorctl start "$PROGRAM_NAME"
    else
        echo "supervisord is not running. Starting it..."
        supervisord -c /etc/supervisor/supervisord.conf 2>/dev/null || supervisord
        supervisorctl reread
        supervisorctl update
        supervisorctl start "$PROGRAM_NAME"
    fi
else
    echo "supervisorctl not available, please start supervisord manually."
fi

echo "Done. $PROGRAM_NAME is configured to start on boot (autostart=true)."
