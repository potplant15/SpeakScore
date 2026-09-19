# Development Log

## DAY1 / 9.17

- 创建 SpeakScore 项目仓库。
- 完成 TTS Service 基础功能：FastAPI、gTTS、健康检查和语音生成接口。
- 配置项目级和 TTS Service 级运行依赖、开发依赖。
- 添加 pytest 测试，测试结果为 3 passed。
- 添加 Dockerfile。
- 添加 GitHub Actions，完成 Docker 构建和接口测试。

当前进度：TTS Service 第一版开发完成，Docker 云端测试通过。

## DAY2 / 9.19

- 完成 Practice Service 第一版基础结构。
- 配置 Java 21、Spring Boot 3.5、Maven 和 MySQL 相关环境。
- 实现练习创建、查询、分页历史和标准音频接口。
- 接入 Reference Service 和 Evaluation Service。
- 实现练习状态管理、评分结果保存和 MySQL 持久化。
- 完成 Reference Service 改造，支持英音、美音以及不同性别声音选择。
- 更新 Reference Service 依赖和 Dockerfile，完成音频生成及 IPA 测试。
- 完成 Evaluation Service 改造，接入 OpenPronounce 进行发音评分。
- 完善 Evaluation Service 的音频识别、音素分析和评分结果返回。
- 配置 Maven 阿里云镜像并完成项目编译打包。

当前进度：Practice Service 基础功能完成，下一步进行三个服务的联调测试，并补充 Java 测试用例。
