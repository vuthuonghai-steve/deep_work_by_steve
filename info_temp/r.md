● 🏗️  Design Section 1: Target Architecture Overview                                                                            
                                                                                                                          
```mermaid
flowchart TB
    subgraph User["User_Project"]
        P1[".skill-context/{name}/"]
    end

    subgraph SkillsRoot["skills-root_Portable_Install"]
        SF["_shared/knowledge/"]
        SA["skill-architect/"]
        SP["skill-planner/"]
        SB["skill-builder/"]
        SV["_shared/validators/"]
    end

    subgraph Output["Output_Skill_Package"]
        PKG["{skills-output}/{skill-name}/"]
    end

    P1 -->|design.md| SA
    SA -->|reads| SF
    SP -->|reads| SF
    SB -->|reads| SF
    SA -->|writes| P1
    SP -->|reads| P1
    SP -->|writes| P1
    SB -->|reads| P1
    SB -->|validates via| SV
    SB -->|produces| PKG

    style SF fill:#e1f5fe
    style SV fill:#fff3e0
```
  Key Principles:                                                                                                              
                                                                                                                               
  1. Dual Root System:                                                                                                         
    - skills_root = nơi install bộ 3 (resolve tự động, không hardcode)                                                         
    - project_root = cwd hoặc nơi có .skill-context/                                                                           
  2. Shared Foundation as Package:                                                                                             
    - _shared/knowledge/framework.md — single source of truth                                                                  
    - _shared/validators/ — handoff validators dùng chung                          
    - Mỗi skill chỉ chứa workflow-specific knowledge                                                                           
  3. Self-Discovering Boot:                                                                                                    
    - Skill tự detect skills_root bằng __file__ hoặc env var                                                                   
    - Không còn ../../_shared hardcode — dùng relative từ skill root 