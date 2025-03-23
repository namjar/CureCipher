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
        根据IP地址获取经纬度，优先使用离线DB-IP数据库，失败则尝试在线API
        
        参数:
            ip (str, optional): 用户IP地址，默认None（自动获取）
            
        返回:
            Tuple[float, float]: 经度（longitude），纬度（latitude）
        """
        # 如果未提供IP，先尝试使用默认IP
        if ip is None:
            # 使用一些中国的常见IP作为默认
            default_ips = ["1.2.4.8", "114.114.114.114", "223.5.5.5", "220.181.38.148"]
            
            # 首先尝试通过离线库使用默认IP查询
            for default_ip in default_ips:
                location = self._query_offline_db(default_ip)
                if location:
                    print(f"使用默认IP {default_ip} 成功获取位置")
                    return location
            
            # 离线查询失败，尝试在线获取IP
            ip = self._get_public_ip()
            
            # 如果在线获取也失败，使用默认值
            if ip is None:
                print(f"无法获取IP，使用默认北京经纬度: {self.default_lon}, {self.default_lat}")
                return self.default_lon, self.default_lat
        
        # 首先尝试使用离线数据库
        location = self._query_offline_db(ip)
        if location:
            return location
        
        # 离线库查询失败，尝试在线API
        location = self._query_online_api(ip)
        if location:
            return location
        
        # 所有方法均失败，使用默认值
        print(f"所有定位方法均失败，使用默认北京经纬度: {self.default_lon}, {self.default_lat}")
        return self.default_lon, self.default_lat
    
    def _get_public_ip(self) -> Optional[str]:
        """
        获取本机公网IP
        
        返回:
            Optional[str]: IP地址，失败则返回None
        """
        # 设置请求头，模拟浏览器
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        }
        
        # 尝试多个IP获取服务
        ip_apis = [
            "https://api.ipify.org",
            "https://ifconfig.me/ip",
            "https://ipinfo.io/ip"
        ]
        
        for api in ip_apis:
            try:
                print(f"尝试通过 {api} 获取公网IP...")
                response = requests.get(api, headers=headers, timeout=3)
                response.raise_for_status()
                ip = response.text.strip()
                print(f"成功获取公网IP: {ip}")
                return ip
            except Exception as e:
                print(f"通过 {api} 获取IP失败: {e}")
                continue
        
        print("所有获取IP的方法均失败")
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
                longitude = result["location"]["longitude"]
                latitude = result["location"]["latitude"]
                print(f"离线数据库查询成功: 经度={longitude}, 纬度={latitude}")
                return longitude, latitude
            print(f"IP {ip} 未在离线数据库中找到位置信息")
            return None
        except Exception as e:
            print(f"离线数据库查询异常: {e}")
            return None
    
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
        
        try:
            print(f"尝试使用在线API查询IP位置: {ip}")
            response = requests.get(f"https://ip-api.com/json/{ip}", headers=headers, timeout=5)
            response.raise_for_status()
            data = response.json()
            if data["status"] == "success":
                longitude = data["lon"]
                latitude = data["lat"]
                print(f"在线API查询成功: 经度={longitude}, 纬度={latitude}")
                return longitude, latitude
            print(f"在线API查询失败: {data.get('message', '未知错误')}")
            return None
        except Exception as e:
            print(f"在线API查询异常: {e}")
            return None

# 单例模式，导出一个实例
location_service = LocationService()
