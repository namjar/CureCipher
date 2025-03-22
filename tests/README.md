# /Users/ericw/Documents/GitHub/CureCipher/tests/README.md
# 八字排盘功能测试

本目录包含用于测试八字排盘功能的各类测试脚本。

## 目录结构

- `unit/`: 单元测试，测试各个独立函数
- `integration/`: 集成测试，测试完整计算流程
- `validation/`: 验证测试，与已知结果对比验证
- `performance/`: 性能测试，确保计算效率
- `edge_cases/`: 边界情况测试，测试各种异常输入
- `cli/`: 命令行工具，包含交互式测试

## 运行测试

### 运行所有测试

```bash
cd tests
python run_tests.py