from .najia import Najia

# 延迟导入 diagnose_health，避免循环导入
def get_diagnose_health():
    try:
        from .diagnosis import diagnose_health
        return diagnose_health
    except Exception as e:
        print(f"Failed to import diagnose_health: {e}")
        raise

__all__ = ['Najia', 'get_diagnose_health']