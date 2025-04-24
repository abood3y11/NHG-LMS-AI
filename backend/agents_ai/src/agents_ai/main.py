#!/usr/bin/env python
import sys
import warnings
import json
import glob

from datetime import datetime

from agents_ai.crew import AgentsAi

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def load_ksu_json_data():
    json_files = glob.glob(r"C:\Users\pc\Desktop\NHG AI LMS\backend\json\student_activity.json")
    all_data = []
    
    for file in json_files:
        with open(file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                # Add source file metadata
                if isinstance(data, list):
                    for item in data:
                        item['_source'] = file
                all_data.extend(data if isinstance(data, list) else [data])
            except json.JSONDecodeError:
                print(f"Error decoding {file}")
    
    return all_data

def run():
    """
    Run the crew with data loaded from JSON files.
    """
    # Load data from JSON files
    json_data = load_ksu_json_data()
    
    # Prepare inputs for each item in the JSON data
    for data_item in json_data:
        try:
            # Create inputs dictionary from JSON data
            # Adjust these mappings based on your JSON structure and what AgentsAi expects
            inputs = {
                'student_answers': data_item.get('student_id', ''),  # or whatever field in your JSON
                'rubric': data_item.get('total_hours', ),  # default value if not found
                'topic': data_item.get('name', '')  # default value if not found
            }
            
            print(f"Processing item from {data_item.get('_source', 'unknown source')}")
            
            # Run the crew with the current item's data
            AgentsAi().crew().kickoff(inputs=inputs)
            
        except Exception as e:
            print(f"An error occurred while processing an item: {e}")
            # You might want to continue with the next item even if one fails
            continue


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        AgentsAi().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        AgentsAi().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    try:
        AgentsAi().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
