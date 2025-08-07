from dotenv import load_dotenv
from langchain_core.messages import SystemMessage
from langchain_deepseek import ChatDeepSeek
from langgraph.graph import END, MessagesState, StateGraph

from recipes_agent.models import RecipeBatchState
from recipes_agent.tools import generate_recipe, generate_recipe_image, upload_recipe

load_dotenv()

llm = ChatDeepSeek(model="deepseek-chat", temperature=0.0, timeout=3600, max_retries=1)


def parse_user_request(state: RecipeBatchState):
    system = SystemMessage(
        content="""You are a planner that extracts N recipe requests from user input. 
        Instructions:
        - Return N recipes names from the user input, using '\n' to separed them
        - The names cannot be 'Receta 1' or similar. They must be a real name like 'Ensalada de quinoa'
        - Do not put numbers before the recipe name (e.g: '1. Tortilla' -> It must be 'Tortilla').
        """
    )
    human = state["messages"][-1]

    response = llm.invoke([system] + [human])
    recipes = [recipe.strip() for recipe in response.content.split("\n")]

    return {**state, "recipe_tasks": recipes, "current_index": 0}


def is_process_completed(state: RecipeBatchState) -> str:
    if state["current_index"] < len(state["recipe_tasks"]) - 1:
        return "next"

    return "end"


def increment_index(state: RecipeBatchState) -> RecipeBatchState:
    return {**state, "current_index": state["current_index"] + 1}


def agent_node(state: RecipeBatchState):
    recipe_name = state["recipe_tasks"][state["current_index"]]
    print(f"Agent node running with recipe: {recipe_name}")

    recipe = generate_recipe(recipe_name)

    if recipe:
        image_url = generate_recipe_image(recipe["name"])
        upload_recipe(recipe, image_url)

    return {**state}


def build_graph():
    builder = StateGraph(MessagesState)

    # Nodes
    builder.add_node("parse_input", parse_user_request, include_multiple=True)
    builder.add_node("agent_node", agent_node)
    builder.add_node("increment_index", increment_index)

    # Entry and finish point
    builder.set_entry_point("parse_input")

    # Edges
    builder.add_edge("parse_input", "agent_node")
    builder.add_conditional_edges(
        "agent_node",
        is_process_completed,
        {"next": "increment_index", "end": END},
    )
    builder.add_edge("increment_index", "agent_node")

    return builder.compile()


def build_and_execute_graph():
    graph = build_graph()

    input = "Dame exactamente 10 recetas veganas y 10 recetas sin gluten"
    result = graph.invoke({"messages": input}, {"recursion_limit": 1000})

    for message in result["messages"]:
        message.pretty_print()


if __name__ == "__main__":
    build_and_execute_graph()
