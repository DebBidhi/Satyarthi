# Satyarthi: AI-Powered News Analysis System

![Satyarthi](https://img.shields.io/badge/Satyarthi-News%20Analysis-805ad5)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![CrewAI](https://img.shields.io/badge/CrewAI-Powered-green)

Satyarthi is an intelligent news analysis system that leverages AI agents to break down complex news topics into comprehensive, multi-perspective analyses. The name "Satyarthi" is inspired by the Sanskrit word meaning "seeker of truth," reflecting the system's mission to provide balanced, thorough insights on news topics.

## 🌟 Features

- **Dynamic Agent Architecture**: Creates specialized research agents tailored to each identified perspective
- **Multi-Perspective Analysis**: Ensures balanced coverage by examining topics from various viewpoints
- **Beautiful HTML Output**: Converts analysis results into modern, responsive card-based HTML interfaces
- **Automated Workflow**: Handles the entire process from query enhancement to final presentation

## 🛠️ System Architecture

Satyarthi operates through a four-stage pipeline:

1. **Initial Query Analysis**

   - Enhances user queries to maximize search relevance
   - Breaks down complex topics into key components
   - Identifies main entities, perspectives, and research areas

2. **Dynamic Agent & Task Creation**
   (`agents creating agents`)

   - Designs specialized research agents for each perspective
   - Creates structured task definitions for comprehensive analysis

3. **Parallel Research & Analysis**

   - Agents perform research using search tools
   - Each agent specializes in a specific perspective or aspect

4. **Content Generation & Display**
   - Converts markdown analyses into modern HTML cards
   - Provides a clean navigation interface for all analyses

## 📋 Prerequisites

- Python 3.11+
- CrewAI library
- SerperDev API key (for web search capabilities)
- OpenAI API key (for agent intelligence)

## 🔧 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/DebBidhi/satyarthi.git
   cd satyarthi
   ```

2. Install dependencies:

   ```bash
   uv sync
   ```

3. Set up environment variables:
   ```bash
   # Create a .env file in the root directory
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   echo "SERPER_API_KEY=your_serper_api_key_here" >> .env
   ```

## 🚀 Usage

Run the main script to start the analysis process:

```bash
python main.py
```

The system will:

1. Prompt you for a news topic/query
2. Design specialized agents for the topic
3. Perform comprehensive research and analysis
4. Generate HTML output in the `/htmls` folder
5. Create a navigation interface at `main.html`

### Example Query

```
"What are the different perspectives on central bank digital currencies?"
```

## 📁 Project Structure

```
satyarthi/
├── main.py              # Main entry point
├── initial.py           # Initial query analysis and agent design
├── dynamic_crew.py      # Dynamic agent creation and task execution
├── paste.py             # Markdown to HTML card conversion
├── run.py               # HTML navigation generation
├── Tasks/               # Task definition modules
├── output/              # JSON output files (agents, tasks)
├── data/                # Markdown analysis results
└── htmls/               # Generated HTML files
```

## 🧩 Core Components

### Query Analysis System

- Enhances user queries for optimal search results
- Identifies key perspectives and research areas
- Ensures balanced coverage of the topic

### Dynamic Agent Designer

- Creates specialized agents with clear roles and goals
- Ensures diverse perspectives are represented
- Balances technical, social, economic, and political viewpoints

### Task Framework Engineer

- Designs structured tasks for comprehensive analysis
- Creates clear instructions and expected outputs
- Ensures all relevant aspects are covered

### HTML Generation System

- Converts markdown analyses to modern HTML cards
- Implements responsive design for all devices
- Creates a unified navigation interface

## 🔄 Workflow

1. User provides a query about a news topic
2. Query Enhancement Specialist refines the query
3. News Query Analyst breaks down the topic
4. Agent Architecture Designer creates specialized research agents
5. Task Framework Engineer designs research tasks
6. Dynamic crew performs the research and analysis
7. Results are converted to HTML cards
8. Navigation interface is generated

## 📊 Output

The system generates:

- JSON files defining agents and tasks
- Markdown analysis files with comprehensive research
- HTML card-based interfaces for each analysis
- A main navigation page linking all analyses

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [CrewAI](https://github.com/joaomdmoura/crewAI) for the agent orchestration framework
- [SerperDev](https://serper.dev) for search capabilities
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for HTML processing
