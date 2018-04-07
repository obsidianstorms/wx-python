import argparse
import os
import lib.term_colors as cout
import sys
from subprocess import check_output, STDOUT

def main(args):
    DOCKER_NAME = args.docker

    # Environment Expectations
    current_dir = os.path.dirname(os.path.realpath(__file__))

    DIRECTORIES = [
        "{}/config".format(current_dir),
        "{}/log".format(current_dir),
        "{}/res".format(current_dir),
        "{}/docs".format(current_dir)
    ]

    TEMPLATES = {
        "secret": "{}/res/secrets.jtpl".format(current_dir)
    }

    FILES = {
        "secret": "{}/config/secrets.json".format(current_dir)
    }

    # Evaluate Environment Expectations
    for dir in DIRECTORIES:
        if os.path.isdir(dir):
            cout.print_info("Found {}".format(dir))
        else:
            cout.print_warn("Not found {}, attempting to create...".format(dir))
            try:
                os.makedirs(dir)
                cout.print_ok("Created {}".format(dir))
            except OSError:
                if not os.path.isdir(dir):
                    cout.print_fail("Failed to create {}".format(dir))
                    raise

    for type, file in FILES.items():
        if os.path.exists(file):
            cout.print_info("Found {}".format(file))
        else:
            cout.print_warn("Not found {}, attempting to create...".format(file))
            try:
                if type not in TEMPLATES:
                    cout.print_fail("Template {} not defined".format(type))
                    raise Exception("Template not defined.")
                if not os.path.exists(TEMPLATES[type]):
                    cout.print_fail("Template file {} not defined".format(TEMPLATES[type]))
                    raise Exception("Template file not defined.")
                cout.print_info("Found template {}".format(TEMPLATES[type]))
                with open(TEMPLATES[type], 'r') as f:
                    template = f.read()
                with open(file, 'w') as f:
                    template = f.write(template)
                cout.print_ok("Copied template to {}".format(file))
                cout.print_warn("Values need to be added to {}".format(file))
            except OSError:
                if not os.path.exists(file):
                    cout.print_fail("Failed to create {}".format(file))
                    raise


    command = "docker -v"
    try:
        response = check_output(
            command,
            stderr=STDOUT,
            shell=True
        )
        if "Docker version" not in response:
            cout.print_fail("Docker not found. Please install.")
            raise Exception("Docker not found. Please install.")
        cout.print_info("Docker found.")
    except Exception as e:
        cout.print_fail("Failed to determine docker availability.")
        raise


    command = "cd docker && docker image build -t {} .".format(DOCKER_NAME)
    try:
        response = check_output(
            command,
            stderr=STDOUT,
            shell=True
        )
        cout.print_ok("Docker image built {}.".format(DOCKER_NAME))
    except Exception as e:
        cout.print_fail("Failed to build docker image {}".format(DOCKER_NAME))
        raise



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('docker')
    args = parser.parse_args()
    try:
        sys.exit(main(args))
    except KeyboardInterrupt:
        cout.print_warn("Keyboard interruption")
        sys.exit(1)
    except Exception as e:
        error_msg = "Runtime failed: {}: {}: {}"
        msg = error_msg.format(__file__, e, sys.exc_info()[0])
        cout.print_fail(msg)
        sys.exit(1)
