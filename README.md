# MCP Inventory Management Server

This project demonstrates how to use **Model Context Protocol (MCP)** to safely connect a **Large Language Model (LLM)** with a **MySQL database** for inventory management.

Instead of allowing an LLM to generate raw SQL queries (which is risky), this project exposes **controlled tools** using MCP, ensuring secure and reliable database operations.

---

## 🚀 Project Overview

The MCP Inventory Server allows an LLM to perform inventory-related operations such as:

- Adding inventory
- Removing inventory
- Checking stock levels
- Listing available inventory

All actions are executed through predefined MCP tools, ensuring the database cannot be misused or corrupted.

---

## 🧠 Why MCP?

Directly connecting an LLM to a database can be dangerous.  
For example, an LLM might accidentally generate destructive SQL queries like `DROP TABLE`.

**Model Context Protocol (MCP)** solves this by:
- Acting as a middleware between the LLM and database
- Allowing only approved operations
- Preventing unsafe or unauthorized queries

---

## 🏗️ System Architecture

User (Natural Language)
↓
LLM
↓
MCP Server (Python Tools)
↓
MySQL Database



The LLM never talks to the database directly.

---

## 🛠️ Tech Stack

- Python 3.10+
- Model Context Protocol (MCP)
- MySQL
- mysql-connector-python
- Pydantic

---

## 📂 Project Structure

inventory-mcp-server/
│
├── inventory_mcp_server.py # MCP server with inventory tools
├── README.md # Project documentation
├── requirements.txt # Python dependencies
└── .venv/ # Virtual environment



---

## 🗄️ Database Schema

```sql
CREATE TABLE inventory (
    item_id VARCHAR(50),
    product_name VARCHAR(100),
    location VARCHAR(50),
    quantity INT DEFAULT 0,
    PRIMARY KEY (item_id, location)
);
🔧 MCP Tools Implemented
Tool Name	Description
add_inventory	Add or update inventory safely
remove_inventory	Remove stock from inventory
check_stock	Check available quantity
list_inventory	List all inventory items

Each tool is explicitly defined and validated.

▶️ How to Run the Project
1️⃣ Activate Virtual Environment
.venv\Scripts\activate
2️⃣ Install Dependencies

pip install -r requirements.txt
3️⃣ Run MCP Server

uv run mcp install inventory_mcp_server.py

The MCP server will start and expose inventory tools.

🧪 Example Usage (LLM Queries)
“List all inventory”

“Check stock for LAP-002 in Mumbai”

“Add 10 units of Logitech Mouse in Delhi”

“Remove 5 units of iPhone 14 in Bengaluru”

The LLM will automatically select the correct MCP tool.

🔐 Security Benefits
No raw SQL from LLM

Parameterized queries only

Controlled tool execution

No destructive operations allowed"# inventory-mcp-server" 
