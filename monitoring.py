import time
import logging
from datetime import datetime
from typing import Dict, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class RequestMetrics:
    user_id: int
    timestamp: datetime
    processing_time: float
    success: bool

class MetricsCollector:
    def __init__(self):
        self.requests: List[RequestMetrics] = []
        self.start_time = datetime.now()
    
    def record_request(self, user_id: int, processing_time: float, success: bool):
        """Запись метрик запроса"""
        metric = RequestMetrics(
            user_id=user_id,
            timestamp=datetime.now(),
            processing_time=processing_time,
            success=success
        )
        self.requests.append(metric)
        
        # Ограничиваем размер истории
        if len(self.requests) > 1000:
            self.requests = self.requests[-1000:]
    
    def get_stats(self) -> Dict:
        """Получение статистики"""
        if not self.requests:
            return {}
        
        successful = [r for r in self.requests if r.success]
        failed = [r for r in self.requests if not r.success]
        
        return {
            "total_requests": len(self.requests),
            "successful_requests": len(successful),
            "failed_requests": len(failed),
            "success_rate": len(successful) / len(self.requests) * 100,
            "avg_processing_time": sum(r.processing_time for r in self.requests) / len(self.requests),
            "uptime_minutes": (datetime.now() - self.start_time).total_seconds() / 60
        }
