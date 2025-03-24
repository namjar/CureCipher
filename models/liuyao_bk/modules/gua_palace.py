"""
卦宫与卦型处理模块 - 识别卦宫、卦型和相关信息
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

# 添加项目根目录到路径
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

# 导入八宫卦数据
from models.liuyao.data.bagong_data import (
    BAGONG_GUA_DATA, 
    GUA_WUXING_MAP, 
    GUA_SHI,
    LIUQIN_DATA,
    LIUSHEN_DATA,
    WUXING_DATA
)

class GuaPalace:
    """卦宫与卦型处理类"""
    
    def __init__(self):
        """初始化方法"""
        self.palace_data = BAGONG_GUA_DATA
        self.gua_wuxing = GUA_WUXING_MAP
        self.shi_ying_data = GUA_SHI
        
        # 用于快速查找卦的字典
        self.gua_dict = {}
        self._initialize_gua_dict()
    
    def _initialize_gua_dict(self):
        """初始化卦字典，用于快速查找卦信息"""
        for palace_name, guas in self.palace_data.items():
            for gua in guas:
                gua_key = self._yao_array_to_key(gua["yao_array"])
                gua_info = gua.copy()
                gua_info["palace"] = palace_name
                gua_info["wuxing"] = self.gua_wuxing.get(palace_name, "")
                # 添加世应爻信息
                for shi_ying_item in self.shi_ying_data.get(palace_name, []):
                    if shi_ying_item["gua_type"] == gua["gua_type"]:
                        gua_info["shi_yao"] = shi_ying_item["shi_yao"]
                        gua_info["ying_yao"] = shi_ying_item["ying_yao"]
                        break
                
                self.gua_dict[gua_key] = gua_info
                # 同时以卦名为键添加
                self.gua_dict[gua["name"]] = gua_info
                # 以简称作为键添加
                if "alias" in gua and gua["alias"]:
                    self.gua_dict[gua["alias"]] = gua_info
    
    def _yao_array_to_key(self, yao_array: List[int]) -> str:
        """
        将爻数组转换为字符串键，用于字典查找
        
        参数:
            yao_array (List[int]): 爻数组
            
        返回:
            str: 字符串键
        """
        return ''.join(map(str, yao_array))
    
    def get_gua_info(self, yao_array: List[int] = None, gua_name: str = None) -> Dict:
        """
        根据爻数组或卦名获取卦信息
        
        参数:
            yao_array (List[int], optional): 爻数组
            gua_name (str, optional): 卦名
            
        返回:
            Dict: 卦信息
        """
        if yao_array is not None:
            key = self._yao_array_to_key(yao_array)
            return self.gua_dict.get(key, {})
        
        if gua_name is not None:
            return self.gua_dict.get(gua_name, {})
        
        return {}
    
    def identify_gua_palace_type(self, yao_array: List[int]) -> Tuple[str, str, Dict]:
        """
        识别卦的宫位和卦型
        
        参数:
            yao_array (List[int]): 爻数组
            
        返回:
            Tuple[str, str, Dict]: 卦宫名称，卦型，完整卦信息
        """
        gua_info = self.get_gua_info(yao_array)
        
        # 如果找不到对应的卦，返回空信息
        if not gua_info:
            return "未知", "未知", {}
        
        palace = gua_info.get("palace", "未知")
        gua_type = gua_info.get("gua_type", "未知")
        
        # 修正卦宫名称格式
        if palace.endswith("宫宫"):
            palace = palace[:-1]
        elif not palace.endswith("宫"):
            palace = palace + "宫"
        
        return palace, gua_type, gua_info
    
    def get_gua_palace_types(self) -> Dict[str, List[str]]:
        """
        获取所有卦宫及其包含的卦型列表
        
        返回:
            Dict[str, List[str]]: 卦宫及卦型列表
        """
        result = {}
        for palace_name, guas in self.palace_data.items():
            gua_names = [gua["name"] for gua in guas]
            result[palace_name] = gua_names
        
        return result
    
    def get_gua_wuxing(self, palace_name: str) -> str:
        """
        获取卦宫的五行属性
        
        参数:
            palace_name (str): 卦宫名称
            
        返回:
            str: 五行属性
        """
        return self.gua_wuxing.get(palace_name, "")
    
    def get_shi_ying_positions(self, palace_name: str, gua_type: str) -> Tuple[int, int]:
        """
        获取特定卦宫和卦型的世应爻位置
        
        参数:
            palace_name (str): 卦宫名称
            gua_type (str): 卦型
            
        返回:
            Tuple[int, int]: 世爻位置，应爻位置
        """
        shi_ying_list = self.shi_ying_data.get(palace_name, [])
        
        for item in shi_ying_list:
            if item["gua_type"] == gua_type:
                return item["shi_yao"], item["ying_yao"]
        
        # 默认返回第6爻和第3爻
        return 6, 3
    
    def get_all_palaces(self) -> List[str]:
        """
        获取所有卦宫名称
        
        返回:
            List[str]: 卦宫名称列表
        """
        return list(self.palace_data.keys())
    
    def get_gua_by_palace_and_type(self, palace_name: str, gua_type: str) -> Dict:
        """
        根据卦宫和卦型获取卦信息
        
        参数:
            palace_name (str): 卦宫名称
            gua_type (str): 卦型
            
        返回:
            Dict: 卦信息
        """
        guas = self.palace_data.get(palace_name, [])
        
        for gua in guas:
            if gua["gua_type"] == gua_type:
                gua_info = gua.copy()
                gua_info["palace"] = palace_name
                gua_info["wuxing"] = self.gua_wuxing.get(palace_name, "")
                
                # 添加世应爻信息
                shi_yao, ying_yao = self.get_shi_ying_positions(palace_name, gua_type)
                gua_info["shi_yao"] = shi_yao
                gua_info["ying_yao"] = ying_yao
                
                return gua_info
        
        return {}
    
    def get_palace_diagram(self, palace_name: str) -> str:
        """
        生成卦宫图形，显示本宫八卦
        
        参数:
            palace_name (str): 卦宫名称
            
        返回:
            str: 卦宫图形字符串
        """
        # 修正卦宫名称中的重复问题
        if palace_name.endswith("宫宫"):
            palace_name = palace_name[:-1]
        elif not palace_name.endswith("宫"):
            palace_name = palace_name + "宫"
            
        # 检查是否存在卦宫数据
        search_name = palace_name
        if search_name.endswith("宫"):
            search_name = search_name[:-1]
            
        if search_name not in self.palace_data:
            return f"未找到 {palace_name} 的信息"
        
        guas = self.palace_data[search_name]
        
        # 提取各卦名称
        gua_names = [gua["name"] for gua in guas]
        gua_types = [gua["gua_type"] for gua in guas]
        
        # 生成卦宫图形
        diagram = f"{palace_name}八卦图:\n"
        diagram += f"本宫卦({gua_types[0]}): {gua_names[0]}\n"
        diagram += f"游魂卦({gua_types[6]}): {gua_names[6]}\n"
        diagram += f"归魂卦({gua_types[7]}): {gua_names[7]}\n"
        diagram += "\n一世卦至五世卦:\n"
        for i in range(1, 6):
            diagram += f"{i}世卦({gua_types[i]}): {gua_names[i]}\n"
        
        return diagram
    
    def generate_all_bagong_text(self) -> str:
        """
        生成所有八宫卦的文本描述
        
        返回:
            str: 八宫卦文本描述
        """
        result = "八宫卦表:\n\n"
        
        for palace_name, guas in self.palace_data.items():
            gua_names = [gua["name"] for gua in guas]
            result += f"{palace_name}八卦: {gua_names[0]}，{gua_names[1]}，{gua_names[2]}，{gua_names[3]}，{gua_names[4]}，{gua_names[5]}，{gua_names[6]}，{gua_names[7]}\n"
        
        return result

# 导出单例实例
gua_palace = GuaPalace()
