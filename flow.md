```mermaid
flowchart TD
    parse_input --> agent

    %% Condicional desde check_process_status
    agent -->|is_process_completed == false| increment_index
    agent -->|is_process_completed == true| END((END))

    increment_index --> agent

    %% Punto de entrada
    start((Start)) --> parse_input
