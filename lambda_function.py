import boto3

client = boto3.client("ecs")
MAX_PAGE = 10

def get_clusters():
  """
  Get list of ECS clusters
  """
  still_going = False
  arns = []
  response = client.list_clusters(
    maxResults = MAX_PAGE
  )
  arns = arns + response["clusterArns"]
  if "nextToken" in response:
    still_going = True
  while still_going:
    response = client.list_clusters(
      nextToken = response["nextToken"],
      maxResults = MAX_PAGE
    )
    if "nextToken" not in response:
      still_going = False
    arns = arns + response["clusterArns"]
  return arns

def get_instances(cluster_arn):
  """
  Get list of instances for a cluster
  """
  still_going = False
  arns = []
  response = client.list_container_instances(
    cluster = cluster_arn,
    maxResults = MAX_PAGE
  )
  arns = arns + response["containerInstanceArns"]
  if "nextToken" in response:
    still_going = True
  while still_going:
    response = client.list_container_instances(
      cluster = cluster_arn,
      nextToken = response["nextToken"],
      maxResults = MAX_PAGE
    )
    if "nextToken" not in response:
      still_going = False
    arns = arns + response["containerInstanceArns"]
  return arns

def update_instance(cluster_arn, instance_arn):
  """
  Updates agent on an instance to the latest version
  """
  try:
    client.update_container_agent(
      cluster = cluster_arn,
      containerInstance = instance_arn
    )
  except Exception as e:
    if "NoUpdateAvailableException" == e.__class__.__name__:
      print("    -> instance does not need an update")

def run():
  clusters = get_clusters()
  for cluster in clusters:
    print("** working on cluster: {}".format(cluster))
    instances = get_instances(cluster_arn = cluster)
    if len(instances) > 0:
      for instance in instances:
        print("  -> updating {}".format(instance))
        update_instance(
          cluster_arn = cluster,
          instance_arn = instance
        )
    else:
      print("  -> no instances in cluster")

if __name__ == "__main__":
  run()