import boto3
from ec2_metadata import ec2_metadata
import logging
import time

import main
from src.notifier import Notifier


def aws_main():
    main.setupLogging()

    instance_id = ec2_metadata.instance_id
    try:
        tags = ec2_metadata.tags
        if tags.__getitem__('strategy') == 'dev':
            return
    except Exception:
        logging.info('No tags found, continuing')

    curr_time = time.time()

    args = main.argumentParser()
    notifier = Notifier(args)
    loaded_accounts = main.setupAccounts()

    notifier.send(
        "\n".join(
            [
                "-------------------------------------------------",
                "Microsoft Rewards Farmer",
                f"Instance: {instance_id}",
                f"Loaded {len(loaded_accounts)} accounts",
                "-------------------------------------------------",
            ]
        )
    )

    for currentAccount in loaded_accounts:
        try:
            main.executeBot(currentAccount, notifier, args)
        except Exception as e:
            logging.exception(f"{e.__class__.__name__}: {e}")

    end_time = time.time()
    runtime = end_time - curr_time
    hours, remainder = divmod(runtime, 3600)
    minutes, seconds = divmod(remainder, 60)
    runtime_str = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))

    notifier.send(
        "\n".join(
            [
                "-------------------------------------------------",
                "Microsoft Rewards Farmer",
                f"Instance: {instance_id}",
                f"Finished {len(loaded_accounts)} accounts",
                f"Runtime: {runtime_str} seconds",
                "Shutting down instance",
                "-------------------------------------------------",
            ]
        )
    )

    client = boto3.client('ec2', region_name=ec2_metadata.region)
    client.stop_instances(InstanceIds=[instance_id])


if __name__ == '__main__':
    aws_main()
