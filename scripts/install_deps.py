"""
依赖安装脚本

自动安装CureCipher项目所需的所有依赖
"""

import sys
import subprocess
import os
from pathlib import Path

def install_requirements():
    """安装requirements.txt中的所有依赖"""
    print("开始安装CureCipher项目依赖...")
    
    # 获取项目根目录
    project_root = Path(__file__).parent.parent
    requirements_file = project_root / "requirements.txt"
    
    if not requirements_file.exists():
        print(f"错误: 找不到requirements.txt文件，请确保文件位于{requirements_file}")
        return False
    
    try:
        # 执行pip安装命令
        cmd = [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)]
        print(f"执行命令: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("所有依赖安装成功!")
            return True
        else:
            print(f"安装依赖时出错:\n{result.stderr}")
            return False
    
    except Exception as e:
        print(f"执行安装命令时出错: {e}")
        return False

def check_dependencies():
    """检查关键依赖是否已安装"""
    required_packages = [
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "lunar_python",
        "geopy",
        "requests"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"以下关键依赖尚未安装: {', '.join(missing_packages)}")
        return False
    else:
        print("所有关键依赖已安装!")
        return True

if __name__ == "__main__":
    print("CureCipher项目依赖安装工具")
    print("=" * 50)
    
    # 检查依赖
    if check_dependencies():
        print("\n所有依赖已安装，无需再次安装。")
        choice = input("是否仍要强制重新安装所有依赖? (y/N): ")
        if choice.lower() != 'y':
            print("安装操作已取消。")
            sys.exit(0)
    
    # 安装依赖
    success = install_requirements()
    
    if success:
        print("\n依赖安装成功! 现在可以运行CureCipher项目了。")
    else:
        print("\n依赖安装失败。请检查错误信息并手动安装依赖。")
        print("可以尝试手动运行以下命令:")
        print(f"  pip install -r {Path(__file__).parent.parent / 'requirements.txt'}")
