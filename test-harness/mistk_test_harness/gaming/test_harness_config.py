from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, LetterCase
from typing import List, Optional

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ServiceConfig:
    port: int = 8081
    image: Optional[str] = None
    module: Optional[str] = None
    url: Optional[str] = None
    container: Optional[str] = None

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class OrchestratorConfig:
    service: ServiceConfig
    name: Optional[str] = None
    properties: Optional[str] = None # environment props
    episodes: int = 1
    episode_save_path: Optional[str] = None
    episode_cfgs: Optional[List[str]] = field(default_factory=list)
    reset: Optional[bool] = True
    
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class AgentConfig:
    
    service: ServiceConfig
    name: Optional[str] = None
    properties: Optional[str] = None
    hyperparameters: Optional[str] = None
    replay: Optional[bool] = True
    model_path: Optional[str] = None
    model_save_path: Optional[str] = None
    reset: Optional[bool] = True
    reset_unload: Optional[bool] = True

@dataclass_json(letter_case=LetterCase.CAMEL)  
@dataclass
class TestHarnessConfig:
    agents: Optional[List[AgentConfig]] = field(default_factory=list)
    orchestrator: Optional[OrchestratorConfig] = None
    logs: Optional[str] = True
    disable_container_shutdown: Optional[bool] = False
        


    
    
