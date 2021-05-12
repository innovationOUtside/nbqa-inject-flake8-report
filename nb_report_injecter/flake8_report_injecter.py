import nbformat

def flake8_report_insertion(report_file, overwrite=False, tags=True):
    """Parse flake8 report file into notebook output cells."""

    # Read in report file generate as eg:
    # nbqa flake8 notebooks/*.ipynb > flake8_reports.txt
    with open(report_file, 'r') as f:
        lines = f.read().splitlines() 


    # Generate reports at notebook item level
    items = {}
    # Will take form:
    # items[path] = [['cell_1', '0', '1', ' D100 Missing docstring in public module'],
    #                ['cell_5', '1', '80', ' E501 line too long (85 > 79 characters)'],

    # Iterate through report lines
    for l in lines:
        parts = l.split(':')
        if parts[0] not in items:
            items[parts[0]] = [parts[1:]]
        else:
            items[parts[0]].append( parts[1:] )

    # Iterate through filenames of notebooks with flake8 errors
    for fn in items:

        # Read notebook
        with open(fn, 'r') as f:
            nb = nbformat.read(f, nbformat.NO_CONVERT)

            # Maintain a count of code cells
            code_i = 0

            reports = {}
            # Will take form: {code_cell_number: error_list}
            # {1: ['0:1: D100 Missing docstring in public module\n'],
            #  5: ['1:80: E501 line too long (85 > 79 characters)\n',
            #      '2:80: E501 line too long (113 > 79 characters)\n']}
            
            # Create reports keyed by notebook listing errors for that notebook
            for r in items[fn]:
                # Get code cell number
                k = int(r[0].split('_')[-1])
                # Get report items
                report = ':'.join(r[1:])+'\n'
                if k not in reports:
                    reports[k] = []
                # Build report list by code_cell_number
                reports[k].append(report)

            # Enumerate through cells
            for i, cell in enumerate(nb['cells']):
                # We'll capture error codes per cell
                error_tags = []
                
                #For each code cell
                if cell['cell_type']=='code':
                    # Increment code cell counter
                    code_i = code_i + 1

                    # If ewe have reports for that code cell
                    if code_i in reports:
                        # Generate a cell output containing reports
                        _out = nbformat.v4.new_output('stream')
                        _out['text'] = reports[code_i]
                        _out["name"]= "stderr"
                        
                        # Add reports to cell output
                        nb['cells'][i]["outputs"] = [_out]
                        # Capture error code into list
                        error_tags = error_tags + ['flake8-error-'+t.split(':')[2].strip().split()[0] for t in reports[code_i]]
                    else:
                        # Clear cell output if no report
                        nb['cells'][i]["outputs"] = []

                    # Create unique list of error codes
                    # (We might also count them?)
                    error_tags = list(set(error_tags))
                    # If we have error codes and we want tags:
                    if tags and error_tags:
                        # Add a generic tag
                        error_tags.append('flake8-error')
                        # Add tags to cell
                        if 'tags' in nb['cells'][i]["metadata"]:
                            nb['cells'][i]["metadata"]['tags'] =  nb['cells'][i]["metadata"]['tags'] + error_tags
                        else:
                            nb['cells'][i]["metadata"]['tags'] = error_tags

        # Create output filename
        out_fn = fn if overwrite else fn.replace('.ipynb', '_flake8.ipynb')
    
        # Write out annotated notebook
        with open(out_fn, 'w') as f_out:         
            nbformat.write(nb, f_out, nbformat.NO_CONVERT)


