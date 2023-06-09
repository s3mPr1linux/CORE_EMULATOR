import argparse
import re
from io import TextIOWrapper


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Helps transition older CORE services to work with newer versions"
    )
    parser.add_argument(
        "-f",
        "--file",
        dest="file",
        type=argparse.FileType("r"),
        help="service file to update",
    )
    return parser.parse_args()


def update_service(service_file: TextIOWrapper) -> None:
    update = []
    for line in service_file.readlines():
        # update service attributes
        line = re.sub(r"^(\s+)_([a-z])", r"\1\2", line)
        # rename dirs to directories
        line = re.sub(r"^(\s+)dirs", r"\1directories", line)
        # fix import states for service
        line = re.sub(
            r"^.+import.+CoreService.+$",
            r"from core.services.coreservices import CoreService",
            line,
        )
        # fix method signatures
        line = re.sub(
            r"def generateconfig\(cls, node, filename, services\)",
            r"def generate_config(cls, node, filename)",
            line,
        )
        line = re.sub(
            r"def getvalidate\(cls, node, services\)",
            r"def get_validate(cls, node)",
            line,
        )
        line = re.sub(
            r"def getstartup\(cls, node, services\)",
            r"def get_startup(cls, node)",
            line,
        )
        line = re.sub(
            r"def getconfigfilenames\(cls, nodenum, services\)",
            r"def get_configs(cls, node)",
            line,
        )
        # remove unwanted lines
        if re.search(r"addservice\(", line):
            continue
        if re.search(r"from.+\.ipaddr|import ipaddr", line):
            continue
        if re.search(r"from.+\.ipaddress|import ipaddress", line):
            continue
        # add modified line to make updated copy
        update.append(line)
    service_file.close()

    with open(f"{service_file.name}.update", "w") as f:
        f.writelines(update)


if __name__ == "__main__":
    args = parse_args()
    update_service(args.file)
