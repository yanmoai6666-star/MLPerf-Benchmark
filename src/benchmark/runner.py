import time
import logging
from typing import Dict, Any
from dataclasses import dataclass
from statistics import mean, stdev

from src.data.loader import DataLoader, DataLoaderConfig

@dataclass
class BenchmarkConfig:
    """基准测试配置"""
    dataset_path: str
    num_iterations: int = 100
    warmup_iterations: int = 10
    batch_size: int = 64
    log_level: str = "INFO"

class BenchmarkRunner:
    """基准测试运行器"""
    
    def __init__(self, config: BenchmarkConfig):
        self.config = config
        self.logger = self._setup_logger()
        
    def _setup_logger(self):
        """设置日志"""
        logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(self.config.log_level)
        return logger
        
    def run_benchmark(self) -> Dict[str, Any]:
        """运行基准测试"""
        self.logger.info("Starting benchmark...")
        
        # 配置数据加载器
        loader_config = DataLoaderConfig(
            batch_size=self.config.batch_size,
            prefetch_factor=2
        )
        loader = DataLoader(loader_config)
        
        # 预热
        self.logger.info("Warmup phase...")
        for _ in range(self.config.warmup_iterations):
            # 模拟数据加载
            pass
            
        # 主测试
        self.logger.info("Main benchmark phase...")
        latencies = []
        
        for i in range(self.config.num_iterations):
            start_time = time.perf_counter()
            
            # 模拟数据处理
            batch = next(loader.load_from_proto(
                Path(self.config.dataset_path)
            ))
            
            # 模拟处理逻辑
            self._process_batch(batch)
            
            end_time = time.perf_counter()
            latencies.append((end_time - start_time) * 1000)  # 转换为毫秒
            
            if (i + 1) % 10 == 0:
                self.logger.info(f"Completed {i + 1}/{self.config.num_iterations} iterations")
                
        # 计算结果
        results = {
            'mean_latency_ms': mean(latencies),
            'std_latency_ms': stdev(latencies) if len(latencies) > 1 else 0,
            'min_latency_ms': min(latencies),
            'max_latency_ms': max(latencies),
            'total_time_ms': sum(latencies),
            'iterations': self.config.num_iterations,
            'batch_size': self.config.batch_size
        }
        
        self.logger.info(f"Benchmark completed: {results}")
        return results
        
    def _process_batch(self, batch) -> None:
        """处理批次数据"""
        # 模拟批处理逻辑
        time.sleep(0.001)  # 模拟1ms处理时间
