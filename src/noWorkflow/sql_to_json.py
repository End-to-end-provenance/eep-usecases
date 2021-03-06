import sqlite3
import json
import ast

def get_info_from_sql(input_db_file, run_num):
    """ queries noWorkflow sql database """

    db = sqlite3.connect(input_db_file, uri=True)
    c = db.cursor()

    # script_name
    c.execute('SELECT id, command from trial where id = ?', (run_num, ))
    temp = c.fetchone()
    temp = temp[1]
    temp = temp.split(" ")
    script_name = temp[1]

    # process nodes
    c.execute('SELECT trial_id, id, name, return_value, line from function_activation where trial_id = ?', (run_num,))
    script_steps = c.fetchall()

    # file io nodes
    c.execute('SELECT trial_id, name, function_activation_id, mode, content_hash_after from file_access where trial_id = ?' , (run_num, ))
    files = c.fetchall()

    # dict for easier access to file info
    temp = {}
    for f in files:
        d = {"name": f[1], "mode": f[3], "hash" : f[4]}
        temp[f[2]] = d
    files = temp

    # functions
    c.execute('SELECT name, trial_id, last_line from function_def where trial_id = ?', (run_num, ))
    func_ends = c.fetchall()

    # dict for easier access to func_ends. used for collapsing nodes
    temp = {}
    end_funcs = {}
    for f in func_ends:
        temp[f[0]] = f[2]
        end_funcs[f[2]] = f[0]
    func_ends = temp

    # if f has return value, f[2]-=1
    # so last line detected correctly
    # last line informs the finish node + allows for sequential functions
    for f in func_ends:
        c.execute('SELECT trial_id, name, return_value from function_activation where trial_id = ? and name = ?', (run_num, f, ))
        calls = c.fetchall()
        for call in calls:
            if call[2]!="None":
                func_ends[f]-=1
                temp = func_ends[f]
                end_funcs[temp]=f

    c.close()

    return script_steps, files, func_ends, end_funcs, script_name

def get_defaults(script_name):
    """ sets default required fields for the Prov-JSON file, ie environment node
    variable 'rdt:script' is the first script in the workflow.
    """
    result, activity_d, environment_d = {}, {}, {}

    environment_d['rdt:language'] = "R"
    environment_d["rdt:script"] = script_name
    activity_d['environment'] = environment_d

    result['activity']= activity_d

    keys = ["entity", "wasInformedBy", "wasGeneratedBy", "used"]
    for i in range (0, len(keys)):
        result[keys[i]]={}

    return result

def add_informs_edge(result, prev_p, current_p, e_count):
    """ adds informs edge between steps in the script or between script nodes """

    current_informs_edge = {}
    current_informs_edge['prov:informant'] = prev_p
    current_informs_edge['prov:informed'] = current_p

    ekey_string = "e" + str(e_count)
    e_count+=1

    result['wasInformedBy'][ekey_string] = current_informs_edge

    return e_count

def add_start_node(result, step, p_count, next_line=None):
    """ adds start node and edge for current step """

    # make node
    start_node_d = {}
    start_node_d['rdt:type'] = "Start"
    start_node_d["rdt:elapsedTime"] = "0.5"
    keys = ["rdt:scriptNum", "rdt:startLine", "rdt:startCol", "rdt:endLine", "rdt:endCol"]
    for key in keys:
        start_node_d[key] = "NA"

    # choose most descriptive label for the node
    if next_line:
        start_node_d['rdt:name'] = next_line
    else:
        start_node_d['rdt:name'] = step[2]

    pkey_string = "p" + str(p_count)
    prev_p = pkey_string
    p_count+=1

    # add node
    result['activity'][pkey_string] = start_node_d

    return prev_p, p_count

def add_end_node(result, p_count, name):
    """ makes Finish node so that the function or loop is collapsible """

    # make node
    end_node_d = {}
    end_node_d['rdt:name'] = name
    end_node_d['rdt:type'] = "Finish"
    end_node_d["rdt:elapsedTime"] = "0.5"
    keys = ["rdt:scriptNum", "rdt:startLine", "rdt:startCol", "rdt:endLine", "rdt:endCol"]
    for key in keys:
        end_node_d[key] = "NA"

    # add node
    pkey_string = "p" + str(p_count)
    p_count += 1
    result['activity'][pkey_string] = end_node_d

    return pkey_string, p_count

def add_process(result, p_name, p_count, s, script_name, next_line):
    """ adds process node and edge for each step in script_steps
    chooses the most descriptive label for the node between:
    noWorkflow default step label or the relevent line in the script"""

    # defaults for all process nodes
    current_process_node = {}
    current_process_node['rdt:type'] = "Operation"
    current_process_node["rdt:elapsedTime"] = "0.5"
    current_process_node["rdt:startLine"], current_process_node["rdt:endLine"] = str(s[4]), str(s[4])

    # get most descriptive label and dependent properties
    if s[2].startswith("__") or s[2]=="f" and next_line != "":
        line_label = next_line.strip()
    else:
        line_label = s[2]

    current_process_node['rdt:name'] = line_label
    current_process_node["rdt:startCol"] = str(0)
    current_process_node["rdt:endCol"] = str(len(line_label))
    current_process_node["rdt:scriptNum"] = str(0)

    # add the node
    pkey_string = "p" + str(p_count)
    p_count += 1
    result["activity"][pkey_string] = current_process_node

    return p_count, pkey_string

def add_file_node(script, current_link_dict, d_count, result, data_dict):
    """ adds a file node, called by add_file """

    #make file node
    current_file_node = {}
    current_file_node['rdt:name'] = script
    current_file_node['rdt:type'] = "File"
    keys = ['rdt:scope', "rdt:fromEnv", "rdt:timestamp", "rdt:location"]
    values = ["undefined", "FALSE", "", ""]
    for i in range (0, len(keys)):
        current_file_node[keys[i]] = values[i]

    split_path_file = current_link_dict['name'].split("/")

    # set value/relative path according to file's parent directory
    try:
        if split_path_file[1] == "results":
            current_file_node['rdt:value'] = script # if result/in results dir
        elif split_path_file[1] == "data":
            current_file_node['rdt:value'] = "." + current_link_dict['name']
        else:
            # if not in data or results, put entire path
            current_file_node['rdt:value']= current_link_dict['name']

    # avoid errors if the file name is not a full path and put entire path
    except:
        current_file_node['rdt:value']= current_link_dict['name']

    # add file node
    dkey_string = "d" + str(d_count)
    d_count+=1
    result["entity"][dkey_string] = current_file_node

    # add to dict of edges to make connections b/w graphs
    data_dict[script] = dkey_string

    return d_count, dkey_string

def add_file_edge(current_p, dkey_string, e_count, current_link_dict, result, activation_id_to_p_string, s, h, path_array, first_step, outfiles):
    """ adds a file edge, called by add_file """

    # make edge
    current_edge_node = {}
    current_edge_node['prov:activity'] = current_p
    current_edge_node['prov:entity'] = dkey_string

    # add edge
    e_string = "e" + str(e_count)
    e_count+=1

    if current_link_dict['mode'] == "r":
        result['used'][e_string] = current_edge_node
    else:
        result['wasGeneratedBy'][e_string] = current_edge_node
        # if file created, add to outfiles dict for linking graphs
        inner_dict = {'data_node_num': dkey_string, 'source': activation_id_to_p_string[s[1]], 'hash_out': h}
        outer_dict = {path_array[-1] : inner_dict}
        outfiles[first_step[2]] = outer_dict

def add_file(result, files, d_count, e_count, current_p, s, outfiles, first_step, activation_id_to_p_string, data_dict):
    """ uses files dict to add file nodes and access edges to the dictionary
    uses outfiles dict to check if file already exists from a previous script """

    dkey_string = -1

    # get file_name
    current_link_dict = files[s[1]]
    path_array = current_link_dict['name'].split("/")

    #get hash
    file_entry = files[s[1]]
    h = file_entry['hash']

    if len(outfiles.keys()) !=0:
    # if not first script, check to see if the file already has a node using name and hash
        for script in outfiles.keys():
                for outfile in outfiles[script]:
                    # if already seen
                    if outfile == path_array[-1] and outfiles[script][outfile]['hash_out']==h:
                        # do not add new node, but return d_key_string
                        dkey_string = data_dict[path_array[-1]]

        if dkey_string == -1: # if not seen yet, add node
            d_count, dkey_string = add_file_node(path_array[-1], current_link_dict, d_count, result, data_dict)
        # add new dependent edge
        add_file_edge(current_p, dkey_string, e_count, current_link_dict, result, activation_id_to_p_string, s, h, path_array, first_step, outfiles)

    # if first script, add file nodes w/o checking prior existence
    else:
        d_count, dkey_string = add_file_node(path_array[-1], current_link_dict, d_count, result, data_dict)
        add_file_edge(current_p, dkey_string, e_count, current_link_dict, result, activation_id_to_p_string, s, h, path_array, first_step, outfiles)

    return d_count, e_count

def add_data_edge(result, s, d_count, e_count, current_p):
    """ makes intermediate data node if process had return value """

    # make data node
    current_data_node = {}
    current_data_node['rdt:name'] = "data"
    current_data_node['rdt:type'] = "Data"
    current_data_node['rdt:scope'] = "R_GlobalEnv"
    keys = ["rdt:fromEnv", "rdt:timestamp", "rdt:location"]
    values = ["FALSE", "", ""]
    for i in range (0, len(keys)):
        current_data_node[keys[i]] = values[i]

    # set return value if it exists
    if s[3]!=None:
        current_data_node['rdt:value'] = s[3]
    else:
        current_data_node['rdt:value'] = "None"

    # add data node
    dkey_string = "d" + str(d_count)
    d_count+=1
    result["entity"][dkey_string] = current_data_node

    # make edge
    current_edge_node = {}
    current_edge_node['prov:activity'] = current_p
    current_edge_node['prov:entity'] = dkey_string

    # add edge
    e_string = "e" + str(e_count)
    e_count+=1
    result['wasGeneratedBy'][e_string] = current_edge_node

    return d_count, e_count, dkey_string

def get_arguments_from_sql(input_db_file, return_value, run_num, activation_id_to_p_string):
    """ queries sql database to find functions dependent on intermediate return value
    returns the process_string of these processes """

    target_processes = []
    db = sqlite3.connect(input_db_file, uri=True)
    c = db.cursor()

    c.execute('SELECT trial_id, value, function_activation_id from object_value where trial_id = ? and value = ?', (run_num, return_value, ))
    all_dep_processes = c.fetchall()

    # get all dependent processes and convert to p_string
    for p in all_dep_processes:
        process = p[2]
        p_string = activation_id_to_p_string[process]
        target_processes.append(p_string)

    return target_processes

def int_data_to_process(dkey_string, process_string, e_count, result):
    """ adds edge from intermediate data node to dependent process node """

    # make edge
    current_edge_node = {}
    current_edge_node['prov:activity'] = process_string
    current_edge_node['prov:entity'] = dkey_string

    # add edge
    e_string = "e" + str(e_count)
    e_count+=1
    result['used'][e_string] = current_edge_node

    return e_count

def make_dict(script_steps, files, input_db_file, run_num, func_ends, end_funcs, p_count, d_count, e_count, outfiles, result, data_dict, finish_node, script_name, loop_dict):
    """ uses the information from the database
    to make a dictionary compatible with Prov-JSON format

    1. Get Defaults and start node
    2. Loop through script_steps
        a. Make process nodes
        b. Check and add file acccesses and edges
        c. Check and add intermediate data values and edges
        d. Make informs edges
    3. Make finish node and final informs edge
    """

    # if first script in list, set up the default formats
    if len(result.keys()) == 0:
        result = get_defaults(script_name)

    # if not first script, add informs edge between
    # the Finish of the previous script and the Start of the current script
    if finish_node!= None:
        current_p = "p" + str(p_count)
        e_count = add_informs_edge(result, finish_node, current_p, e_count)

    # initialize per-script variables
    process_stack, int_values, int_dkey_strings, dkey_string, activation_id_to_p_string, loop_name_stack = [], [], [], -1, {}, []
    prev_p, p_count = add_start_node(result, script_steps[0], p_count)
    process_stack.append(script_steps[0][4])
    current_line = ""

    # iterate through each line in the script
    for i in range (1, len(script_steps)):
        s = script_steps[i]

        # get the line of the script
        next_line=""
        with open(script_name) as f:
            # subtract 1 from s[4] because script_steps starts as [1] to avoid redundant start node
            for i, line in enumerate(f):
                if i == s[4]-1:
                    next_line = line
                elif i > s[4]-1:
                    break

        # if current step is a function, add start node
        # store the function_activation_id in stack to be able to make Finish node
        if s[2] in func_ends:
            current_p, p_count = add_start_node(result, s, p_count)
            process_stack.append(func_ends[s[2]])

        # if current_step is the start of a for or while loop, add start node
        # store the last line in loop in stack to be able to make Finish node
        elif s[4] in loop_dict.keys():
            current_p, p_count = add_start_node(result, s, p_count, next_line.strip())
            process_stack.append(loop_dict[s[4]])
            loop_name_stack.append(next_line.strip())

        # if function or loop has ended on current step, add finish node
        # need to make this == process_stack.
        elif s[4] >= process_stack[-1]:

            if len(loop_name_stack) == 0: # if end_line function/loop reached, but function/loop never called, add normal process node
                p_count, current_p = add_process(result, s[2], p_count, s, script_name, next_line)
            else:
                try:  # function end
                    func_name = end_funcs[s[4]]
                except:
                    try: # loop end
                        func_name = loop_name_stack.pop()
                    except:
                        pass

                current_p, p_count = add_end_node(result, p_count, func_name)
                process_stack.pop()

                # add informs edge between last process node in loop and the finish node of the loop
                e_count = add_informs_edge(result, prev_p, current_p, e_count)
                prev_p = "p" + str(p_count-1)

                # after adding finish node, add current node as a normal process node
                # TO DO: what if current node is another loop/file io/etc?
                p_count, current_p = add_process(result, s[2], p_count, s, script_name, next_line)

        # if no special cases, add normal process node
        else:
            p_count, current_p = add_process(result, s[2], p_count, s, script_name, next_line)

        # dict for use in get_arguments_from_sql
        activation_id_to_p_string[s[1]] = current_p

        # if process node reads or writes to file, add file nodes and edges
        # TO DO: read file not detected unless with open() as f format.
        if s[1] in files.keys():
            d_count, e_count = add_file(result, files, d_count, e_count, current_p, s, outfiles, script_steps[0], activation_id_to_p_string, data_dict)

        # if process node has return statement, make intermediate data node and edges
        if s[3] != "None":
            d_count, e_count, dkey_string = add_data_edge(result, s, d_count, e_count, current_p)
            int_values.append(s[3])
            int_dkey_strings.append(dkey_string)

        # add_informs_edge between all process nodes
        e_count = add_informs_edge(result, prev_p, current_p, e_count)
        prev_p = "p" + str(p_count-1)

    # after all steps in script done
    # add finish nodes and informs edges for the rest of the process_stack
    while len(process_stack)>1:
        func_line = process_stack.pop()
        func_name = end_funcs[func_line]
        current_p, p_count = add_end_node(result, p_count, func_name)
        e_count = add_informs_edge(result, prev_p, current_p, e_count)
        prev_p = "p" + str(p_count-1)

    # add finish node and final informs edge for the script
    current_p, p_count = add_end_node(result, p_count, script_steps[0][2])
    e_count = add_informs_edge(result, prev_p, current_p, e_count)

    # adds used edges using dependencies from database table: object_value
    for i in range (0, len(int_values)):
        print(i) #52309
        return_value = int_values[i]
        target_processes = get_arguments_from_sql(input_db_file, return_value, run_num, activation_id_to_p_string)
        for process in target_processes:
            e_count = int_data_to_process(int_dkey_strings[i], process, e_count, result)

    return result, p_count, d_count, e_count, outfiles, current_p

def get_loop_locations(script_name):
    """ uses ast module to find the start and end lines of for and while loops
    to allow for collapsible nodes for loops (as well as functions) """

    loop_dict = {}

    with open(script_name) as f:
        tree = ast.parse(f.read())

    for node in ast.walk(tree):
        if isinstance(node, (ast.For, ast.While)):
            # keys = start line, values = finish line
            # offset by 1 to match with script_steps numbering
            loop_dict[node.lineno] = node.body[-1].lineno+1

    return loop_dict

def write_json(dictionary, output_json_file):
    with open(output_json_file, 'w') as outfile:
        json.dump(dictionary, outfile)

def link_DDGs(trial_num_list, input_db_file, output_json_file):
    """ input: db_file generated by noworkflow
    target path where the Prov-JSON file will be written
    and a list of trial numbers that will be linked together into a DDG
    where trial numbers correspond to individual scripts stored in the noworkflow database

    output: prov-json file that can be opened in DDG Explorer
    """

    # initialize variables that will carry over from 1 script to the next
    p_count, d_count, e_count = 1, 1, 1
    result, outfiles, data_dict = {}, {}, {}
    finish_node = None

    # for each trial, query and add to the result
    for trial_num in trial_num_list:
        script_steps, files, func_ends, end_funcs, script_name = get_info_from_sql(input_db_file, trial_num)
        loop_dict = get_loop_locations(script_name)
        result, p_count, d_count, e_count, outfiles, finish_node = make_dict(script_steps, files, input_db_file, trial_num, func_ends, end_funcs, p_count, d_count, e_count, outfiles, result, data_dict, finish_node, script_name, loop_dict)

    # Write to file
    write_json(result, output_json_file)

def main():

    # TO DO: how to get these paths?
    input_db_file = '/Users/jen/Desktop/newNow/scripts/.noworkflow/db.sqlite'
    output_json_file = "/Users/jen/Desktop/newNow/results/testJ.json"

    # TO DO: how to get these from now list, how to make sure they are in order?
    trial_num_list = [13]

    link_DDGs(trial_num_list, input_db_file, output_json_file)

    # TO DO: how to open DDG Explorer automatically?
    # TO DO: pretty string formatting

if __name__ == "__main__":
    main()
