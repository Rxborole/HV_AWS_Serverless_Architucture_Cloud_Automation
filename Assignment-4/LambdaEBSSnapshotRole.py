import boto3
from datetime import datetime, timezone, timedelta

ec2 = boto3.client('ec2')

VOLUME_ID = "vol-xxxxxxxxxxxxxxxxx"

def lambda_handler(event, context):

    created_snapshots = []
    deleted_snapshots = []

    # Create Snapshot
    snapshot = ec2.create_snapshot(
        VolumeId=VOLUME_ID,
        Description='Automated Backup by Lambda'
    )

    snapshot_id = snapshot['SnapshotId']

    created_snapshots.append(snapshot_id)

    print(f"Created Snapshot: {snapshot_id}")

    # Find snapshots older than 30 days
    retention_date = datetime.now(timezone.utc) - timedelta(days=30)

    snapshots = ec2.describe_snapshots(
        OwnerIds=['self']
    )

    for snap in snapshots['Snapshots']:

        if snap['VolumeId'] == VOLUME_ID:

            start_time = snap['StartTime']

            if start_time < retention_date:

                ec2.delete_snapshot(
                    SnapshotId=snap['SnapshotId']
                )

                deleted_snapshots.append(
                    snap['SnapshotId']
                )

                print(
                    f"Deleted Snapshot: {snap['SnapshotId']}"
                )

    return {
        'statusCode': 200,
        'created_snapshots': created_snapshots,
        'deleted_snapshots': deleted_snapshots
    }