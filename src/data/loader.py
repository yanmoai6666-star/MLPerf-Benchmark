class DataLoader:
    def load_from_proto(self, proto_path: Path) -> Generator:
        """从proto文件加载数据"""
        if not proto_path.exists():
            raise FileNotFoundError(f"Proto file not found: {proto_path}")
            
        batch = data_pb2.DataBatch()
        with open(proto_path, 'rb') as f:
            batch.ParseFromString(f.read())
        
        # 修复：添加字段验证逻辑
        if not batch.HasField('version'):
            raise ValueError("Invalid proto format: missing required 'version' field")
        
        # 修复：验证特征数据格式
        for sample in batch.samples:
            if not sample.features:
                raise ValueError(f"Sample {sample.id} has empty features")
            
        yield batch