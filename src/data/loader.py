import sys
from typing import Generator, Optional
from dataclasses import dataclass
from pathlib import Path

# 本地导入
from .proto import data_pb2

@dataclass
class DataLoaderConfig:
    """数据加载器配置"""
    batch_size: int = 32
    prefetch_factor: int = 2
    shuffle: bool = True
    drop_last: bool = False

class DataLoader:
    """数据加载器实现"""
    
    def __init__(self, config: DataLoaderConfig):
        self.config = config
        self._stream = None
        self._buffer = []
        
    def load_from_proto(self, proto_path: Path) -> Generator:
        """从proto文件加载数据"""
        if not proto_path.exists():
            raise FileNotFoundError(f"Proto file not found: {proto_path}")
            
        # 模拟proto数据解析
        batch = data_pb2.DataBatch()
        with open(proto_path, 'rb') as f:
            batch.ParseFromString(f.read())
            
        yield batch
        
    def stream_data(self, source: str) -> Generator:
        """流式数据加载"""
        # 模拟数据流处理
        for i in range(1000):
            batch = data_pb2.DataBatch()
            # 填充模拟数据
            yield batch
            
    def __del__(self):
        """析构函数 - 可能的内存泄漏点"""
        if hasattr(self, '_stream'):
            self._stream.close()
