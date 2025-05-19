from typing import Dict, Any, Callable, List
import asyncio

class EventDispatcher:
    # A simple event dispatcher for handling asynchronous events
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}
        self._event_queue = asyncio.Queue()
        self._running = False
        self._worker_task = None

    def register(self, event_type: str, listener: Callable):
        # Register a listener for a specific event type
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)
    
    async def dispatch(self, event_type: str, data: Any = None):
        # Dispatch an event to all registered listeners
        await self._event_queue.put((event_type, data))
    
    async def _process_events(self):
        # Process events from the queue
        while self._running:
            try:
                event_type, data = await self._event_queue.get()
                if event_type in self.listeners:
                    for listener in self.listeners[event_type]:
                        try:
                            if asyncio.iscoroutinefunction(listener):
                                await listener(data)
                            else:
                                listener(data)
                        except Exception as e:
                            print(f"Error in event listener: {e}")
                self._event_queue.task_done()
            except Exception as e:
                print(f"Error processing event: {e}")
    
    def start(self):
        # Start the event processing loop
        if not self._running:
            self._running = True
            self._worker_task = asyncio.create_task(self._process_events())
    
    async def stop(self):
        # Stop the event processing loop
        if self._running:
            self._running = False
            # Add a dummy event to unblock the queue
            await self._event_queue.put(("__stop__", None))
            if self._worker_task:
                await self._worker_task
                self._worker_task = None

# Create a global event dispatcher instance
event_dispatcher = EventDispatcher()

# Define event types
PROJECT_CREATED = "project.created"
PROJECT_UPDATED = "project.updated"
PROJECT_DELETED = "project.deleted"