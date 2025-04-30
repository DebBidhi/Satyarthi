import os
from pydantic import BaseModel, Field
import json
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from functools import partial
import os
from dotenv import load_dotenv
import re
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")


# Initialize tools
news_search_tool = SerperDevTool()

# Setup output callbacks
def json_callback(output, type):
    """Save task output to JSON file with consistent JSON structure"""
    try:
        # Create output directory if it doesn't exist
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        # type is agents or tasks
        filename = f"{output_dir}/{type}.json"
        
        # Extract the raw data to work with
        if hasattr(output, 'raw'):
            data_to_process = output.raw
        elif hasattr(output, 'result'):
            data_to_process = output.result
        else:
            data_to_process = output
        
        # Convert to string if it's not already
        if not isinstance(data_to_process, str):
            data_to_process = str(data_to_process)
        
        # Try to find JSON content within the string (between { and })
        json_pattern = r'(\{[\s\S]*\})'
        matches = re.search(json_pattern, data_to_process)
        
        if matches:
            json_str = matches.group(1)
            # Parse the extracted JSON string into a Python dictionary
            try:
                json_data = json.loads(json_str)
                
                # Ensure properly formatted output structure for agents and tasks
                if type == "agents":
                    # Ensure each agent has a proper prefix like agent_1, agent_2, etc.
                    formatted_data = {}
                    for i, (key, value) in enumerate(json_data.items(), 1):
                        # If key doesn't already start with 'agent_', add the prefix
                        if not key.startswith('agent_'):
                            formatted_key = f"agent_{i}"
                        else:
                            formatted_key = key
                        formatted_data[formatted_key] = value
                    json_data = formatted_data
                
                elif type == "tasks":
                    # Ensure each task has a proper prefix like task_1, task_2, etc.
                    formatted_data = {}
                    for i, (key, value) in enumerate(json_data.items(), 1):
                        # If key doesn't already start with 'task_', add the prefix
                        if not key.startswith('task_'):
                            formatted_key = f"task_{i}"
                        else:
                            formatted_key = key
                        formatted_data[formatted_key] = value
                    json_data = formatted_data
                
                # Save as JSON with indentation for readability
                with open(filename, 'w') as file:
                    json.dump(json_data, file, indent=2)
                print(f"✅ JSON output successfully saved to {filename}")
                return filename
            except json.JSONDecodeError as je:
                print(f"❌ Error parsing JSON: {str(je)}")
                # Fall back to saving the raw text
                with open(filename, 'w') as file:
                    file.write(json_str)
                print(f"✅ Saved raw JSON string to {filename}")
                return filename
        else:
            print("❌ No JSON data found in the output")
            # Save whatever we have
            with open(filename, 'w') as file:
                file.write(data_to_process)
            print(f"✅ Saved raw output to {filename}")
            return filename
            
    except Exception as e:
        print(f"❌ Error saving JSON output: {str(e)}")
        return None
    
agents_json_callback = partial(json_callback, type="agents")
tasks_json_callback = partial(json_callback, type="tasks")

def save_query(output):
    with open("output/title.txt", "w") as wr:
        # If output is a TaskOutput object
        if hasattr(output, 'raw'):
            wr.write(output.raw)
        # If output is a string
        else:
            wr.write(str(output))

# Pydantic models for validation
class AgentConfig(BaseModel):
    """Configuration for an agent with proper validation"""
    role: str = Field(..., description="The role of the agent")
    goal: str = Field(..., description="The primary goal of the agent")
    backstory: str = Field(..., description="Background story for the agent")
    
class TaskConfig(BaseModel):
    """Configuration for a task with proper validation"""
    description: str = Field(..., description="Detailed description of the task")
    agent: str = Field(..., description="ID of the agent assigned to this task")
    expected_output: str = Field(..., description="Description of expected output format")

def create_agents():
    """Create all agents for the integrated workflow"""
    query_enhancer_agent = Agent(
        role="Query Enhancement Specialist",
        goal="Improve and refine user queries to maximize search relevance and information retrieval",
        backstory="""You are an expert in query refinement with expertise in information retrieval techniques, 
        natural language processing, and domain-specific knowledge. You can identify missing context, 
        suggest relevant keywords, and reframe questions to yield optimal results.""",
        verbose=True,
        tools=[news_search_tool],
        allow_delegation=False
    )
    
    query_analysis_agent = Agent(
        role="News Query Analyst",
        goal="Break down complex news topics into key components for comprehensive analysis",
        backstory="""You are an expert analyst with years of experience breaking down complex news stories.
        Your specialty is identifying underlying narratives, key stakeholders, and critical perspectives
        that need investigation. You have a knack for recognizing when a topic needs historical context
        or future implications analysis.""",
        verbose=True,
        tools=[news_search_tool],
        allow_delegation=False
    )

    agent_designer = Agent(
        role="Agent Architecture Designer",
        goal="Design specialized research agents tailored to each identified perspective",
        backstory="""You are an AI systems architect with expertise in creating specialized research agents.
        You understand how to design agents with clear roles, goals, and backstories that are optimized
        for specific information gathering tasks. You ensure that your agent designs provide balanced
        coverage of all perspectives without bias.""",
        verbose=True,
        tools=[news_search_tool],
        allow_delegation=False
    )

    task_designer = Agent(
        role="Task Framework Engineer",
        goal="Create structured task definitions that guide agents to produce comprehensive analysis",
        backstory="""You are a workflow optimization expert who excels at breaking down complex
        research projects into concrete, actionable tasks. You know exactly how to structure
        task descriptions with clear inputs, processes, and expected outputs that will guide
        agents effectively and ensure high-quality results.""",
        verbose=True,
        allow_delegation=False
    )
    
    return {
        "query_enhancer_agent": query_enhancer_agent,
        "query_analysis_agent": query_analysis_agent,
        "agent_designer": agent_designer,
        "task_designer": task_designer
    }

def create_tasks(agents, query: str = "{query}"):
    """Create all tasks for the integrated workflow"""
    # First task: enhance the user query
    query_enhancement_task = Task(
        description=f"""Transform this user query: "{query}" into a comprehensive, well-structured request.
        Identify missing context, add relevant keywords, and reframe the question to yield optimal results.
        Ensure the enhanced query will provide balanced coverage of the topic.""",
        expected_output="""An enhanced query with additional context, keywords, and proper formatting.
        The query should be comprehensive and well-structured.""",
        agent=agents["query_enhancer_agent"],
        callback=save_query
    )

    # Second task: analyze the enhanced query
    query_analysis_task = Task(
        description="""Using the enhanced query from the previous task, analyze and identify:
        1) Main entities/parties involved in the story
        2) Different perspectives that should be researched (minimum 3-5)
        3) Key aspects of the topic requiring specialized research
        4) Any temporal considerations (historical context, future implications)
        
        Provide a structured analysis that ensures balanced coverage.""",
        expected_output="""A structured JSON dictionary with the following keys:
        - 'entities': list of main entities/parties involved
        - 'perspectives': list of different viewpoints to research
        - 'research_areas': list of specific aspects needing investigation
        - 'temporal_aspects': dict with 'historical_context' and 'future_implications' keys""",
        agent=agents["query_analysis_agent"],
        context=[query_enhancement_task]
    )

    # Modified task to ensure specific JSON output format
    agent_design_task = Task(
        description="""Design specialized agents based on the analysis provided.
        For each identified perspective and research area, create an agent configuration
        with appropriate role, goal, and backstory. Ensure agents are designed to provide
        balanced, comprehensive coverage of the topic without inherent bias.
        
        IMPORTANT: Format your response as a JSON object with this exact structure:
        {
          "agent_1": {
            "role": "...",
            "goal": "...",
            "backstory": "..."
          },
          "agent_2": {
            ...
          },
          ... and so on
        }
        
        Do not include any narrative text before or after the JSON object.""",
        expected_output="""A dictionary with keys "agent_1", "agent_2", etc., each mapping to an agent configuration with:
        - 'role': specific role title for the agent 
        - 'goal': clear primary objective
        - 'backstory': a detailed background written in the second person, addressing the agent directly to define their expertise and context that positions the agent as an expert
        - 'verbose': boolean for logging (default True)""",
        agent=agents["agent_designer"],
        context=[query_analysis_task],
        output_json=AgentConfig,
        callback=agents_json_callback
    )

    # Modified task to ensure specific JSON output format
    task_design_task = Task(
        description="""Create task definitions for each agent that will guide their
        research and analysis process. Each task should have a clear description,
        be assigned to the right agent, and define expected output format and criteria.
        
        IMPORTANT: Format your response as a JSON object with this exact structure:
        {
          "task_1": {
            "description": "...",
            "agent": "agent_1",
            "expected_output": "..."
          },
          "task_2": {
            ...
          },
          ... and so on
        }
        
        Do not include any narrative text before or after the JSON object.""",
        expected_output="""A dictionary with keys "task_1", "task_2", etc., each mapping to task configuration with:
        - 'description': detailed task instructions
        - 'agent': agent_id of the assigned agent (use agent_1, agent_2, etc.)
        - 'expected_output': clear description of output format
        - 'verbose': boolean for logging (default True)""",
        agent=agents["task_designer"],
        context=[query_analysis_task, agent_design_task],
        output_json=TaskConfig,
        callback=tasks_json_callback
    )
    
    return [query_enhancement_task, query_analysis_task, agent_design_task, task_design_task]

def create_crew(query: str = None):
    """Create and configure the integrated crew with query enhancement and analysis"""
    agents_dict = create_agents()
    agents_list = list(agents_dict.values())
    tasks = create_tasks(agents_dict, query)
    
    # Create the integrated crew with sequential processing
    crew = Crew(
        agents=agents_list,
        tasks=tasks,
        process=Process.sequential, 
        verbose=True
    )

    return crew

def main():
    
    user_query = input("Your Query: ")
    crew = create_crew(user_query)
    result = crew.kickoff()
    print("\nCrew analysis complete!")
    print(result)
    print("\nOutput files available in the 'output' directory:")


if __name__ == "__main__":
    main()