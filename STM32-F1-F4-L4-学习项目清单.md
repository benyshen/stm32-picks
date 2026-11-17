# STM32F1 / F4 / L4 学习项目清单（GitHub 精选）

> 数据抓取自 GitHub 官方搜索 API，星数与更新时间截至 **2026-11-08**。
> 面向：本科电子/自动化/嵌入式方向学生，从「点灯」到「能写进简历的实物项目」。
> 选码原则：能在真实硬件上跑、有完整工程（不是只有 .c 片段）、中文注释或文档友好、维护活跃。

---

## 0. 先看这张路线图

| 阶段 | 目标 | 用什么 |
|---|---|---|
| ① 跑通工具链 | 会用 CubeMX + CubeIDE/Keil + 下载器，能点灯、串口打印 | 官方 Cube 包、STM32-base 模板 |
| ② 摸外设 | GPIO/USART/I2C/SPI/ADC/TIM/DMA 各写一遍，能读传感器、驱动屏幕 | 例程仓库 + 一个 BluePill |
| ③ 上 RTOS | 任务/队列/信号量/优先级，双任务通信 | FreeRTOS 中文教程 + 一个 L4 板 |
| ④ 做一个真项目 | 有外壳、有上位机/云、能讲清楚取舍 | 下面第 5 节任选一个改造 |

**芯片分工建议**
- **F1（F103C8T6 BluePill，¥15）**：入门首选，寄存器/SPL/HAL 资料最全，做小工具、HID、逻辑分析仪。
- **F4（F407/F429，¥60~150）**：性能课设主力，跑 GUI、USB、摄像头、DSP、飞控固件。
- **L4（NUCLEO-L476RG，¥90）**：低功耗/电池类课题、IoT 节点、可穿戴，Cube 支持最完整。

---

## 1. 官方底子：必须有，不要拿来"学"而是拿来"查"

| 项目 | ★ | 内容 | 用途 |
|---|---|---|---|
| [STMicroelectronics/STM32CubeF1](https://github.com/STMicroelectronics/STM32CubeF1) | 748 | F1 全量包（HAL+LL+CMSIS+中间件+每板例程） | 外设怎么写，看 `Projects/*/Examples` |
| [STMicroelectronics/STM32CubeF4](https://github.com/STMicroelectronics/STM32CubeF4) | 1364 | F4 全量包（150MB） | USB/DSP/以太网例程的权威来源 |
| [STMicroelectronics/STM32CubeL4](https://github.com/STMicroelectronics/STM32CubeL4) | 344 | L4 全量包（334MB） | 低功耗模式、LPUART、LCD 玻璃驱动 |

> 只下需要的系列，别全克隆：单个 150~350MB，含全部历史更大。

---

## 2. 工程模板 / 从零搭架子（阶段①）

| 项目 | ★ | 芯片 | 为什么推荐 |
|---|---|---|---|
| [STM32-base/STM32-base](https://github.com/STM32-base/STM32-base) | 432 | 全系 | Makefile + 链接脚本 + 启动文件的最小骨架，脱离 IDE 理解「程序怎么进去的」 |
| [STMicroelectronics](https://github.com/STMicroelectronics) 官方 `STM32Cube*` 的 `Projects/` | — | 全系 | 每个外设一个独立小工程，按需复制 |
| [platformio/platform-ststm32](https://github.com/platformio/platform-ststm32) | 474 | 全系 | VS Code + PlatformIO 一条命令建工程，适合不想折腾 Keil 的学生 |
| [stm32duino/Arduino_Core_STM32](https://github.com/stm32duino/Arduino_Core_STM32) | 3378 | 全系 | 用 Arduino 语法先做出东西，再回头学底层；比赛赶工期很好用 |
| [rogerclarkmelbourne/Arduino_STM32](https://github.com/rogerclarkmelbourne/Arduino_STM32) | 2677 | F1 | BluePill 社区版，配套大量 F103 例程 |

---

## 3. 例程仓库：把外设一个个吃透（阶段②）

| 项目 | ★ | 芯片 | 说明 |
|---|---|---|---|
| [yohanes-erwin/stm32f103-keil](https://github.com/yohanes-erwin/stm32f103-keil) | 289 | F1 | **标准库(SPL)** 逐外设例程，BluePill 直接烧，最贴近国内教材 |
| [avislab/STM32F103](https://github.com/avislab/STM32F103) | 977 | F1 | F103C8 例程合集（含 USB、CAN、编码器），代码短小 |
| [controllerstech/STM32-HAL](https://github.com/controllerstech/STM32-HAL) | 474 | F1/F4 | 配 YouTube 课程的 HAL 例程，I2C/SPI/DMA/定时器/中断齐全 |
| [4ilo/ssd1306-stm32HAL](https://github.com/4ilo/ssd1306-stm32HAL) | 280 | 全系 | OLED 驱动 + 位图/字体工具，课设必备零件 |
| [MaJerle/stm32f429](https://github.com/MaJerle/stm32f429) | 2523 | F4 | Keil 工程 + 自研库，DMA/定时器/USB 写得非常规范，进阶读码首选 |
| [MaJerle/stm32fxxx-hal-libraries](https://github.com/MaJerle/stm32fxxx-hal-libraries) | 833 | F4/F7 | 在 HAL 之上封装的实用库（GSM/WiFi/传感器），工程化写法参考 |
| [cnoviello/mastering-stm32](https://github.com/cnoviello/mastering-stm32) | 496 | F0/F4/L0 | 《Mastering STM32》全部示例，配书学最系统（英文原著有中文版） |
| [ve3wwg/stm32f103c8t6](https://github.com/ve3wwg/stm32f103c8t6) | 396 | F1 | libopencm3 + FreeRTOS 裸工程，教你不依赖 ST 库 |
| [Apress/Beg-STM32-Devel-FreeRTOS-libopencm3-GCC](https://github.com/Apress/Beg-STM32-Devel-FreeRTOS-libopencm3-GCC) | 121 | F1 | 《Beginning STM32》配套代码（GCC + FreeRTOS + libopencm3） |

---

## 4. 中文资源（看懂比看懂英文更重要的时候）

| 项目 | ★ | 说明 |
|---|---|---|
| [Despacito0o/FreeRTOS](https://github.com/Despacito0o/FreeRTOS) | 319 | **中文** FreeRTOS + STM32 全流程：移植、示例工程、环境配置，入门 RTOS 最省时间 |
| [wuxiaolie/Knowledge-Notes](https://github.com/wuxiaolie/Knowledge-Notes) | 1839 | 个人技术笔记大全：C/C++、总线、STM32+RTOS、Linux 驱动，当百科查 |
| [nhivp/Awesome-Embedded](https://github.com/nhivp/Awesome-Embedded) | 9324 | 嵌入式资源索引（含大量 STM32 教程/工具），找东西先搜这里 |
| [Luyi365/awesome-embedded](https://github.com/Luyi365/awesome-embedded) | 227 | 中文嵌入式开源库速查表，300+ 库按功能分类，选型时好用 |
| [iDoka/awesome-embedded-software](https://github.com/iDoka/awesome-embedded-software) | 1147 | 同上（英文），接口/协议/库分类更细 |

---

## 5. 真实项目：能改成课设/毕设/简历项目（阶段④）

### 5.1 飞控 / 机器人 / 小车

| 项目 | ★ | 芯片 | 项目实质 | 可改造点 |
|---|---|---|---|---|
| [betaflight/betaflight](https://github.com/betaflight/betaflight) | 11756 | F4/F7/H7 | 全球最主流的开源飞控固件，姿态融合+PID+电调协议 | 读 `src/main/flight`，做「姿态解算对比实验」；写一篇参数调优报告就够一个课设 |
| [StarDust-XCHH/autonomous-car-project](https://github.com/StarDust-XCHH/autonomous-car-project) | 228 | F446 | ROS1 竞速小车：RPLIDAR + IMU + 蓝牙 + 十六路循迹 | 把 ROS 换成纯上位机串口协议，成本降到几百元 |
| [dyfcalid/STM32-car-MPU6050-Bluetooth-Ultrason](https://github.com/dyfcalid/STM32-car-MPU6050-Bluetooth-Ultrasonic) | 400 | F103 | 中文：MPU6050+蓝牙+超声波+触摸屏+电机的小车 | 现成硬件清单，直接复刻答辩用 |
| [Nolimy/steeringWheel_MeterBox_STM32_FreeRTOS](https://github.com/Nolimy/steeringWheel_MeterBox_STM32_FreeRTOS) | 166 | F4 | 大学生方程式赛车方向盘仪表盒，FreeRTOS 多任务 | 「多任务 + CAN + 屏显」三件套，非常适合作为简历项目 |
| [simplefoc/Arduino-FOC-balancer](https://github.com/simplefoc/Arduino-FOC-balancer) | 278 | 全系 | 无刷云台电机两轮自平衡机器人（模块化） | 平衡车/球板经典毕设 |

### 5.2 电机控制（无刷 FOC / 步进）

| 项目 | ★ | 芯片 | 说明 |
|---|---|---|---|
| [simplefoc/Arduino-FOC](https://github.com/simplefoc/Arduino-FOC) | 3097 | F1/F4/L4 | 开源 FOC 库，支持编码器/霍尔/无感，文档极好，20 天能做出转动演示 |
| [simplefoc/Arduino-SimpleFOCShield](https://github.com/simplefoc/Arduino-SimpleFOCShield) | 634 | — | 配套驱动板（可直接买板/打板） |
| [lxcy-tiger/FOC-Sensorless-EKF-STM32F103C8T6-FixedPoint](https://github.com/lxcy-tiger/FOC-Sensorless-EKF-STM32F103C8T6-FixedPoint) | 9 | F103 | 中文：EKF 无感观测器 FOC，配 X-NUCLEO-IHM07M1 |
| [lxcy-tiger/FOC-Sensorless-EKF-STM32G474](https://github.com/lxcy-tiger/FOC-Sensorless-EKF-STM32G474) | 40 | G4 | 同上，EKF/滑模/非线性磁链三种观测器对比，适合做算法课设 |

### 5.3 CNC / 3D 打印 / 运动控制

| 项目 | ★ | 芯片 | 说明 |
|---|---|---|---|
| [MarlinFirmware/Marlin](https://github.com/MarlinFirmware/Marlin) | 17653 | F1/F4/L4 | 3D 打印机固件，`Marlin/src/HAL/STM32` 是优秀硬件抽象层教材 |
| [Paciente8159/uCNC](https://github.com/Paciente8159/uCNC) | 461 | F1/F4/L4 | 通用 CNC 固件，单文件配置，跑在 BluePill 上就能动三轴 |
| [Schildkroet/GRBL-Advanced](https://github.com/Schildkroet/GRBL-Advanced) | 300 | F4 | GRBL 的 32 位重写，带 USB/以太网，源码干净 |
| [thomast777/grbl32](https://github.com/thomast777/grbl32) | 226 | F103/F4 | GRBL 1.1 移植到 STM32，代码量小，适合「读懂一个真实固件」 |

### 5.4 仪器仪表 / 小工具（成本低、演示效果好）

| 项目 | ★ | 芯片 | 说明 |
|---|---|---|---|
| [thanks4opensource/buck50](https://github.com/thanks4opensource/buck50) | 637 | F103 | 逻辑分析仪 + 示波器 + 信号发生器三合一，BluePill 改造 |
| [parezj/EMBO](https://github.com/parezj/EMBO) | 393 | F1/F4 | 「6 美元的示波器」：示波器/逻辑分析仪/万用表，开源 PCB |
| [keshikan/CurematicCaliper](https://github.com/keshikan/CurematicCaliper) | 26 | L4 | 数显卡尺/直线编码器读数，电容编码原理，做工控课题很亮 |
| [frisnit/STM32L476-radar](https://github.com/frisnit/STM32L476-radar) | 45 | L476 | 多普勒测速雷达（Discovery 板 + 微波模块），L4 上的 FFT 实战 |
| [iliasam/STM32F4_UVC_Camera](https://github.com/iliasam/STM32F4_UVC_Camera) | 258 | F4 | USB UVC 免驱摄像头 + 麦克风，把 F4 变成摄像头 |
| [openmv/openmv](https://github.com/openmv/openmv) | 2895 | F4/F7/H7 | 机器视觉模块固件（找色块/二维码/人脸），竞赛视觉方案首选 |

### 5.5 低功耗 / 可穿戴（L4 的主场）

| 项目 | ★ | 芯片 | 说明 |
|---|---|---|---|
| [RT-Thread/IoT_Board](https://github.com/RT-Thread/IoT_Board) | 378 | L4 | 官方 IoT 开发板全套例程（WiFi/传感器/LCD/音频），国产 OS + L4 组合 |
| [junhua-best/H-Watch](https://github.com/junhua-best/H-Watch) | 64 | L4 | 中文：低功耗智能手表，休眠/唤醒/功耗预算写得清楚 |
| [Spectrewolf777/Stm32l4-Watch](https://github.com/Spectrewolf777/Stm32l4-Watch) | 35 | L4P5 | TinyUSB + GUI 的开源手表，仍在更新 |
| [stm32duino/STM32LowPower](https://github.com/stm32duino/STM32LowPower) | 226 | 全系 | 休眠/唤醒 API 封装，几十行就能量出 STOP2 的微安级电流 |
| [akospasztor/stm32-rtc-scheduler](https://github.com/akospasztor/stm32-rtc-scheduler) | 14 | L4 | RTC 超低功耗任务调度器，做「电池跑一年」类课题的现成框架 |
| [frisnit/STM32L476-radar](https://github.com/frisnit/STM32L476-radar) | 45 | L476 | 见上，低功耗 + 信号处理 |

### 5.6 物联网 / 智能家居（课设重灾区，挑一个改出差异）

| 项目 | ★ | 芯片 | 说明 |
|---|---|---|---|
| [kevinlq/SmartHome-Qt](https://github.com/kevinlq/SmartHome-Qt) | 718 | 全系 | 中文：Zigbee + STM32 + Qt 上位机，架构完整，能直接讲清「三层结构」 |
| [YoM-lab/SmartHomeDemo](https://github.com/YoM-lab/SmartHomeDemo) | 119 | 全系 | STM32 + ESP8266 + 微信小程序 + MQTT，演示链路完整 |
| [zthxxx/STM32-Contiki_Sensor_Smart_Home](https://github.com/zthxxx/STM32-Contiki_Sensor_Smart_Home) | 56 | F1 | 2016 TI 杯四川省一等奖，Contiki 系统 + 传感器组网 |
| [jackmachen/SmartHomeSTM32](https://github.com/jackmachen/SmartHomeSTM32) | 142 | 全系 | 中文：贝壳物联 + DHT11 + 烟雾/红外传感器 |
| [bookshiyi/SmartHome_stm32](https://github.com/bookshiyi/SmartHome_stm32) | 56 | 全系 | 机智云平台接入，云端配置步骤齐全 |
| [kastaineibum/STM32F4SensorHub](https://github.com/kastaineibum/STM32F4SensorHub) | 17 | F407 | 中文：F407 SensorHub，多传感器 + FreeRTOS + CubeMX |
| [TsingWei/stm32_iot_light_sensor](https://github.com/TsingWei/stm32_iot_light_sensor) | 49 | 全系 | HAL + ESP8266 + BH1750 + MQTT 智能街灯 |
| [lovelyterry/SmartSpeaker](https://github.com/lovelyterry/SmartSpeaker) | 314 | F407 | 中文：云端语音识别智能音箱（F407 + WM8978 + ESP8266） |

### 5.7 USB / 免驱 / 工具固件（小而完整，适合做「产品感」项目）

| 项目 | ★ | 芯片 | 说明 |
|---|---|---|---|
| [FreeJoy-Team/FreeJoy](https://github.com/FreeJoy-Team/FreeJoy) | 1052 | F103 | 把 STM32 变成可配置 HID 游戏控制器（轴/按键/编码器），配置工具齐全 |
| [Serasidis/STM32_HID_Bootloader](https://github.com/Serasidis/STM32_HID_Bootloader) | 528 | F10x | 免驱 USB HID 下载器，理解 Bootloader 跳转的最佳样本 |
| [rogerclarkmelbourne/STM32duino-bootloader](https://github.com/rogerclarkmelbourne/STM32duino-bootloader) | 1091 | F103 | BluePill 的 DFU bootloader，4KB 讲清「上电去哪」 |
| [RadioOperator/STM32F103C8T6_CMSIS-DAP_SWO](https://github.com/RadioOperator/STM32F103C8T6_CMSIS-DAP_SWO) | 450 | F103 | 15 元自制 CMSIS-DAP 调试器（带 SWO 串口），省下 ST-Link 的钱 |
| [ARMmbed/DAPLink](https://github.com/ARMmbed/DAPLink) | 2844 | F1/F4 | 官方 DAPLink 固件，调试器实现原理 |
| [blackmagic-debug/blackmagic](https://github.com/blackmagic-debug/blackmagic) | 3716 | F1/F4 | Black Magic Probe，GDB 直连调试，无 IDE 工作流 |

### 5.8 Bootloader / OTA（毕设高频考点）

| 项目 | ★ | 芯片 | 说明 |
|---|---|---|---|
| [akospasztor/stm32-bootloader](https://github.com/akospasztor/stm32-bootloader) | 1076 | F4/L4 | 可配置 Bootloader（UART/CAN/USB + CRC + 双分区），文档一流 |
| [Ferenc-nemeth/stm32-bootloader](https://github.com/Ferenc-nemeth/stm32-bootloader) | 436 | F1/F4 | 最小 UART bootloader，200 行看懂升级流程 |
| [viktorvano/STM32-Bootloader](https://github.com/viktorvano/STM32-Bootloader) | 316 | F4 | 双 App 互跳（A/B 分区）示例 |

---

## 6. 进阶：RTOS 与「工业级」框架（学有余力 / 做创新点）

| 项目 | ★ | 说明 |
|---|---|---|
| [RT-Thread/rt-thread](https://github.com/RT-Thread/rt-thread) | 12331 | 国产 RTOS，`bsp/stm32` 覆盖 F1/F4/L4，文档中文，国内就业加分 |
| [FreeRTOS/FreeRTOS-Kernel](https://github.com/FreeRTOS/FreeRTOS-Kernel) | 4642 | 内核本体，配合上面中文教程读源码 |
| [zephyrproject-rtos/zephyr](https://github.com/zephyrproject-rtos/zephyr) | 17034 | 工业级 RTOS + 设备树 + 统一驱动模型，大厂在用（克隆 1GB，慎下） |
| [libopencm3/libopencm3](https://github.com/libopencm3/libopencm3) | 3674 | 轻量开源外设库，摆脱 ST 库依赖、真正看懂寄存器 |
| [ChibiOS/ChibiOS](https://github.com/ChibiOS/ChibiOS) | 874 | RTOS + HAL 二合一，实时性极强 |
| [alejoseb/Modbus-STM32-HAL-FreeRTOS](https://github.com/alejoseb/Modbus-STM32-HAL-FreeRTOS) | 851 | 工业通信必备：Modbus RTU/TCP 主从机，简历关键词 |
| [stm32-rs/stm32f1xx-hal](https://github.com/stm32-rs/stm32f1xx-hal) · [stm32f4xx-hal](https://github.com/stm32-rs/stm32f4xx-hal) | 664 / 703 | Rust 嵌入式（embedded-hal），想学新语言可以拿 F1 做实验 |
| [rusefi/rusefi](https://github.com/rusefi/rusefi) | 1207 | 开源发动机 ECU（F4），「真实工业级代码」阅读材料，仓库 1.6GB 慎下 |

---

## 7. 怎么把「抄一个项目」变成「自己的项目」

1. **换主控不换功能**：把 F103 的课设搬到 L476，写清「低功耗模式下电流从 28mA 降到 45µA」——这就是创新点。
2. **加一维数据**：传感器项目加 SD 卡日志 + Python 画图；本来只有串口打印的，加上位机。
3. **做对比实验**：同一算法跑 SPL / HAL / LL 三版，量代码体积、执行时间、功耗，出一张表——答辩非常吃这套。
4. **拆一个真实固件**：拿 `grbl32` 或 `buck50`，画出它的任务/中断时序图，改一处功能并验证。比从零写一个玩具项目有说服力。
5. **硬件也自己动**：这些仓库多含 KiCad/立创 EDA 工程，打板一次成本 < ¥50，能讲「从原理图到固件」。

### 推荐组合（三个难度档）

| 档位 | 组合 | 周期 | 亮点 |
|---|---|---|---|
| 入门（大二） | BluePill + `stm32f103-keil` + SSD1306 + DHT11 | 3~4 周 | 外设全通，能讲清 I2C/SPI 时序 |
| 中等（大三/电赛） | NUCLEO-L476RG + FreeRTOS 中文教程 + `stm32-rtc-scheduler` + LoRa/NB-IoT | 6~8 周 | 低功耗 + RTOS + 无线，三件套齐全 |
| 拔高（毕设） | F407 板 + `betaflight` 姿态部分 / `SimpleFOC` 无感驱动 / `akospasztor/stm32-bootloader` OTA | 10~12 周 | 有算法、有协议、有可靠性设计 |

---

## 8. 硬件与工具最小清单

| 用途 | 推荐 | 价格 |
|---|---|---|
| F1 入门 | STM32F103C8T6 BluePill + ST-Link V2 | ¥15 + ¥15 |
| F4 主力 | STM32F407VET6 核心板 或 F4-Discovery | ¥60~200 |
| L4 低功耗 | NUCLEO-L476RG（板载 ST-Link，官方例程直接跑） | ¥90~120 |
| 调试器 | 自制 CMSIS-DAP（见 5.7）或 ST-Link V3 MINI | ¥15~120 |
| 电流测量 | INA219 模块 / 万用表 µA 档 | ¥15 |
| 逻辑分析 | `buck50`（自制）或 ¥30 的 8 通道分析仪 | ¥30 |

---

## 9. 数据说明与免责

- 星数/更新时间为 2026-11-08 抓取快照，会随时间变化。
- 仓库体积差异巨大（`stm32ai-modelzoo` 4.2GB、`rusefi` 1.6GB、`STM32CubeL4` 334MB），克隆前先看 README 和 release，优先 `--depth 1`。
- 部分中文项目是学生毕设代码，工程规范参差：**当作参考实现，不要当作工程范本**。
- 引用他人代码/硬件设计进论文或答辩材料，请遵守仓库 LICENSE 并注明出处。
