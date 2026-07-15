from typing import Dict, Callable

class MessageBus:
    """The central router connecting Channel Managers (Slack, Telegram) to the Engine."""
    
    def __init__(self):
        self.channel_listeners: Dict[str, Callable] = {}
        
    def register_channel(self, channel_name: str, callback: Callable):
        """Register a channel like 'Slack' and the function to call when it receives a payload."""
        self.channel_listeners[channel_name] = callback
        print(f"Registered Channel Webhook listener for {channel_name}")
        
    def receive_message(self, channel_name: str, payload: dict):
        """Entrypoint for external web requests to trigger the agent natively instead of Typer CLI."""
        if channel_name in self.channel_listeners:
            print(f"[MessageBus] Routing payload from {channel_name}")
            return self.channel_listeners[channel_name](payload)
        else:
            raise ValueError(f"Channel {channel_name} is not registered.")
            
global_message_bus = MessageBus()
