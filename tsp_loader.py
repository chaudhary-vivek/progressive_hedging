import re
from typing import Dict, List, Tuple
import os

# All problem
def parse_mptsp_problem(file_path: str) -> Dict:
    with open(file_path + '/prob.txt', 'r') as file:
        content = file.read()

    # Initialize the data structure to store parsed information
    problem_data = {
        'name': '',
        'comment': '',
        'type': '',
        'dimension': 0,
        'n_path': 0,
        'edge_weight_type': '',
        'edge_data_format': '',
        'nodes': [],
        'edges': []
    }

    # Parse the header information
    header_pattern = r'NAME\s*:\s*(.+)\nCOMMENT\s*:\s*(.+)\nTYPE\s*:\s*(.+)\nDIMENSION\s*:\s*(\d+)\nN_PATH\s*:\s*(\d+)\nEDGE_WEIGHT_TYPE\s*:\s*(.+)\nEDGE_DATA_FORMAT\s*:\s*(.+)'
    header_match = re.search(header_pattern, content, re.MULTILINE)
    
    if header_match:
        problem_data['name'] = header_match.group(1).strip()
        problem_data['comment'] = header_match.group(2).strip()
        problem_data['type'] = header_match.group(3).strip()
        problem_data['dimension'] = int(header_match.group(4))
        problem_data['n_path'] = int(header_match.group(5))
        problem_data['edge_weight_type'] = header_match.group(6).strip()
        problem_data['edge_data_format'] = header_match.group(7).strip()

    # Parse node coordinates
    node_section = re.search(r'NODE_COORD_SECTION([\s\S]*?)EDGE_WEIGHT_SECTION', content)
    if node_section:
        node_lines = node_section.group(1).strip().split('\n')
        for line in node_lines:
            node_id, x, y = map(float, line.split())
            problem_data['nodes'].append((int(node_id), x, y))

    # Parse edge weights
    edge_section = re.search(r'EDGE_WEIGHT_SECTION([\s\S]*?)EOF', content)
    if edge_section:
        edge_lines = edge_section.group(1).strip().split('\n')
        for line in edge_lines:
            node1, node2, weight = map(int, line.split())
            problem_data['edges'].append((node1, node2, weight))

    return problem_data


def parse_scenario_file(file_path: str) -> Dict[Tuple[int, int, int], float]:
    with open(file_path, 'r') as file:
        content = file.read()

    # Extract the C_ijk values
    values = re.findall(r'\d+(?:\.\d+)?', content)
    values = [float(v) for v in values[1:]]  # Skip the first value (number of nodes)

    # Organize the data into a dictionary
    scenario_data = {}
    n_nodes = int(len(values) ** (1/3))  # Cube root of total values gives number of nodes
    for i in range(n_nodes):
        for j in range(n_nodes):
            for k in range(3):  # 3 paths
                index = i * n_nodes * 3 + j * 3 + k
                scenario_data[(i, j, k)] = values[index]

    return scenario_data

# All scenarios
def parse_all_scenarios(directory: str) -> Dict[int, Dict[Tuple[int, int, int], float]]:
    all_scenarios = {}
    scenario_files = [f for f in os.listdir(directory) if f.startswith("Scenario") and f.endswith(".dat")]
    
    for file in scenario_files:
        scenario_number = int(re.search(r'Scenario(\d+)', file).group(1))
        file_path = os.path.join(directory, file)
        scenario_data = parse_scenario_file(file_path)
        all_scenarios[scenario_number] = scenario_data

    return all_scenarios

def print_scenario_summary(scenarios: Dict[int, Dict[Tuple[int, int, int], float]]):
    print(f"Total number of scenarios: {len(scenarios)}")
    for scenario_num, scenario_data in scenarios.items():
        n_nodes = int(len(scenario_data) ** (1/3))
        print(f"\nScenario {scenario_num}:")
        print(f"  Number of nodes: {n_nodes}")
        print(f"  Total C_ijk values: {len(scenario_data)}")
        print("  Sample values:")
        for (i, j, k), value in list(scenario_data.items())[:5]:
            print(f"    C_{i},{j},{k} = {value}")
