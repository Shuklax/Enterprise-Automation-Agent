import asyncio
from typing import Dict, Any
from agent.loop import AgentLoop
from services.database import save_task_result

class TaskProcessor:
    """
    Background worker that processes tasks
    """
    
    def __init__(self):
        self.agent = AgentLoop()
        self.task_queue = asyncio.Queue()
    
    async def add_task(self, task_id: str, task_params: Dict[str, Any]):
        """Add task to processing queue"""
        await self.task_queue.put((task_id, task_params))
    
    async def process_tasks(self):
        """Main worker loop - processes tasks from queue"""
        while True:
            try:
                task_id, task_params = await self.task_queue.get()
                
                # Update status to processing
                save_task_result(task_id, "processing")
                
                # Process task through agent loop
                result = await self.agent.process_task(task_id, task_params)
                
                # Save results to database
                save_task_result(
                    task_id=task_id,
                    status="completed",
                    category=result["category"],
                    reasoning=result["reasoning"],
                    action_taken=result["action_taken"],
                    result=result
                )
                
                self.task_queue.task_done()
                
            except Exception as e:
                print(f"Error processing task {task_id}: {str(e)}")
                save_task_result(
                    task_id=task_id,
                    status="failed",
                    result={"error": str(e)}
                )
                self.task_queue.task_done()
    
    async def start(self):
        """Start the background worker"""
        asyncio.create_task(self.process_tasks())

# Global task processor instance
task_processor = TaskProcessor()