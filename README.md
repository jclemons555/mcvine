# Download McVine Dependency File:
[mcvine-dev.yml](mcvine-dev.yml)

# create conda environment dev-mcvine with deps:
$ conda env create -f mcvine-dev.yml --solver=libmamba

# activate the environment:
$ conda activate mcvine-dev

# Clone McVine to Local System:
$ mkdir -p ~/dv/mcvine

$ cd ~/dv/mcvine

$ git clone https://github.com/mcvine/mcvine.git

$ git clone https://github.com/mcvine/resources.git

# env var shell script:
envs.sh file: 
# download and move shell script to your local mcvine directory:
[envs.sh](envs.sh)   <br>
after downloading the script, place it in the /dv/mcvine/. after successfully moving the script, ensure that you are in the /dv/mcvine/ directory via terminal.
# run shell script:
use this command to run script:
$ . envs.sh

# Build and install for the first time:
$ build0

# Test:
$ mt

# Addressing Failed Tests: 
After building McVine and testing, 7/300 of the tests failed.

# 10 - instrument/instrument/factories/ARCSBootstrap_TestCase (Failed):
Explaination:
The error message TypeError: sort() takes no positional arguments suggests that the sort() method is being called incorrectly in your code. In Python, the sort() method for lists does not take positional arguments for comparing elements directly. Instead, it uses a key function or relies on the natural ordering of elements, depending on how it's called.

The specific line causing the error is: 
records.sort( lambda x,y: x[0]-y[0] )
To fix this issue, modify the sorting line to use a key function that extracts the element to be sorted:
records.sort(key=lambda x: x[0])

# 20 - instrument/instrument/geometry/yaml/parser_TestCase (Failed)

Explanation
The TypeError: load() missing 1 required positional argument: 'Loader' error occurs because in recent versions of PyYAML, the yaml.load() function requires an explicit Loader argument to be specified. This is a security measure to prevent arbitrary code execution vulnerabilities that can arise from using the default yaml.load() function.

Potential Changes
parse_file function:

    - Add  d = yaml.load(open(path), Loader=yaml.Loader)
    - Use context manager (with statement): This ensures the file is properly closed after reading, avoiding ResourceWarning.

# 21 - instrument/instrument/geometry/yaml/renderer_TestCase (Failed)
The error in your test renderer_TestCase is due to the yaml.load function missing the required positional argument 'Loader'. This is a common issue with PyYAML versions starting from 5.1, where the yaml.load function requires an explicit Loader argument for security reasons.

    - Add  d = yaml.load(open(path), Loader=yaml.Loader)
    - Use context manager (with statement): This ensures the file is properly closed after reading, avoiding ResourceWarning.

# 55 - mcni/mcni/pyre_support/journal_simapp_TestCase (Failed)


# 63 - mcni/mcni/pyre_support/journal_TestCase (Failed)

The AssertionError in your test indicates that the expected output string is not found in the actual output of the program. 

# 102 - libmccomposite/geometry/test_intersect.cc (Subprocess aborted)
The error message indicates that there is a failed assertion in the test2() function in your test_intersect.cc file, specifically where it is expecting find_1st_hit< int >( start, direction, shapes ) to equal 1. This suggests there is either a logical error in the find_1st_hit function or the test setup itself.

# 108 - libmccomposite/mccomposite/test_neutron_propagation.cc (Subprocess aborted)

The error message you are seeing indicates that a neutron propagation event is causing an exception because the neutron is already inside the shape it is supposed to propagate into. This might be due to incorrect initialization or a logical error in the propagation code.
