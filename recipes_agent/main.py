from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_core.messages.system import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from recipes_agent.tools import TOOLS

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(TOOLS)


def assistant(state: MessagesState):
    sys_msg = SystemMessage(
        content="You are a helpul assistant tasked with creating healthy, high protein recipes."
    )
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}


def build_graph():
    builder = StateGraph(MessagesState)

    # Nodes
    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(TOOLS))

    # Edges
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", tools_condition)
    builder.add_edge("tools", "assistant")

    return builder.compile()


def main():
    graph = build_graph()

    input = [
        HumanMessage(
            content="Dame una receta vegana alta en proteínas, crea su imagen y súbela a la base de datos."
        )
    ]
    result = graph.invoke({"messages": input})

    for message in result["messages"]:
        message.pretty_print()


if __name__ == "__main__":
    main()
