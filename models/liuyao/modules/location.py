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
            # 默认指向固定的IP地理位置库文件
            self.dbip_path = "/Users/ericw/Documents/GitHub/CureCipher/data/dbip-city-lite-2025-03.mmdb"
        else:
            self.dbip_path = dbip_path
        
        # 加载DB-IP Lite数据库
        self.dbip_reader = self._load_dbip_data()
        
        # 默认经纬度（中国北京）
        self.default_lon = 116.4
        self.default_lat = 39.9
        
        # 加州经纬度（旧金山）
        self.california_lon = -122.4194
        self.california_lat = 37.7749
        
        # 加州IP地址列表
        self.california_ips = [
            "104.16.182.15",  # Cloudflare (加州)
            "157.240.11.35",  # Facebook (加州)
            "172.217.6.78",   # Google (加州)
            "199.232.36.133"  # GitHub (加州)
        ]
    
    def _load_dbip_data(self):
        """
        加载DB-IP Lite数据库（MMDB格式）
        
        返回:
            maxminddb.Reader: MMDB数据库读取器
        """
        try:
            print(f"尝试加载IP地理位置库: {self.dbip_path}")
            reader = maxminddb.open_database(self.dbip_path)
            print("IP地理位置库加载成功")
            return reader
        except Exception as e:
            print(f"加载DB-IP数据库失败: {e}")
            return None
    
    def get_location_from_ip(self, ip: Optional[str] = None) -> Tuple[float, float]:
        """
        根据IP地址获取经纬度，优先在线API，失败则用离线DB-IP数据库
        
        参数:
            ip (str, optional): 用户IP地址，默认None（使用加州IP）
            
        返回:
            Tuple[float, float]: 经度（longitude），纬度（latitude）
        """
        # 如果未提供IP，使用加州IP
        if ip is None:
            for california_ip in self.california_ips:
                # 优先尝试使用在线API查询加州IP
                location = self._query_online_api(california_ip)
                if location:
                    print(f"使用加州IP {california_ip} 成功获取位置")
                    return location
                
                # 如果在线API失败，尝试离线数据库
                location = self._query_offline_db(california_ip)
                if location:
                    print(f"使用离线数据库查询加州IP {california_ip} 成功")
                    return location
            
            # 所有加州IP都查询失败，返回默认加州坐标
            print(f"所有加州IP查询失败，使用默认加州经纬度: {self.california_lon}, {self.california_lat}")
            return self.california_lon, self.california_lat
        
        # 提供了IP，优先使用在线API
        location = self._query_online_api(ip)
        if location:
            return location
        
        # 在线API失败，尝试离线数据库
        location = self._query_offline_db(ip)
        if location:
            return location
        
        # 所有方法均失败，根据IP地址特征选择默认值
        if any(ip.startswith(prefix) for prefix in ["192.168.", "10.", "172."]):
            # 内网IP，默认使用北京经纬度
            print(f"检测到内网IP，使用默认北京经纬度: {self.default_lon}, {self.default_lat}")
            return self.default_lon, self.default_lat
        else:
            # 其他情况，使用加州经纬度
            print(f"无法定位IP，使用默认加州经纬度: {self.california_lon}, {self.california_lat}")
            return self.california_lon, self.california_lat
    
    def _query_online_api(self, ip: str) -> Optional[Tuple[float, float]]:
        """
        使用在线API查询IP位置
        
        参数:
            ip (str): IP地址
            
        返回:
            Optional[Tuple[float, float]]: 经纬度，失败则返回None
        """
        # 设置请求头，模拟浏览器
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        }
        
        # 尝试多个在线API服务
        api_services = [
            {
                "url": f"https://ip-api.com/json/{ip}",
                "timeout": 5,
                "parser": lambda data: (data.get("lon"), data.get("lat")) if data.get("status") == "success" else None
            },
            {
                "url": f"https://ipapi.co/{ip}/json/",
                "timeout": 5,
                "parser": lambda data: (data.get("longitude"), data.get("latitude")) if "longitude" in data and "latitude" in data else None
            },
            {
                "url": f"https://ipinfo.io/{ip}/json",
                "timeout": 5,
                "parser": lambda data: tuple(map(float, data.get("loc", "0,0").split(","))) if "loc" in data else None
            }
        ]
        
        for api in api_services:
            try:
                print(f"尝试使用在线API查询IP位置: {ip} (API: {api['url']})")
                response = requests.get(api["url"], headers=headers, timeout=api["timeout"])
                response.raise_for_status()
                data = response.json()
                
                location = api["parser"](data)
                if location and location[0] is not None and location[1] is not None:
                    print(f"在线API查询成功: 经度={location[0]}, 纬度={location[1]}")
                    return location
                
                print(f"在线API返回的数据不包含有效的经纬度")
            except Exception as e:
                print(f"在线API查询异常: {e}")
                continue
        
        print("所有在线API查询均失败")
        return None
    
    def _query_offline_db(self, ip: str) -> Optional[Tuple[float, float]]:
        """
        使用离线数据库查询IP位置
        
        参数:
            ip (str): IP地址
            
        返回:
            Optional[Tuple[float, float]]: 经纬度，失败则返回None
        """
        if not self.dbip_reader:
            print("离线数据库不可用")
            return None
        
        try:
            print(f"使用离线数据库查询IP: {ip}")
            result = self.dbip_reader.get(ip)
            if result and "location" in result:
                longitude = result["location"].get("longitude")
                latitude = result["location"].get("latitude")
                
                if longitude is not None and latitude is not None:
                    print(f"离线数据库查询成功: 经度={longitude}, 纬度={latitude}")
                    return longitude, latitude
                    
            print(f"IP {ip} 未在离线数据库中找到有效的位置信息")
            return None
        except Exception as e:
            print(f"离线数据库查询异常: {e}")
            return None

# 单例模式，导出一个实例
location_service = LocationService()
