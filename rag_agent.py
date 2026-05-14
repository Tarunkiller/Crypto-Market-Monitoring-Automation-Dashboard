import os
from loguru import logger
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain.memory import ConversationBufferMemory
from langchain.agents import Tool, AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from database.connection import DATABASE_URL
from analytics.embeddings import get_vector_store

class RAGAnalyticsAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0)
        self.memory = ConversationBufferMemory(return_messages=True, memory_key="chat_history")
        
        # 1. SQL Tool setup
        try:
            self.db = SQLDatabase.from_uri(DATABASE_URL)
            self.sql_agent = create_sql_agent(
                llm=self.llm,
                toolkit=None, # Will use raw tools if toolkit is not explicitly needed, but easier to just use the agent as a tool
                db=self.db,
                agent_type=AgentType.OPENAI_FUNCTIONS,
                verbose=True
            )
        except Exception as e:
            logger.error(f"Failed to initialize SQL Database for Agent: {e}")
            self.sql_agent = None

        # 2. Vector Store setup
        self.vector_store = get_vector_store()
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})

        # 3. Combine Tools
        self.tools = [
            Tool(
                name="DatabaseQuery",
                func=self._run_sql_query,
                description="Use this tool to execute SQL queries and answer questions about exact prices, high growth, volume trends, and specific coin metrics in the database."
            ),
            Tool(
                name="MarketReports",
                func=self._search_vector_store,
                description="Use this tool to search for historical market reports, trends, anomalies, and summarized insights."
            )
        ]

        # 4. Master Agent Prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an intelligent Crypto Analytics Copilot for a fintech dashboard. "
                       "Your job is to provide clear, professional business insights based on the user's data. "
                       "You have access to a PostgreSQL database (via DatabaseQuery) for structured queries like prices and volume, "
                       "and a Vector Store (via MarketReports) for qualitative reports and trends. "
                       "Always explain KPIs clearly and format responses cleanly using Markdown."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        self.master_agent = create_openai_tools_agent(self.llm, self.tools, prompt)
        self.agent_executor = AgentExecutor(
            agent=self.master_agent, 
            tools=self.tools, 
            verbose=True,
            memory=self.memory
        )

    def _run_sql_query(self, query: str) -> str:
        if self.sql_agent:
            return self.sql_agent.run(query)
        return "SQL Database connection is currently unavailable."

    def _search_vector_store(self, query: str) -> str:
        docs = self.retriever.invoke(query)
        if not docs:
            return "No relevant market reports found."
        return "\n\n".join([doc.page_content for doc in docs])

    def chat(self, user_input: str) -> str:
        try:
            response = self.agent_executor.invoke({"input": user_input})
            return response['output']
        except Exception as e:
            logger.error(f"Agent chat failed: {e}")
            return "I encountered an error while trying to process your request."
