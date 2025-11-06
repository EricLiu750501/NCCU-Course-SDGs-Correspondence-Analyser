import re

def format_goals_for_llm(raw_text: str) -> str:
    output_lines = []
    # Use regex to find all goal sections. A section starts with '# Goal ' and goes until the next one or the end of the file.
    goal_sections = re.findall(r'# Goal \d+.*?(?=# Goal \d+|$)', raw_text, re.DOTALL)

    for section in goal_sections:
        goal_match = re.search(r'# Goal (\d+)', section)
        if not goal_match: continue
        goal_num = int(goal_match.group(1))
        goal_name = SDG_MAPPING[goal_num - 1]
        output_lines.append(f"# Goal {goal_num}: {goal_name}\n")

        # Split the section by the 'Target' marker to isolate each target and its indicators.
        target_blocks = re.split(r'Target\s*####\s*', section)[1:]
        for block in target_blocks:
            # For each block, split the target from its indicators.
            if 'Indicators' in block:
                target_part, indicators_part = re.split(r'Indicators\s*', block, 1)
            else:
                target_part = block
                indicators_part = ''

            # Process Target
            target_content = target_part.strip().replace('\n', ' ')
            
            match = re.match(r'([\d.a-z]+)\s+(.*)', target_content)
            if not match: continue
            target_id, target_desc = match.groups()
            output_lines.append(f"- **Target {target_id}:** {target_desc.strip()}")

            # Process Indicators
            indicator_list = re.split(r'\s*#####\s*', indicators_part.strip())
            for indicator_content in indicator_list:
                indicator_content = indicator_content.strip().replace('\n', ' ')
                if not indicator_content: continue
                
                match = re.match(r'([\d.a-z.]+)\s+(.*)', indicator_content)
                if not match: continue
                indicator_id, indicator_desc = match.groups()
                output_lines.append(f"  - **Indicator {indicator_id}:** {indicator_desc.strip()}")
            
            output_lines.append("") # Add a newline for better readability between targets.
    return "\n".join(output_lines)

def format_goals_less(raw_text: str) -> str:
    """
    Parses the raw goals markdown and formats it into a clean,
    structured list with only targets (no indicators).
    """
    output_lines = []
    goal_sections = re.findall(r'# Goal \d+.*?(?=# Goal \d+|$)', raw_text, re.DOTALL)
    for section in goal_sections:
        goal_match = re.search(r'# Goal (\d+)', section)
        if not goal_match: continue
        goal_num = int(goal_match.group(1))
        goal_name = SDG_MAPPING[goal_num - 1]
        output_lines.append(f"# Goal {goal_num}: {goal_name}\n")
        target_blocks = re.split(r'Target\s*####\s*', section)[1:]
        for block in target_blocks:
            if 'Indicators' in block:
                target_part, _ = re.split(r'Indicators\s*', block, 1)
            else:
                target_part = block
            target_content = target_part.strip().replace('\n', ' ')
            match = re.match(r'([\d.a-z]+)\s+(.*)', target_content)
            if not match: continue
            target_id, target_desc = match.groups()
            output_lines.append(f"- **Target {target_id}:** {target_desc.strip()}")
        output_lines.append("")
    return "\n".join(output_lines)

SDG_MAPPING = [
    "No Poverty",
    "Zero Hunger",
    "Good Health and Well-being",
    "Quality Education",
    "Gender Equality",
    "Clean Water and Sanitation",
    "Affordable and Clean Energy",
    "Decent Work and Economic Growth",
    "Industry, Innovation and Infrastructure",
    "Reduced Inequalities",
    "Sustainable Cities and Communities",
    "Responsible Consumption and Production",
    "Climate Action",
    "Life Below Water",
    "Life on Land",
    "Peace, Justice and Strong Institutions",
    "Partnerships for the Goals",
]



def main():
    """
    Reads the messy goals.md file, formats it into two versions,
    and saves them to new files.
    """
    try:
        with open('goals.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Generate the full version
        formatted_content_full = format_goals_for_llm(content)
        with open('goals_formatted.md', 'w', encoding='utf-8') as f:
            f.write(formatted_content_full)
        print("Successfully formatted goals and saved to 'goals_formatted.md'")

        # Generate the version without indicators
        formatted_content_less = format_goals_less(content)
        with open('goal_formatted_less.md', 'w', encoding='utf-8') as f:
            f.write(formatted_content_less)
        print("Successfully formatted goals without indicators and saved to 'goal_formatted_less.md'")
        
    except FileNotFoundError:
        print("Error: goals.md not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()