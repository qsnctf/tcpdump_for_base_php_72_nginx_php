# CTF 攻击流量出题环境

基于 Docker 的一键式 CTF 流量分析题出题环境，自动抓取所有网络流量并导出 pcap 文件，方便出题人制作流量分析 / 流量取证类题目。

## 架构

```
┌─────────────┐     ┌──────────────┐     ┌───────────┐
│   Nginx     │────▶│  PHP 7.2-FPM │────▶│  MySQL 5.7│
│  :8080→80   │     │   :9000       │     │  :3306     │
└──────┬──────┘     └──────────────┘     └───────────┘
       │
       │ network_mode: service:nginx
┌──────┴──────┐
│   tcpdump   │  ──▶  ./pcap/*.pcap
│  (抓包容器)  │
└─────────────┘
```

| 服务 | 说明 |
|------|------|
| **nginx** | Web 服务器，端口 `8080`，日志映射到 `./logs/nginx/` |
| **php** | PHP 7.2-FPM，带 pdo_mysql / mysqli / gd / zip 扩展 |
| **mysql** | MySQL 5.7，首次启动自动导入 `db.sql` |
| **tcpdump** | 共享 nginx 网络命名空间，持续抓包到 `./pcap/` |

## 目录结构

```
.
├── docker-compose.yml      # 主编排文件
├── db.sql                  # 数据库初始化 SQL（首次启动自动导入）
├── exp.py                  # 攻击利用脚本（CTF 选手参考/出题验证）
├── README.md
├── files/                  # Web 根目录 /var/www/html
│   ├── index.php           # 默认首页
│   └── shell.php           # PHP 一句话后门
├── pcap/                   # tcpdump 抓包输出（Wireshark 可直接打开）
├── logs/
│   └── nginx/              # Nginx access/error 日志
├── conf/
│   └── nginx/
│       └── default.conf    # Nginx 站点配置
└── build/
    ├── php/
    │   └── Dockerfile      # PHP 7.2 镜像构建
    └── tcpdump/
        ├── Dockerfile      # tcpdump 镜像构建
        └── entrypoint.sh   # 抓包启动脚本
```

## 快速开始

### 1. 启动环境

```bash
docker-compose up --build -d
```

等待所有容器启动完成：

```bash
docker-compose ps
```

确认四个容器（nginx、php、mysql、tcpdump）均为 `Up` 状态。

### 2. 验证服务

浏览器访问 `http://localhost:8080`，应看到 PHP 信息页面及数据库连接状态。

### 3. 模拟攻击流量

使用 `exp.py` 脚本模拟攻击者行为，生成攻击流量：

```bash
# 默认模式：读取 /etc/passwd，成功后进入交互式 shell
python exp.py

# 仅读取 /etc/passwd
python exp.py -r

# 执行单条命令
python exp.py -c "cat /etc/shadow"

# 指定目标地址
python exp.py -u http://target-ip:8080/shell.php
```

交互模式下可逐条输入命令，输入 `exit` 退出。

### 4. 停止抓包并导出流量

```bash
# 停止 tcpdump 容器（pcap 文件自动保留）
docker-compose stop tcpdump
```

抓包文件位于 `./pcap/` 目录，文件名格式为 `capture_YYYYMMDD_HHMMSS.pcap`。

### 5. 制作题目

将 `pcap/` 中的 pcap 文件分发给选手，结合 `logs/nginx/` 中的日志，构成流量分析题。

### 6. 停止环境

```bash
docker-compose down
```

如需清除数据库数据：

```bash
docker-compose down -v
```

## 自定义出题

### 修改 Web 应用

将你的 PHP 文件放入 `files/` 目录，它们会自动映射到容器的 `/var/www/html`。

### 修改后门类型

编辑 `files/shell.php`，可替换为其他类型的后门（如隐藏参数、编码绕过等），以调整题目难度。

### 导入数据库

将 SQL 语句写入 `db.sql`，首次启动 MySQL 时会自动导入。若需重新导入：

```bash
docker-compose down -v
docker-compose up -d
```

### 修改 Nginx 配置

编辑 `conf/nginx/default.conf`，修改后重启 nginx：

```bash
docker-compose restart nginx
```

## 出题流程总结

1. 编写 Web 应用和后门，放入 `files/`
2. 按需编写 `db.sql` 初始化数据
3. 启动环境 `docker-compose up --build -d`
4. 使用攻击脚本（或手工）产生攻击流量
5. 停止 tcpdump `docker-compose stop tcpdump`
6. 取 `pcap/` 和 `logs/nginx/` 作为题目附件
7. 编写题面，如："分析流量包，找到攻击者使用的后门密码和执行的命令"

## 数据库连接信息

| 参数 | 值 |
|------|-----|
| Host | mysql（容器内）/ localhost:3306（宿主机） |
| Database | app |
| Root Password | root |
| User | app |
| Password | app |
