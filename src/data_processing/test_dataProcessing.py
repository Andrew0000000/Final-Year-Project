from dataProcessing import split_duties
# BEGIN: Test split_duties function

# Test case 1: Single duty without parentheses
duty1 = " Prepare lesson plans"
assert split_duties(duty1) == ["Prepare lesson plans"]

# Test case 2: Single duty without parentheses
duty2 = "Prepare lesson plans "
assert split_duties(duty2) == ["Prepare lesson plans"]

# Test case 3: Multiple duties separated by commas
duty3 = " Grade assignments, Provide feedback ,Conduct tutorials "
assert split_duties(duty3) == ["Grade assignments", "Provide feedback", "Conduct tutorials"]
