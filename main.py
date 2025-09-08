from controller.healthController import get_health_status
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional


# A Pydantic model to define the structure of a DevOps tool.
# This ensures that incoming data has the correct format and types.
class DevOpsTool(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    is_open_source: bool = False

# The main FastAPI application instance.
app = FastAPI()

# A simple in-memory dictionary to act as our database.
# We'll use this to store and manage our tools.
db_tools: Dict[int, DevOpsTool] = {
    1: DevOpsTool(name="Jenkins", description="Automation server", category="CI/CD"),
    2: DevOpsTool(name="Docker", description="Containerization platform", category="Containerization"),
    3: DevOpsTool(name="Kubernetes", description="Container orchestration", category="Orchestration"),
}

# Counter for new tool IDs.
tool_id_counter = 4

# Endpoint for the "screen" or main page.
@app.get("/", summary="Main screen")
def read_root():
    """
    This is the main screen of the application.
    It returns a welcome message and points to the API documentation.
    """
    return {"message": "Welcome to the DevOps Tools API! Navigate to /docs for the interactive API documentation."}

# Health check endpoint.
app.add_api_route(
    path="/health",
    endpoint=get_health_status,
    methods=["GET"],
    summary="Health Check"
)

# --- CRUD Endpoints for DevOps Tools ---

# GET all tools
@app.get("/tools", summary="List all DevOps tools")
def get_all_tools():
    """
    Retrieves a list of all DevOps tools.
    """
    return list(db_tools.values())

# GET a single tool by ID
@app.get("/tools/{tool_id}", summary="Get a DevOps tool by ID")
def get_tool_by_id(tool_id: int):
    """
    Retrieves a single DevOps tool by its unique ID.
    Raises a 404 error if the tool is not found.
    """
    if tool_id not in db_tools:
        raise HTTPException(status_code=404, detail="Tool not found")
    return db_tools[tool_id]

# POST a new tool
@app.post("/tools", summary="Create a new DevOps tool")
def create_tool(tool: DevOpsTool):
    """
    Creates a new DevOps tool with a unique ID.
    """
    global tool_id_counter
    new_id = tool_id_counter
    db_tools[new_id] = tool
    tool_id_counter += 1
    return {"id": new_id, **tool.dict()}

# PUT to update an existing tool
@app.put("/tools/{tool_id}", summary="Update an existing DevOps tool")
def update_tool(tool_id: int, tool: DevOpsTool):
    """
    Updates an existing DevOps tool identified by its ID.
    Raises a 404 error if the tool is not found.
    """
    if tool_id not in db_tools:
        raise HTTPException(status_code=404, detail="Tool not found")
    db_tools[tool_id] = tool
    return {"id": tool_id, **tool.dict()}

# DELETE a tool
@app.delete("/tools/{tool_id}", summary="Delete a DevOps tool")
def delete_tool(tool_id: int):
    """
    Deletes a DevOps tool identified by its ID.
    Raises a 404 error if the tool is not found.
    """
    if tool_id not in db_tools:
        raise HTTPException(status_code=404, detail="Tool not found")
    del db_tools[tool_id]
    return {"message": f"Tool with ID {tool_id} has been deleted."}
