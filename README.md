# Desert Cat 企业级 UI 自动化

独立 Python 3.11 + Playwright 测试工程。30 条 UI 目录用例按领域组织：28 个路由页面在桌面和手机视口执行 56 个浏览器流程，2 个尚无产品路由的组件产生 4 个明确 `xfail`，另有独立登录/权限守卫套件。测试函数不直接维护选择器，页面契约由 Page Object 层管理。

## 架构

```text
cases.py                       30 条静态页面目录
src/desertcat_ui/
  config/settings.py          环境、身份、视口、超时和产物配置
  execution/route_resolver.py 路由覆盖与 ID 解析
  execution/executor.py       登录态、权限守卫、页面错误、刷新与失败取证
  execution/component_contract.py 无路由 Vue 组件契约
  pages/base.py               Page Object 公共行为
  pages/registry.py           28 个路由页面的具体控件契约
tests/ui/                      公共、社区、社交、账号/管理领域套件
tests/unit/                    不启动浏览器的框架行为测试
configs/                       本地与 CI 环境模板
scripts/                       安装和分层运行入口
reports/                       截图、视频、HTML 和 JUnit 产物
```

设计细节见 [ARCHITECTURE.md](ARCHITECTURE.md)。

## 初始化与运行

```powershell
cd D:\desert-cat\ui-automation
.\scripts\bootstrap.ps1
Copy-Item .env.example .env
.\scripts\run.ps1 -Suite smoke
.\scripts\run.ps1 -Suite regression
.\scripts\run.ps1 -Suite admin
```

管理页面需要在 `TEST_USER_INFO_JSON.permissions` 中配置对应 `page:*` 权限。默认 `UI_REQUIRE_AUTH=true`，缺少 Token 或必需权限会在测试会话启动时直接失败，避免受保护正向流程全部跳过后流水线仍显示绿色。只有明确执行公共页面时才可设置 `UI_REQUIRE_AUTH=false`；权限拒绝仍由独立守卫套件验证。

## 常用命令

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests\unit
.\.venv\Scripts\python.exe run_ui.py -m "ui and p0"
.\.venv\Scripts\python.exe run_ui.py -m "ui and community" --headed
.\.venv\Scripts\python.exe generate_cases.py
```

正向页面流程缺少 Token 或权限时会明确跳过，不会把登录跳转冒充成页面通过；登录与权限拒绝由独立的 `access_control` 套件验证。每次失败保存整页截图；浏览器上下文录制视频；同时采集未处理脚本异常、控制台错误及 `/api/` 500 响应。
