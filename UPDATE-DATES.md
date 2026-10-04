# 日期筛选更新

## 安装
关闭正在运行的扫描和看板窗口。把本更新包内容解压到现有 D:\code\job-scan，覆盖同名程序文件。
更新包没有 profile.md、preferences.toml、search_config.json 或 output 数据，不会覆盖个人配置及评分。
可先手动复制 output 文件夹作为备份。

## 第一次：补齐原有岗位的发布日期
```powershell
powershell -ExecutionPolicy Bypass -File .\Run-Scan.ps1 -FetchOnly
```
重新抓取能为仍被来源返回的岗位补齐日期。已有评分、状态和 first_seen 保留；旧岗位未再次出现时日期仍可能未知。
日期未知单独保留，不能凭 first_seen 推断真实发布日期。

## 阶段一：近7天
```powershell
powershell -ExecutionPolicy Bypass -File .\Run-Scan.ps1 -ScoreOnly -Days 7 -MaxJobs 20
powershell -ExecutionPolicy Bypass -File .\Open-Review.ps1
```
重复评分命令会接着评分该窗口内未评分岗位，不会重复消耗已评分岗位。
看板默认近7天、最低75分、隐藏已申请/拒绝/审核岗位；可改最低65分或不限以查看候补/待评分。
每批20只是额度控制，不代表已完成全部近期岗位；出现 eligible pending batch: 0 才表示该窗口无待评分岗位（开启 auto_score 时）。

## 阶段二：近30天
```powershell
powershell -ExecutionPolicy Bypass -File .\Run-Scan.ps1 -ScoreOnly -Days 30 -MaxJobs 20
```
看板将日期选为近30天。已评分/已处理岗位不再评分；保留之前近7天的分数。

## 每日14:00
先确认手动抓取与评分成功，再运行：
```powershell
powershell -ExecutionPolicy Bypass -File .\Install-Schedule.ps1 -Time '14:00'
```
每日抓取全部配置来源，按链接合并，只评分近7天内未评分岗位，新发布的优先。默认每次20个（preferences.toml 的 max_jobs_per_run）；数量超出时下一次继续。
这同时保留失败/关机遗漏的近期积压，不仅限于当天发布。超过7天的积压需用 -Days 30 手动处理。
任务默认时间已改为14:00，时间按 Windows 本地时区；需要电脑开机且用户已登录。
只负责抓取和评分，不自动提交申请。原来的定时任务会以相同名称更新。

## 限制
看板“今日发现”依据首次发现日期，不等于今日发布。刚开始用的第一批岗位可能全部显示为同日发现。
已过明确截止日期的岗位隐藏；没有截止日期不能保证岗位仍开放，投递前检查原链接。
公司官网来源未提供日期时不会进入7/30天窗口；在“所有日期（含未知）”中查看。没有实现逐家公司补抓。
边界按本地日历日期计算：近7天为发布日期距今天0至7天，近30天为0至30天。
评分达到75仅是模型判断，不代表面试概率；先审查结果并校准。
