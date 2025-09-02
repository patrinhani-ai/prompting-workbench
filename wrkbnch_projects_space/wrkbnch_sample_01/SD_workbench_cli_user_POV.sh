# runner

# Current ------------------------------------------------------

# Run all prompts of the "wrkbnch_sample_01" project
pdm run prompting_workbench run wrkbnch_sample_01

# Run a specific prompt of the "wrkbnch_sample_01" project
pdm run prompting_workbench run wrkbnch_sample_01 -P 01-01--sample_prompt

# Run the test (eval) for specific prompt of the "wrkbnch_sample_01"
pdm run prompting_workbench run wrkbnch_sample_01 -P 01-01--sample_prompt --test

# New ------------------------------------------------------

# Run all prompts of the "wrkbnch_sample_01" project
pdm run prompting_workbench runnner wrkbnch_sample_01

# Run a specific prompt of the "wrkbnch_sample_01" project
pdm run prompting_workbench runner wrkbnch_sample_01 -P 01-01--sample_prompt

# Run the test (eval) for specific prompt of the "wrkbnch_sample_01"
pdm run prompting_workbench eval wrkbnch_sample_01 -P 01-01--sample_prompt --test


-----------

# flow_web

# Current ------------------------------------------------------

# Run the flow_web integration for specific prompt of the "wrkbnch_sample_01" project
pdm run prompting_workbench flow_web wrkbnch_sample_01 -P 01-01--sample_prompt --prompts-push --debug

# New ------------------------------------------------------

# Deployment of the default profile only
pdm run prompting_workbench flow_web wrkbnch_sample_01 -P 01-01--sample_prompt --push --debug

# Deployment of the custom-01 profile only
pdm run prompting_workbench flow_web wrkbnch_sample_01 -P 01-01--sample_prompt --push --profile custom-01 --debug

# Deployment of the multiple profiles
pdm run prompting_workbench flow_web wrkbnch_sample_01 -P 01-01--sample_prompt --push --profile default, custom-01 --debug
