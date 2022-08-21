
from google.cloud import monitoring_v3

class RessourceDescriptorViewer:
    "Répertorie les ressources surveillées"
    def __init__(self, project_id:str) -> None:
        self.project_id=project_id

    def list_monitored_resources(self) -> None:
        "Liste actuelle des types de ressources surveillées à partir de l'API Monitoring"
        client = monitoring_v3.MetricServiceClient()
        project_name = f"projects/{self.project_id}"
        resource_descriptors = client.list_monitored_resource_descriptors(name=project_name)
        for descriptor in resource_descriptors:
            print(descriptor.type)

    def get_monitored_resource_descriptor(self, resource_type_name:str) -> None:
        "Obtenir des descripteurs de ressources"
        client = monitoring_v3.MetricServiceClient()
        resource_path = (
            f"projects/{self.project_id}/monitoredResourceDescriptors/{resource_type_name}"
        )
        print(client.get_monitored_resource_descriptor(name=resource_path))

def main():
    import os
    project_id=os.environ["GOOGLE_CLOUD_PROJECT"]

    descriptor=RessourceDescriptorViewer(project_id)
    print('=====================================') 
    descriptor.list_monitored_resources()
    print('=====================================') 
    descriptor.get_monitored_resource_descriptor('gce_instance')
    #descriptor.get_monitored_resource_descriptor('global')

if __name__ == '__main__':
    main()

