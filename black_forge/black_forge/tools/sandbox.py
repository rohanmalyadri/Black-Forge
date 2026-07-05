import docker
from typing import Optional
from black_forge.tools.registry import global_tool_registry, ToolSchema

class DockerSandbox:
    """Manages isolated execution of shell commands within a Docker container."""
    
    def __init__(self, image: str = "ubuntu:latest"):
        self.image = image
        try:
            self.client = docker.from_env()
        except docker.errors.DockerException as e:
            # For environments without Docker daemon running
            self.client = None
            print(f"Warning: Docker daemon is not accessible. Sandboxing disabled: {e}")

    def run_command(self, command: str, working_dir: str = "/workspace") -> str:
        """Runs a bash command securely inside a one-off Docker container."""
        if not self.client:
            return "Error: Docker daemon is not running. Cannot execute shell safely."
            
        try:
            # Run detached and wait for execution context, auto-removing to prevent bloat.
            container = self.client.containers.run(
                self.image,
                command=f'bash -c "{command}"',
                working_dir=working_dir,
                detach=False,
                remove=True,
                network_disabled=True # Max security: don't allow it to fetch from web natively unless expected
            )
            return container.decode('utf-8')
        except docker.errors.ContainerError as e:
            return f"Command execution failed with exit code {e.exit_status}:\n{e.stderr.decode('utf-8')}"
        except Exception as e:
            return f"Error spawning sandbox: {str(e)}"

# Global Sandbox instance
global_sandbox = DockerSandbox()

def run_shell(command: str) -> str:
    """Executes a Bash command in a secure Docker sandbox."""
    return global_sandbox.run_command(command)

# Register the sandbox execution tool to the global registry
global_tool_registry.register_tool(
    ToolSchema(name="run_shell", description="Executes a Bash command inside an isolated, secure Docker container. Use this to run linux commands safely."),
    run_shell
)
