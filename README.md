# STM32 F1 / F4 / L4 学习项目清单

> 给大学生的一份 GitHub 项目地图：从点灯到能写进简历的实物项目。

**在线浏览 👉 https://benyshen.github.io/stm32-picks/**

## 这是什么

一份面向本科电子/自动化/嵌入式方向学生的 STM32 开源项目精选清单，共 **70 个仓库**，按学习阶段与项目类型组织：

| 章节 | 内容 |
|---|---|
| 0 | 四阶段路线图 + F1/F4/L4 选型分工 |
| 1 | 官方 STM32CubeF1/F4/L4（拿来查，不拿来学） |
| 2 | 工程模板 / 从零搭架子 |
| 3 | 外设例程（SPL / HAL / libopencm3 裸机） |
| 4 | 中文资源（FreeRTOS 中文教程、笔记库、awesome 索引） |
| 5 | 真实项目 8 类：飞控机器人、电机 FOC、CNC/3D 打印、仪器仪表、低功耗可穿戴、物联网智能家居、USB/HID 工具固件、Bootloader/OTA |
| 6 | 进阶：RTOS 与工业级框架 |
| 7 | 怎么把「抄一个项目」变成「自己的项目」+ 三档推荐组合 |
| 8 | 硬件与工具最小清单（含价格） |
| 9 | 数据说明与免责 |

选码原则：能在真实硬件上跑、有完整工程（不是只有 `.c` 片段）、中文注释或文档友好、维护活跃。

## 页面功能

- 实时搜索（项目名 / 描述 / 关键词）
- 按芯片系列筛选：全部 / F1 / F4 / L4
- 系列色标 + ★ 星数 + 一句话说明的项目卡片
- 粘性侧边目录、深浅色切换、打印/存 PDF 适配
- 单文件、零外部依赖，断网可看

## 数据

- 星数与更新时间：**2026-11-08** 从 GitHub 官方 Search API 抓取
- 全部仓库外链已逐一实测 HTTP 200（`links.txt` 可复检）
- 部分中文项目是学生毕设代码，工程规范参差：当参考实现，不要当工程范本
- 引用他人代码/硬件设计请遵守仓库 LICENSE 并注明出处

## 工程结构

```
index.html                      生成的单页网页（Pages 入口）
STM32-F1-F4-L4-学习项目清单.md   源文档（改内容改这个）
build_html.py                   Markdown → HTML 生成器
links.txt                       仓库链接清单（复检用）
.nojekyll                       关闭 Jekyll 处理
```

重新生成：

```bash
python build_html.py
```

## 相关项目

- [zpl-core](https://github.com/benyshen/zpl-core) —— ZPL 指令生成与校验引擎
- [awesome-image-prompts](https://github.com/benyshen/awesome-image-prompts) —— AI 生图提示词案例库
