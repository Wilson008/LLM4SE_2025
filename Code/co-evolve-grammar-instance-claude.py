import os
from anthropic import Anthropic

def read_file(filename):
    """Read content from a file"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file {filename}: {str(e)}")
        return None

def get_response_content(response):
    """Extract content from API response"""
    try:
        if hasattr(response.content, 'text'):
            return response.content.text
        elif isinstance(response.content, list):
            return ' '.join(str(item.text) for item in response.content if hasattr(item, 'text'))
        return str(response.content)
    except Exception as e:
        print(f"Warning: Error processing response content: {e}")
        return str(response.content)

def analyze_grammar_evolution(api_key):
    """Main function: Analyze grammar evolution using Chain-of-Thought approach"""
    # Read files
    grammar1 = read_file('Code\\Step_3_Case_Languages\\CheckerDSL\\grammar_1_20150503_55911bf.txt')
    grammar2 = read_file('Code\\Step_3_Case_Languages\\CheckerDSL\\grammar_2_20150727_3fa6e6d.txt')
    instance1 = read_file('Code\\Step_3_Case_Languages\\CheckerDSL\\instance_1_20250503_55911bf.txt')
    
    if None in [grammar1, grammar2, instance1]:
        print("File reading failed. Please check file paths and contents.")
        return
    
    # Initialize Anthropic client
    client = Anthropic(api_key=api_key)
    messages = []
    final_result = []
    
    # Step 1: Introduce grammar_1
    messages.append({
        "role": "user",
        "content": f"""
        I will show you two versions of a grammar and an instance that conforms to the first grammar. 
        Let's start with the first grammar version:

        {grammar1}

        Please remember the content.
        """
    })
    
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1000,
        messages=messages
    )
    # messages.append({"role": "assistant", "content": response.content})
    content = get_response_content(response)
    messages.append({"role": "assistant", "content": content})
    
    # Step 2: Introduce grammar_2
    messages.append({
        "role": "user",
        "content": f"""
        Now, here's the second version of the grammar:

        {grammar2}

        Please remember the content also.
        """
    })
    
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1000,
        messages=messages
    )
    # messages.append({"role": "assistant", "content": response.content})
    content = get_response_content(response)
    messages.append({"role": "assistant", "content": content})
    
    # Step 3: Process instance
    messages.append({
        "role": "user",
        "content": f"""
        Now, here's an instance that conforms to the first grammar:

        {instance1}

        grammar_1 is the initial grammar of the DSL. We evolved it to get grammar_2. instance_1 was originally a text instance that followed grammar_1. Now I want you to analyze the differences between the two versions of the grammar, and based on this difference, modify instance_1 and get instance_2, which will follow grammar_2. Please address the following things:
        1. When evolving the instance, please do not omit any mandatory elements, such as characters enclosed by single quotes
        2. If grammar_2 adds a new grammar rule or a new attribute that is optional or in an “OR” relationship (i.e., |), then please do not instantiate it.
        3. Do not miss or add any auxiliary information inthe instance, e.g., comments, formats (white space, indents, tabs, empty lines, etc.).

        """
    })
    
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2000,
        messages=messages
    )
    content = get_response_content(response)
    final_result.append("=== Step 3: Instance Transformation ===\n" + content)
    final_text = '\n'.join(final_result)
    
    # Save the final result
    with open('Code\\Step_3_Case_Languages\\CheckerDSL\\instance_2_gen_claude_10.txt', 'w', encoding='utf-8') as f:
        f.write(str(final_text))
    
    print("Analysis completed. The result has been save in Code\\Step_3_Case_Languages\\CheckerDSL\\instance_2_gen_claude_10.txt")
    # print("\nAnalysis result: ")
    # print("="*50)
    # # Using final_text instead of response.content for preview
    # if len(final_text) > 500:
    #     print(final_text[:500] + "...")
    # else:
    #     print(final_text)

if __name__ == "__main__":
    # # Input API key    
    analyze_grammar_evolution(' ')