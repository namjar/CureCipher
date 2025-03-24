"""
基础解释器接口
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class BaseInterpreter(ABC):
    """基础解释器接口类"""
    
    @abstractmethod
    def interpret(self, gua_result: Dict, day_master: Optional[str] = None, 
                 query_type: Optional[str] = None) -> str:
        """
        解释卦象
        
        参数:
            gua_result (Dict): 卦象计算结果
            day_master (str, optional): 日主天干
            query_type (str, optional): 测算类型(事业/财运/婚姻/健康等)
            
        返回:
            str: 解释结果
        """
        pass
