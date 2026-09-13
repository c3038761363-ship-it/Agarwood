# Agarwood Prospecting

面向沉香、线香、乌木香（oud）、芳香疗愈、宗教香氛、沉香手串、沉香原材和香具行业的海外 B2B 客户开发 Skill。

它使用公开来源执行完整的客户开发流程：

1. 明确目标市场、产品和客户类型
2. 多路径搜索潜在客户
3. 核实公司、产品类目、官网和公开联系方式
4. 按 ICP 评分并识别产品切入点
5. 去重、排序并输出可开发客户
6. 在确认采用后同步客户台账

## 安装

将本仓库克隆到 Codex/ChatGPT Skills 目录：

```bash
git clone https://github.com/c3038761363-ship-it/Agarwood.git ~/.codex/skills/agarwood-prospecting
```

重新载入 Skills 后，可直接提出类似请求：

> 帮我寻找 10 家澳大利亚沉香、香薰或宗教用品批发商。逐家公司核实主营类目和官网公开联系方式，排除台账已有客户，并给出个性化开发角度。

## 目录

- `SKILL.md`：主工作流与调用规则
- `references/`：ICP、搜索、联系方式验证、去重和输出规范
- `scripts/sync_ledger.py`：已采用客户的台账同步脚本
- `台账/seen.json`：标准去重台账
- `state/seen.json`：兼容旧版路径的空台账
- `agents/openai.yaml`：界面元数据
- `assets/icon.svg`：Skill 图标

## 数据原则

- 只使用公开可访问的商业信息
- 不登录、不绕过 CAPTCHA 或访问控制
- 不猜测邮箱，也不把普通电话号码推断为 WhatsApp
- 搜索结果摘要和平台页面只能用于发现，不能单独作为最终证据
- 只有在用户确认客户已采用、导入或实际使用后才写入台账

## License

MIT
