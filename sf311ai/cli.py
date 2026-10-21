import argparse
import json

from sf311ai.workflows import process_images_and_report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Detect issues; preview by default"
    )
    parser.add_argument("config", nargs="?", default="config.yaml")
    parser.add_argument("images", nargs="?", default="images/")
    parser.add_argument(
        "--submit",
        action="store_true",
        help="Submit with explicit image_locations",
    )
    args = parser.parse_args()
    print(
        json.dumps(
            process_images_and_report(
                args.config, args.images, submit=args.submit
            )
        )
    )
