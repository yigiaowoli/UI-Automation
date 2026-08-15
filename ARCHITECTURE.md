# UI 自动化架构

## 执行链

`UiCaseExecutor.execute(page, case, viewport)` 是领域测试使用的唯一公开接口：

1. `RouteResolver` 解析路由参数和环境覆盖。
2. 执行器在首个文档脚本前注入测试身份，并验证登录/权限守卫。
3. `PageRegistry` 返回页面对象，统一执行加载契约和主流程交互。
4. 执行器检查横向溢出、空白页面、刷新恢复、控制台、页面异常和后端 500。
5. 异常时自动保存截图，浏览器上下文持续录制视频。

注册与找回密码组件在产品路由中没有入口，因此先由 `ComponentContract` 校验字段绑定；测试结果标记为 `xfail`，不会冒充浏览器 UI 通过。一旦产品增加路由，必须迁移为浏览器 Page Object 后才能计入 UI 通过率。

## 选择器治理

- 业务测试文件不允许写 CSS/XPath。
- 稳定选择器集中在 `pages/registry.py`。
- 页面复杂交互应新增专用 Page Object，而不是在测试中增加步骤。
- 每个目录用例的根选择器必须与 Page Object 注册值一致。

## 失败诊断

- `reports/failures/`：失败整页截图。
- `reports/videos/`：浏览器上下文视频。
- `reports/ui-report.html`：可离线查看的 HTML 报告。
- `reports/ui-junit.xml`：CI 测试结果。
