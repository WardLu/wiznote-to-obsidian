# 离线授权集成测试实施计划

**状态**: 准备实施
**目标**: 为刚修复的 6 个离线授权问题添加集成测试

## 测试文件规划

### 1. test_offline_full_activation_flow.py
测试完整的离线激活流程（从 API 调用到缓存保存）

**测试用例**：
- `test_complete_offline_activation_workflow`: 完整激活流程（API → 数据库 → 缓存 → 验证）
- `test_activation_with_network_failure`: 网络失败时的激活流程

### 2. test_offline_degradation_flow.py
测试云端失败降级策略

**测试用例**：
- `test_cloud_to_offline_degradation`: 云端失败自动降级到离线
- `test_offline_to_cloud_recovery`: 离线恢复到在线同步

### 3. test_offline_persistence_flow.py
测试授权状态跨会话持久化

**测试用例**：
- `test_authorization_persists_across_restarts`: 授权状态跨重启保持
- `test_cache_expiry_handling`: 缓存过期处理流程

### 4. test_offline_reactivation_flow.py
测试重复激活和续期流程

**测试用例**：
- `test_same_device_reactivation`: 同设备重复激活（续期）
- `test_different_device_activation_blocked`: 不同设备激活被阻止

## 实施步骤

### Batch 1: 完整激活流程测试
1. 创建 `tests/integration/test_offline_full_activation_flow.py`
2. 实现 2 个测试用例
3. 运行测试验证

### Batch 2: 降级策略流程测试
1. 创建 `tests/integration/test_offline_degradation_flow.py`
2. 实现 2 个测试用例
3. 运行测试验证

### Batch 3: 持久化流程测试
1. 创建 `tests/integration/test_offline_persistence_flow.py`
2. 实现 2 个测试用例
3. 运行测试验证

### Batch 4: 重复激活流程测试
1. 创建 `tests/integration/test_offline_reactivation_flow.py`
2. 实现 2 个测试用例
3. 运行测试验证

### Batch 5: 完整测试和文档
1. 运行所有新增集成测试
2. 更新测试文档
3. 提交代码

## 技术要点

### 集成测试策略
- 使用真实的缓存管理器（临时目录）
- Mock Supabase 客户端（云端调用）
- 测试模块间协作（API + 数据库 + 缓存）

### 验证点
- 数据流完整性
- 模块间协作正确性
- 错误处理和降级策略
- 状态持久化

### 测试数据
- 使用 `LicenseBuilder` 创建测试数据
- 使用 `CacheHelper` 管理缓存
- 模拟真实使用场景
