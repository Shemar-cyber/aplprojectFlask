from graphviz import Digraph

def generate_ast(parsed_command, filename='ast'):
    """
    Generates a visual Abstract Syntax Tree (AST) representation of parsed commands
    as a PNG image using Graphviz.
    
    """
    # Initialize directed graph with global styling
    dot = Digraph(comment='AST', format='png')
    
    
    # Unified visual styling for all nodes
    dot.attr('node', 
             shape='ellipse',        # Rounded node shapes
             style='filled',         # Filled background
             fillcolor='#f0f8ff',    # Light blue fill color
             fixedsize='true',       # Consistent node sizes
             width='1.8',           # Node width in inches
             height='0.9',          # Node height in inches
             fontsize='10',         # Font size
             fontname='Arial')      # Clean font face
    
    # Only generate AST if the input is a structured command
    if isinstance(parsed_command, tuple):
        _add_ast_nodes(dot, parsed_command)
    
    # Render and automatically open the visualization
    dot.render(filename, view=False, cleanup=True)
    return f"{filename}.png"

def _add_ast_nodes(dot, node, parent_id=None):
    """
    Recursively builds the AST by adding nodes and edges to the Digraph.
    
    Args:
        dot (Digraph): Graphviz graph object
        node: Current node to process (tuple/dict/list/primitive)
        parent_id: ID of parent node for edge creation
    
    Processing Logic:
        - Handles 4 node types: tuples, dicts, lists, and primitives
        - Implements intelligent text formatting:
          * Line breaks for long values
          * Smart truncation with ellipsis
          * Key-value separation for dicts
    """
    # Configuration for text formatting
    max_label_length = 18  # Maximum characters before truncation
    max_value_lines = 2    # Maximum lines for value text
    
    # Tuple nodes represent command structures
    if isinstance(node, tuple):
        node_id = str(id(node))  # Unique ID using memory address
        label = node[0]          # Command name (first element)
        
        # Truncate long labels with ellipsis
        if len(label) > max_label_length:
            label = f"{label[:max_label_length]}..."
        
        # Add the node to the graph
        dot.node(node_id, label=label)
        
        # Connect to parent if exists
        if parent_id:
            dot.edge(parent_id, node_id)
        
        # Process all non-None children
        for child in node[1:]:
            if child is None:
                continue
                
            # Recursive processing based on child type    
            if isinstance(child, (tuple, dict, list)):
                _add_ast_nodes(dot, child, node_id)
            else:
                # Format primitive values
                child_label = str(child)
                if len(child_label) > max_label_length:
                    child_label = f"{child_label[:max_label_length]}..."
                
                child_id = f"{node_id}_{id(child)}"
                dot.node(child_id, label=child_label)
                dot.edge(node_id, child_id)
    
    # Dictionary nodes contain command details
    elif isinstance(node, dict):
        node_id = str(id(node))
        dot.node(node_id, label="Details")
        
        if parent_id:
            dot.edge(parent_id, node_id)
        
        # Process each key-value pair
        for key, value in node.items():
            key_id = f"{node_id}_{key}"
            
            # Format value with multi-line handling
            value_str = str(value)
            if len(value_str) > 15:
                # Split long values into chunks
                chunks = [value_str[i:i+15] for i in range(0, len(value_str), 15)]
                value_str = '\n'.join(chunks[:max_value_lines])
                if len(chunks) > max_value_lines:
                    value_str += '...'
            
            # Create visually separated key-value nodes
            dot.node(key_id, label=f"{key}\n──\n{value_str}")
            dot.edge(node_id, key_id)
            
            # Recursively process complex values
            if isinstance(value, (tuple, dict, list)):
                _add_ast_nodes(dot, value, key_id)
    
    # List nodes (less common in this grammar)
    elif isinstance(node, list):
        node_id = str(id(node))
        dot.node(node_id, label="List")
        
        if parent_id:
            dot.edge(parent_id, node_id)
        
        # Process list items with index-based IDs
        for index, item in enumerate(node):
            item_id = f"{node_id}_item{index}"
            if isinstance(item, (tuple, dict, list)):
                _add_ast_nodes(dot, item, node_id)
            else:
                item_label = str(item)
                if len(item_label) > max_label_length:
                    item_label = f"{item_label[:max_label_length]}..."
                dot.node(item_id, label=item_label)
                dot.edge(node_id, item_id)