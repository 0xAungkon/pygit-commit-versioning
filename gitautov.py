#!/usr/bin/env python3

import subprocess
import sys

# Function to calculate the next version number based on the last commit message.
def return_next_version():
    # Run git log command to get the last commit message
    result = subprocess.run(['git', 'log', '-1', '--pretty=%B'], capture_output=True, text=True)
    last_commit_message = result.stdout.strip()

    # Extract version from the commit message if it contains a version pattern
    if ('-' in last_commit_message):
        version = last_commit_message.split('-')[0]  # Extract the part before the dash
        version = version.replace('v', '')          # Remove "v" prefix if present
    else:
        version = '0.0'                             # Default version if none found

    version = version.strip()                       # Clean up any extra whitespace

    # Convert the extracted version to a float
    try:
        version = float(version)
    except ValueError:
        version = 0.0                               # Default to 0.0 if conversion fails

    # Convert the version back to a string for processing
    version = str(version)

    # Determine the next version based on the presence of "-rel" in the arguments
    if ('-rel' in sys.argv):
        version_pre = int(version.split('.')[0]) + 1  # Increment the major version
        version_post = int(0)                        # Reset the minor version
    else:
        version_pre = int(version.split('.')[0])      # Keep the major version
        version_post = int(version.split('.')[1]) + 1 # Increment the minor version

    # Construct the new version string
    version = str(version_pre) + '.' + str(version_post)
    return version

# Check if the "-m" flag is provided in the arguments for the commit message
if '-m' in sys.argv:
    commit_msg = sys.argv[sys.argv.index('-m') + 1]    # Get the commit message from the arguments
else:
    commit_msg = input('Enter Commit Message: ')      # Prompt the user for the commit message

# Calculate the next version number
version = return_next_version()

# Append the version number to the commit message
commit_msg = version + ' - ' + commit_msg

# Stage all changes for commit
subprocess.run(['git', 'add', '.'])

# Show the git status
subprocess.run(['git', 'status'])

# Commit the changes with the constructed commit message
subprocess.run(['git', 'commit', '-m', commit_msg])

# Push the committed changes to the remote repository
subprocess.run(['git', 'push'])

# Print the final commit message
print('\n\nCommit Message: ' + commit_msg)