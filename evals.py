from agent import run_agent

test_cases = [
    {
        "user_id": "user_1",
        "user_input": "why has my skin been getting worse this month?",
        "expected_tools": ["get_user_history", "search_ingredients"],
    },
    {
        "user_id": "user_1",
        "user_input": "what is my skin history?",
        "expected_tools": ["get_user_history"],
    },
    {
        "user_id": "user_1",
        "user_input": "what does niacinamide do?",
        "expected_tools": ["search_ingredients"],
    },
    {
        "user_id": "user_1",
        "user_input": "hi, what can you help me with?",
        "expected_tools": [],
    },
]

def check_tools_called(result, expected_tools):
    messages = result["messages"]
    tool_names_called = []
    
    for message in messages:
        if message["role"] != "assistant":
            continue
        content = message["content"]
        if isinstance(content, str):
            continue
        for block in content:
            if block.type == "tool_use":
                tool_names_called.append(block.name)
        
        return set(expected_tools).issubset(set(tool_names_called))

def run_evals():
    for case in test_cases:
        result = run_agent(case["user_id"], case["user_input"])
        passed = check_tools_called(result, case["expected_tools"])
        print(f"{'PASS' if passed else 'FAIL'}: {case['user_input']}")

if __name__ == "__main__":
    run_evals()        