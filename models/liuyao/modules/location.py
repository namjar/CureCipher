"""
位置模块 - 提供IP定位和经纬度获取功能
"""

import os
import time
import requests
import maxminddb
from pathlib import Path
from typing import Tuple, Optional

class LocationService:
    """位置服务类，提供IP定位功能"""
    
    def __init__(self, dbip_path: str = None):
        """
        初始化位置服务
        
        参数:
            dbip_path (str, optional): DB-IP Lite数据库路径
        """
        # 如果未提供路径，使用默认路径
        if dbip_path is None:
            root_dir = Path(__file__).parent.parent.parent.parent
            self.dbip_path = os.path.join(root_dir, "data", "dbip-city-lite-2025-03.mmdb")
        else:
            self.dbip_path = dbip_path
        
        # 加载DB-IP Lite数据库
        self.dbip_reader = self._load_dbip_data()
    
    def _load_dbip_data(self):
        """
        加载DB-IP Lite数据库（MMDB格式）
        
        返回:
            maxminddb.Reader: MMDB数据库读取器
        """
        try:
            return maxminddb.open_database(self.dbip_path)
        except Exception as e:
            print(f"加载DB-IP数据库失败: {e}")
            return None
    
    def get_location_from_ip(self, ip: Optional[str] = None) -> Tuple[float, float]:
        """
        根据IP地址获取经纬度，优先在线API，失败则用离线DB-IP数据库
        
        参数:
            ip (str, optional): 用户IP地址，默认None（自动获取）
            
        返回:
            Tuple[float, float]: 经度（longitude），纬度（latitude）
        """
        # 设置请求头，模拟浏览器
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        }

        # 如果未提供IP，获取本机公网IP
        if ip is None:
            try:
                response = requests.get("https://api.ipify.org", headers=headers, timeout=5)
                response.raise_for_status()
                ip = response.text
            except Exception as e:
                print(f"获取公网IP失败: {e}，尝试备用API")
                try:
                    response = requests.get("https://ifconfig.me/ip", headers=headers, timeout=5)
                    response.raise_for_status()
                    ip = response.text
                except Exception as e:
                    print(f"备用API失败: {e}，使用默认北美经纬度")
                    print("建议手动输入经纬度以提高真太阳时计算精度")
                    return -100, 40

        # 优先尝试在线API（ip-api.com）
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.get(f"https://ip-api.com/json/{ip}", headers=headers, timeout=5)
                response.raise_for_status()
                data = response.json()
                if data["status"] == "success":
                    return data["lon"], data["lat"]
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"在线API获取位置失败（尝试{max_retries}次）: {e}，尝试离线数据库")
                else:
                    print(f"在线API第{attempt+1}次尝试失败，等待1秒后重试...")
                    time.sleep(1)  # 增加重试间隔
                    continue

        # 在线失败，尝试离线DB-IP数据库（MMDB格式）
        if self.dbip_reader:
            try:
                result = self.dbip_reader.get(ip)
                if result and "location" in result:
                    return result["location"]["longitude"], result["location"]["latitude"]
                print(f"IP {ip} 未在DB-IP数据库中找到，使用默认北美经纬度")
            except Exception as e:
                print(f"离线数据库查询失败: {e}，使用默认北美经纬度")
        else:
            print("离线数据库不可用，使用默认北美经纬度")

        print("建议手动输入经纬度以提高真太阳时计算精度")
        return -100, 40  # 默认北美经纬度

# 单例模式，导出一个实例
location_service = LocationService()
