import os
import boto3

# Configure your AWS credentials
# You can either set environment variables AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY or configure using `aws configure` command.
# https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html

# Initialize boto3 client
ec2 = boto3.client("ec2")


def increment_cidr_block(cidr_block):
    ip, subnet = cidr_block.split('/')
    ip_parts = ip.split('.')
    for i in reversed(range(len(ip_parts))):
        ip_parts[i] = int(ip_parts[i]) + 1
        if ip_parts[i] <= 255:
            break
        ip_parts[i] = 0
    return '.'.join(str(part) for part in ip_parts) + '/' + subnet


def find_available_cidr_block(cidr_block):
    # Get all VPCs
    response = ec2.describe_vpcs()
    existing_vpcs = response["Vpcs"]

    # Extract the CIDR blocks of existing VPCs
    existing_cidr_blocks = [vpc["CidrBlock"] for vpc in existing_vpcs]

    # Find an available CIDR block
    current_cidr_block = cidr_block
    while current_cidr_block not in existing_cidr_blocks:
        return current_cidr_block
    else:
        current_cidr_block = increment_cidr_block(current_cidr_block)

    # If no CIDR block is available, return None
    return None


if __name__ == "__main__":
    start_cidr_block = "1.0.0.0/16"
    available_cidr_block = find_available_cidr_block(start_cidr_block)
    if available_cidr_block:
        print(f"Available CIDR block: {available_cidr_block}")
    else:
        print("No available CIDR block found.")
