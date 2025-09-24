from mcp.server.fastmcp import FastMCP
from pydantic import Field
from simple_salesforce import Salesforce
import os

# MCP server base
mcp = FastMCP(
    name="Salesforce MCP Server",
    host="0.0.0.0",
    port=3000,
    stateless_http=True,
    debug=True,
)

# Connessione a Salesforce usando variabili d’ambiente
def connect_salesforce():
    return Salesforce(
        username=os.getenv("SF_USERNAME"),
        password=os.getenv("SF_PASSWORD"),
        security_token=os.getenv("SF_SECURITY_TOKEN"),
        domain="login"  # se usi sandbox -> "test"
    )

@mcp.tool(
    title="Welcome a user",
    description="Return a friendly welcome message for the user."
)
def welcome(name: str = Field(description="Name of the user")) -> str:
    return f"Welcome {name}, your Salesforce MCP is running!"

@mcp.tool(
    title="Count Accounts",
    description="Return how many Accounts exist in Salesforce."
)
def count_accounts() -> str:
    sf = connect_salesforce()
    result = sf.query("SELECT COUNT() FROM Account")
    return f"There are {result['totalSize']} Accounts in Salesforce."

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
