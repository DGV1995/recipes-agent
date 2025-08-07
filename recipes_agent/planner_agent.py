from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4.1-nano")


def planner_agent(user_input: str) -> list[str]:
    system = SystemMessage(
        content="""You are a planner that extracts N recipe requests from user input. 
        Instructions:
        - Return N recipes names from the user input, using '\n' to separed them
        - The names cannot be 'Receta 1' or similar. They must be a real name like 'Ensalada de quinoa'
        """
    )

    response = llm.invoke([system, HumanMessage(content=user_input)])
    tasks = [task.strip() for task in response.content.split("\n")]
    return tasks
