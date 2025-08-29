🧠 AI Agent Framework
=====================

This project is a minimal agentic framework that allows a Large Language Model (LLM) to reason, call tools, and return results in a loop until the task is complete.

✨ Features
----------

*   Uses **LLM reasoning** to decide next actions.
    
*   Supports **tool execution** via function calls.
    
*   **Agent loop**: runs until the model determines the task is complete.
    
*   Handles structured function responses and text responses.
    

⚙️ How it Works
---------------

1.  User provides a **prompt**.
    
2.  The **LLM generates candidates** (next steps).
    
3.  If a **tool call** is required, the framework executes the function and feeds results back to the LLM.
    
4.  If no further steps are needed, the loop ends and returns the final answer.
    

🛠️ Example Tools
-----------------

*   get\_file\_contents → Reads the contents of a file.
    
*   run\_python\_code → Executes Python code safely.
    

🚀 Running the Agent
--------------------

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python agent.py "get the contents of lorem.txt"   `

Example output:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   Hello from AI-agent!  User prompt: get the contents of lorem.txt  Final response: wait, this isn't lorem ipsum   `

📌 Notes
--------

*   If the model calls an **unknown tool**, the framework raises a fatal error.
    
*   You can extend the agent by **adding more tools** to the tools dictionary.