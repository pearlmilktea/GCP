
from google.cloud import monitoring_v3

class MetricDescriptorViewer:
    """
    Répertorie les metriques surveillées
    La methode list_metric_descriptors() retourne la liste exhaustive
    "'custom.googleapis.com/my_metric' est un exemple de Metric Descriptor
    """
    def __init__(self, project_id:str) -> None:
        self.project_id=project_id

    def _get_metric_descriptors(self) -> None:
        client = monitoring_v3.MetricServiceClient()
        project_name = f"projects/{self.project_id}"

        list_descriptor=[]
        for descriptor in client.list_metric_descriptors(name=project_name):
            list_descriptor.append(descriptor.type)
        return list_descriptor

    def list_metric_descriptors(self) -> []:
        "Liste des metric_descriptor"
        for descriptor in self._get_metric_descriptors():
            print(descriptor)

    def get_metric_descriptor(self, metric_name:str) -> None:
        client = monitoring_v3.MetricServiceClient()
        descriptor = client.get_metric_descriptor(name=f'projects/{self.project_id}/metricDescriptors/{metric_name}')
        print(descriptor)

def main():
    import os
    project_id=os.environ["GOOGLE_CLOUD_PROJECT"]

    descriptor=MetricDescriptorViewer(project_id)
    print('=====================================') 
    descriptor.list_metric_descriptors()
    print('=====================================') 
    descriptor.get_metric_descriptor('custom.googleapis.com/in_gcs_images')

if __name__ == '__main__':
    main()

