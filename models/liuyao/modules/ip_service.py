"""
IP服务模块 - 提供IP地址获取和位置查询功能
"""

import socket
import urllib.request
import urllib.error
import json
import time
import os
from typing import Dict, Tuple, Optional, List, Any

class IPService:
    """IP服务类，提供IP地址获取和位置查询功能"""
    
    def __init__(self, cache_dir: Optional[str] = None):
        """
        初始化IP服务
        
        参数:
            cache_dir (str, optional): 缓存目录，用于保存临时IP数据
        """
        # 缓存目录
        self.cache_dir = cache_dir or os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # 缓存文件
        self.ip_cache_file = os.path.join(self.cache_dir, "ip_cache.json")
        
        # 初始化缓存
        self.ip_cache = self._load_cache()
        
        # 可用的IP地址获取服务
        self.ip_services = [
            "https://api.ipify.org",
            "https://icanhazip.com",
            "https://ifconfig.me",
            "https://ident.me",
            "https://ipecho.net/plain"
        ]
        
        # 可用的地理位置查询服务
        self.geo_services = [
            {
                "url": "https://ip-api.com/json/{ip}",
                "parser": self._parse_ip_api,
                "timeout": 3
            },
            {
                "url": "https://ipapi.co/{ip}/json/",
                "parser": self._parse_ipapi_co,
                "timeout": 3
            },
            {
                "url": "https://ipinfo.io/{ip}/json",
                "parser": self._parse_ipinfo,
                "timeout": 3
            }
        ]
        
        # 默认位置 (如果所有方法都失败)
        self.default_location = {
            "city": "北京",
            "country": "中国",
            "region": "北京市",
            "longitude": 116.4,
            "latitude": 39.9
        }
    
    def _load_cache(self) -> Dict[str, Any]:
        """
        从缓存文件加载IP数据
        
        返回:
            Dict[str, Any]: 缓存的IP数据
        """
        try:
            if os.path.exists(self.ip_cache_file):
                with open(self.ip_cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return data
            return {}
        except Exception as e:
            print(f"加载IP缓存失败: {e}")
            return {}
    
    def _save_cache(self) -> None:
        """保存IP数据到缓存文件"""
        try:
            with open(self.ip_cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.ip_cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存IP缓存失败: {e}")
    
    def get_local_ip(self) -> str:
        """
        获取本地IP地址
        
        返回:
            str: 本地IP地址
        """
        try:
            # 建立一个临时连接来获取本地IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception as e:
            print(f"获取本地IP失败: {e}")
            return "127.0.0.1"
    
    def get_external_ip(self) -> str:
        """
        获取外部IP地址，尝试多个服务
        
        返回:
            str: 外部IP地址
        """
        # 首先检查缓存
        if "external_ip" in self.ip_cache:
            cache_time = self.ip_cache.get("external_ip_updated", 0)
            # 如果缓存不超过1小时，直接返回
            if time.time() - cache_time < 3600:
                return self.ip_cache["external_ip"]
        
        # 尝试从多个服务获取外部IP
        for service in self.ip_services:
            try:
                with urllib.request.urlopen(service, timeout=3) as response:
                    ip = response.read().decode('utf-8').strip()
                    if ip and self._is_valid_ip(ip):
                        # 更新缓存
                        self.ip_cache["external_ip"] = ip
                        self.ip_cache["external_ip_updated"] = time.time()
                        self._save_cache()
                        return ip
            except Exception as e:
                print(f"从服务 {service} 获取IP失败: {e}")
                continue
                
        # 如果所有服务都失败，返回本地IP
        return self.get_local_ip()
    
    def _is_valid_ip(self, ip: str) -> bool:
        """
        检查是否为有效的IP地址
        
        参数:
            ip (str): IP地址
            
        返回:
            bool: 是否有效
        """
        try:
            # 简单的IPv4格式检查
            parts = ip.split('.')
            if len(parts) != 4:
                return False
            for part in parts:
                if not part.isdigit() or int(part) < 0 or int(part) > 255:
                    return False
            return True
        except:
            return False
    
    def get_location_from_ip(self, ip: Optional[str] = None) -> Dict[str, Any]:
        """
        从IP地址获取地理位置
        
        参数:
            ip (str, optional): IP地址，为None则自动获取
            
        返回:
            Dict[str, Any]: 位置信息，包含经纬度、城市、国家等
        """
        # 如果未提供IP，则获取外部IP
        if ip is None:
            ip = self.get_external_ip()
            print(f"自动获取IP地址: {ip}")
        
        # 检查缓存
        cache_key = f"location_{ip}"
        if cache_key in self.ip_cache:
            cache_time = self.ip_cache.get(f"{cache_key}_updated", 0)
            # 缓存有效期为1天
            if time.time() - cache_time < 86400:
                return self.ip_cache[cache_key]
        
        # 尝试在线服务
        for service in self.geo_services:
            try:
                url = service["url"].format(ip=ip)
                parser = service["parser"]
                timeout = service["timeout"]
                
                print(f"尝试使用在线API查询IP位置: {ip} (API: {url})")
                with urllib.request.urlopen(url, timeout=timeout) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    location = parser(data)
                    
                    if location:
                        print(f"在线API查询成功: 经度={location['longitude']}, 纬度={location['latitude']}")
                        # 更新缓存
                        self.ip_cache[cache_key] = location
                        self.ip_cache[f"{cache_key}_updated"] = time.time()
                        self._save_cache()
                        return location
            except Exception as e:
                print(f"在线API查询异常: {e}")
                continue
        
        # 所有方法失败，返回默认位置
        print(f"所有位置查询方法失败，使用默认位置")
        return self.default_location
    
    def _parse_ip_api(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        解析ip-api.com的响应数据
        
        参数:
            data (Dict[str, Any]): 响应数据
            
        返回:
            Optional[Dict[str, Any]]: 解析后的位置信息
        """
        if data.get("status") != "success":
            return None
            
        return {
            "city": data.get("city", "未知城市"),
            "country": data.get("country", "未知国家"),
            "region": data.get("regionName", "未知地区"),
            "longitude": data.get("lon", 0.0),
            "latitude": data.get("lat", 0.0),
            "timezone": data.get("timezone", "")
        }
    
    def _parse_ipapi_co(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        解析ipapi.co的响应数据
        
        参数:
            data (Dict[str, Any]): 响应数据
            
        返回:
            Optional[Dict[str, Any]]: 解析后的位置信息
        """
        if "error" in data:
            return None
            
        return {
            "city": data.get("city", "未知城市"),
            "country": data.get("country_name", "未知国家"),
            "region": data.get("region", "未知地区"),
            "longitude": data.get("longitude", 0.0),
            "latitude": data.get("latitude", 0.0),
            "timezone": data.get("timezone", "")
        }
    
    def _parse_ipinfo(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        解析ipinfo.io的响应数据
        
        参数:
            data (Dict[str, Any]): 响应数据
            
        返回:
            Optional[Dict[str, Any]]: 解析后的位置信息
        """
        if "error" in data or "loc" not in data:
            return None
            
        # 从loc字段解析经纬度
        lat, lon = 0.0, 0.0
        try:
            lat_lon = data.get("loc", "0,0").split(",")
            lat = float(lat_lon[0])
            lon = float(lat_lon[1])
        except:
            pass
            
        return {
            "city": data.get("city", "未知城市"),
            "country": data.get("country", "未知国家"),
            "region": data.get("region", "未知地区"),
            "longitude": lon,
            "latitude": lat,
            "timezone": data.get("timezone", "")
        }
    
    def get_location_coordinates(self, ip: Optional[str] = None) -> Tuple[float, float]:
        """
        从IP地址获取经纬度坐标
        
        参数:
            ip (str, optional): IP地址，为None则自动获取
            
        返回:
            Tuple[float, float]: 经度, 纬度
        """
        location = self.get_location_from_ip(ip)
        return location["longitude"], location["latitude"]
    
    def get_formatted_location(self, ip: Optional[str] = None) -> str:
        """
        获取格式化的位置信息字符串
        
        参数:
            ip (str, optional): IP地址，为None则自动获取
            
        返回:
            str: 格式化的位置信息
        """
        location = self.get_location_from_ip(ip)
        
        city = location.get("city", "未知城市")
        country = location.get("country", "未知国家")
        region = location.get("region", "")
        
        if region and region != city:
            return f"{city}, {region}, {country}"
        else:
            return f"{city}, {country}"

# 导出单例实例
ip_service = IPService()
