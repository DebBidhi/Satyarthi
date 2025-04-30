import os
import json
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
from crewai import TaskOutput
news_search_tool = SerperDevTool()

# Helper callback function
def save_md(output: TaskOutput):
    """
    Saves the given TaskOutput content to a Markdown (.md) file.

    Parameters:
    output (TaskOutput): An object containing the content and metadata for the Markdown file.
    """
    os.makedirs('data', exist_ok=True)

    # Construct the filename using the agent attribute
    filename = f"data/{output.agent}.md"

    try:
        # Write the raw content to the file with UTF-8 encoding
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(output.raw)
        print(f"File saved as '{filename}'.")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")

# File paths
agents_file_path = 'output/agents.json'
tasks_file_path = 'output/tasks.json'

def main():
    # Load agents from JSON file
    with open(agents_file_path, 'r') as f:
        agents_data = json.load(f)

    # Load tasks from JSON file
    with open(tasks_file_path, 'r') as f:
        tasks_data = json.load(f)

    # Create Agent instances
    agents = {}
    for agent_key, agent_info in agents_data.items():
        agents[agent_key] = Agent(
            role=agent_info['role'],
            goal=agent_info['goal'],
            tools=[news_search_tool],
            backstory=agent_info['backstory'],
            verbose=agent_info.get('verbose', False)
        )

    # Create Task instances
    tasks = []
    for task_key, task_info in tasks_data.items():
        agent_key = task_info['agent']

        if agent_key not in agents:
            raise ValueError(f"Agent '{agent_key}' not found for task '{task_key}'")

        tasks.append(Task(
            description=task_info['description']+ ". Present your findings in a clear, well-structured markdown format",
            expected_output=task_info['expected_output'] + ". Output should be a Markdown",
            agent=agents[agent_key],
            callback=save_md,
            verbose=task_info.get('verbose', False)
        ))

    # Initialize Crew with agents and tasks
    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        verbose=True  
    )
    
    crew.kickoff()


if __name__ == "__main__":
    main()

