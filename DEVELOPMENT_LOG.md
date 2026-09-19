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

## DAY3 / 9.20

- 完成 Docker Compose 多服务部署配置和云服务器部署。
- 配置 MySQL、Kokoro 模型、Whisper 模型和 Hugging Face 缓存卷。
- 解决云服务器网络限制导致的 Kokoro、Whisper 和 OpenPronounce 模型下载失败问题。
- 完成 Kokoro 模型和 Whisper 模型的本地上传及容器挂载。
- 下载 OpenPronounce 所需的 Wav2Vec2 模型，并整理 Hugging Face 缓存目录结构。
- 配置 Evaluation Service 离线加载模型，避免运行时访问 Hugging Face。
- 修复前端 Nginx 代理和云端 API 访问问题。
- 使用 Cloudflare Quick Tunnel 提供 HTTPS 访问，使浏览器可以使用麦克风。
- 定位评分超时、Nginx 499 和模型缓存路径错误等部署问题。
- 创建完整错误日志，记录项目开发和部署过程中的问题及解决方法。

当前进度：项目已完成主要微服务和 Docker Compose 云端部署，当前重点是验证 OpenPronounce 离线模型缓存后的完整评分链路。

## DAY4 / 9.20

- 完成 `www.speakscore.icu` 的 DNS A 记录解析到云服务器。
- 使用 Certbot 为域名申请并部署 Let's Encrypt HTTPS 证书。
- 配置 Nginx 将 80/443 请求反向代理到前端容器 5173。
- 将前端、Reference Service、Evaluation Service、Practice Service 和 MySQL 的公网访问收敛到域名入口。
- 将 5173 改为仅监听服务器本机，关闭 8001、8002、8080 和 3306 的公网访问。
- 停止 Cloudflare Quick Tunnel，改用服务器 Nginx 和正式域名提供 HTTPS 访问。

当前进度：SpeakScore 已具备正式域名 HTTPS 访问入口，浏览器可通过域名安全使用麦克风；后续继续验证生产环境评分链路。
