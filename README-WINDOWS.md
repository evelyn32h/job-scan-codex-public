# Job Scan — Windows + Codex 版

原项目 https://github.com/1carusalwayswa/job-scan ，MIT 许可保留。
新增入口是 scripts/codex_scan.py；不要使用原 Claude daily_scan.sh / setup 指令。

## 安装
1. 安装 Python 3.11+（勾选 Add Python to PATH）和 Node.js LTS。重新打开 VS Code / PowerShell。
2. 解压整个 job-scan 文件夹到固定位置，例如 C:\Users\你的用户名\Projects\job-scan。不要只复制 scripts。
3. 在该文件夹打开 PowerShell：

```powershell
python --version
node --version
npm install -g @openai/codex
codex login
codex login status
```
登录选择你的 ChatGPT Plus 账户，不需要 API key。不向任何人发送 token。
如果系统已有 OPENAI_API_KEY / CODEX_API_KEY 或自定义 provider，请核对 Codex 实际账户与计费方式。

4. 检查 profile.md 是否准确（已按当前已知经历填写，未加入私人健康或关系信息）。修改 search_config.json 和 preferences.toml。

## 首次验证与使用
```powershell
powershell -ExecutionPolicy Bypass -File .\Run-Scan.ps1 -FetchOnly
powershell -ExecutionPolicy Bypass -File .\Run-Scan.ps1 -ScoreOnly
powershell -ExecutionPolicy Bypass -File .\Open-Review.ps1
```
本地看板 http://localhost:8765；关闭窗口/按 Ctrl+C 可退出。
以后完整运行：
```powershell
powershell -ExecutionPolicy Bypass -File .\Run-Scan.ps1
```
默认一次最多评分 20 个岗位，每批 5 个；失败批次保持待评分，下次继续。可调整 preferences.toml。
工签不支持/工作权利/安全审查是独立提示，不排除，不降低技术分。仅明确强制瑞典或 EU/EEA 国籍且不符合时隐藏。国籍检测保守，含糊句子可能需人工确认。
明确要求瑞典语的岗位按已有语言规则隐藏；咨询/运维/网络不按类别硬排除。
标题/短摘要不足 300 字符的岗位保留，评分最多 59 并标待确认。当前没有通用全文补抓；公司官网需要逐家适配验证。
来源：JobSearch（Platsbanken）。target_companies.json 初始为空，不宣称已监控任何公司。可按原 README 配置官网，抓取失败会报警并保留部分数据。未接 LinkedIn、Indeed、芬兰专用接口或 JobAd Links。

## 每天自动运行（手动验证成功后）
```powershell
powershell -ExecutionPolicy Bypass -File .\Install-Schedule.ps1 -Time '07:00'
```
电脑开机且用户已登录才能运行；时间按 Windows 本地时区。额度/登录过期可能使评分暂停。
日志 output/scheduled-scan.log。卸载：Unregister-ScheduledTask -TaskName JobScan-Codex。
如果程序强制终止遗留 scan.lock，确认没有扫描进程后删除 output/scan.lock。
扫描期间避免在看板改状态（批次保存会重读状态，但最后写入时存在短暂竞争窗口）。

## 验证范围
随包包含自动化测试：python -m unittest discover -s tests -v。
已在 Linux 环境验证 Python 逻辑；Windows PowerShell/任务调度和你的 Plus 实际评分必须在你本机验证。不会代替你登录，也未部署到你的电脑。
