<div align="center">

# 🚀 MockServer-CLI

**Lightweight Terminal HTTP API Mock Server**

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Zero-Dependencies-orange.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Cross--Platform-lightgrey.svg)]()

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)

</div>

---

<a name="english"></a>
## 🇺🇸 English

### 🎉 Project Introduction

**MockServer-CLI** is a lightweight, zero-dependency terminal HTTP API mock server designed for developers who need to quickly mock REST APIs during development and testing phases.

**Why MockServer-CLI?**
- 🚫 **Zero Dependencies** - Uses only Python standard library, no pip install needed
- ⚡ **Lightning Fast** - Start mocking APIs in seconds with simple JSON/YAML config
- 🎯 **Developer Friendly** - Intuitive CLI interface with helpful error messages
- 🔧 **Highly Configurable** - Dynamic routes, path parameters, template variables
- 📊 **Built-in Monitoring** - Request logging and statistics

### ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🌐 **HTTP Methods** | Support GET, POST, PUT, DELETE, PATCH, OPTIONS |
| 🛣️ **Dynamic Routes** | Path parameters with `:id` syntax |
| 📝 **Template Engine** | Built-in variables: `{{timestamp}}`, `{{random}}`, `{{params.id}}`, `{{body.field}}` |
| 🌟 **CORS Support** | Automatic CORS headers for frontend development |
| ⏱️ **Delay Simulation** | Simulate network latency |
| ❌ **Error Simulation** | Configure error rate for resilience testing |
| 📊 **Request Logging** | Track and analyze API calls |
| 📄 **JSON/YAML Config** | Flexible configuration formats |

### 🚀 Quick Start

#### Installation

```bash
# Clone the repository
git clone https://github.com/gitstq/MockServer-CLI.git
cd MockServer-CLI

# Or install via pip
pip install mockserver-cli
```

#### Basic Usage

```bash
# Start with default configuration
python mockserver.py

# Start with custom config
python mockserver.py -c mockserver.config.json

# Start on different port
python mockserver.py -p 3000

# Create sample config file
python mockserver.py --init
```

#### Configuration Example

```json
{
  "host": "127.0.0.1",
  "port": 8080,
  "cors": true,
  "delay": 0,
  "error_rate": 0,
  "routes": {
    "/api/users": {
      "method": "GET",
      "status": 200,
      "response": {
        "users": [
          {"id": 1, "name": "Alice"},
          {"id": 2, "name": "Bob"}
        ]
      }
    },
    "/api/users/:id": {
      "method": "GET",
      "status": 200,
      "response": {
        "id": "{{params.id}}",
        "name": "User {{params.id}}"
      }
    }
  }
}
```

### 📖 Detailed Usage Guide

#### Template Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{{timestamp}}` | Current ISO timestamp | `2024-01-15T10:30:00` |
| `{{random}}` | Random number (0-9999) | `1234` |
| `{{params.name}}` | Path parameter | `/users/:id` → `{{params.id}}` |
| `{{body.field}}` | Request body field | POST JSON body |

#### CLI Options

```bash
mockserver-cli [OPTIONS]

Options:
  -c, --config PATH    Configuration file path
  -p, --port PORT      Server port (default: 8080)
  -H, --host HOST      Server host (default: 127.0.0.1)
  --init               Create sample config file
  --stats              Show request statistics
  -v, --version        Show version
  -h, --help           Show help message
```

### 💡 Design Philosophy

MockServer-CLI was built with these principles:
1. **Simplicity** - No complex setup, just run and go
2. **Zero Dependencies** - Works anywhere Python is available
3. **Flexibility** - JSON/YAML configs, template variables
4. **Developer Experience** - Clear error messages, helpful defaults

### 📦 Packaging & Deployment

#### As Python Package

```bash
# Build package
python setup.py sdist bdist_wheel

# Install locally
pip install -e .

# After installation, use globally
mockserver-cli --help
```

#### Standalone Script

```bash
# Make executable
chmod +x mockserver.py

# Run directly
./mockserver.py
```

### 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<a name="简体中文"></a>
## 🇨🇳 简体中文

### 🎉 项目介绍

**MockServer-CLI** 是一个轻量级、零依赖的终端HTTP API Mock服务器，专为需要在开发和测试阶段快速模拟REST API的开发者设计。

**为什么选择MockServer-CLI？**
- 🚫 **零依赖** - 仅使用Python标准库，无需pip安装
- ⚡ **极速启动** - 通过简单的JSON/YAML配置，几秒钟内启动Mock服务
- 🎯 **开发者友好** - 直观的CLI界面，清晰的错误提示
- 🔧 **高度可配置** - 动态路由、路径参数、模板变量
- 📊 **内置监控** - 请求日志记录和统计分析

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🌐 **HTTP方法** | 支持GET、POST、PUT、DELETE、PATCH、OPTIONS |
| 🛣️ **动态路由** | 使用`:id`语法的路径参数 |
| 📝 **模板引擎** | 内置变量：`{{timestamp}}`、`{{random}}`、`{{params.id}}`、`{{body.field}}` |
| 🌟 **CORS支持** | 自动添加CORS响应头，方便前端开发 |
| ⏱️ **延迟模拟** | 模拟网络延迟 |
| ❌ **错误模拟** | 配置错误率进行弹性测试 |
| 📊 **请求日志** | 追踪和分析API调用 |
| 📄 **JSON/YAML配置** | 灵活的配置格式 |

### 🚀 快速开始

#### 安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/MockServer-CLI.git
cd MockServer-CLI

# 或通过pip安装
pip install mockserver-cli
```

#### 基本用法

```bash
# 使用默认配置启动
python mockserver.py

# 使用自定义配置
python mockserver.py -c mockserver.config.json

# 使用不同端口
python mockserver.py -p 3000

# 创建示例配置文件
python mockserver.py --init
```

#### 配置示例

```json
{
  "host": "127.0.0.1",
  "port": 8080,
  "cors": true,
  "delay": 0,
  "error_rate": 0,
  "routes": {
    "/api/users": {
      "method": "GET",
      "status": 200,
      "response": {
        "users": [
          {"id": 1, "name": "Alice"},
          {"id": 2, "name": "Bob"}
        ]
      }
    },
    "/api/users/:id": {
      "method": "GET",
      "status": 200,
      "response": {
        "id": "{{params.id}}",
        "name": "User {{params.id}}"
      }
    }
  }
}
```

### 📖 详细使用指南

#### 模板变量

| 变量 | 描述 | 示例 |
|------|------|------|
| `{{timestamp}}` | 当前ISO时间戳 | `2024-01-15T10:30:00` |
| `{{random}}` | 随机数字(0-9999) | `1234` |
| `{{params.name}}` | 路径参数 | `/users/:id` → `{{params.id}}` |
| `{{body.field}}` | 请求体字段 | POST JSON请求体 |

#### CLI选项

```bash
mockserver-cli [选项]

选项:
  -c, --config PATH    配置文件路径
  -p, --port PORT      服务器端口 (默认: 8080)
  -H, --host HOST      服务器主机 (默认: 127.0.0.1)
  --init               创建示例配置文件
  --stats              显示请求统计
  -v, --version        显示版本
  -h, --help           显示帮助信息
```

### 💡 设计理念

MockServer-CLI遵循以下设计原则：
1. **简洁** - 无需复杂配置，即开即用
2. **零依赖** - 只要有Python就能运行
3. **灵活** - JSON/YAML配置，模板变量
4. **开发者体验** - 清晰的错误提示，合理的默认值

### 📦 打包与部署

#### 作为Python包

```bash
# 构建包
python setup.py sdist bdist_wheel

# 本地安装
pip install -e .

# 安装后全局使用
mockserver-cli --help
```

#### 独立脚本

```bash
# 添加执行权限
chmod +x mockserver.py

# 直接运行
./mockserver.py
```

### 🤝 贡献指南

1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

### 📄 开源协议

本项目采用MIT协议开源 - 详见 [LICENSE](LICENSE) 文件。

---

<a name="繁體中文"></a>
## 🇹