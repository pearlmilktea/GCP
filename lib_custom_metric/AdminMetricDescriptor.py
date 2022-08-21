from MetricDescriptorViewer import MetricDescriptorViewer
from google.cloud import monitoring_v3

class AdminMetricDescriptor(MetricDescriptorViewer):
    """
    Management des Metric Descriptor
    La methode list_metric_descriptors() retourne la liste exhaustive
    "'custom.googleapis.com/my_metric' est un exemple de Metric Descriptor
    """

    def __init__(self, project_id:str) -> None:
        self.project_id=project_id

    def delete_metric_descriptor(self, descriptor_name:str) -> None:
        "Suppression du metric_descriptor specifie"
        if descriptor_name not in self._get_metric_descriptors():
            print("Metric descriptor {} is already deleted".format(descriptor_name))
        else:
            client = monitoring_v3.MetricServiceClient()
            client.delete_metric_descriptor(name=f'projects/{self.project_id}/metricDescriptors/{descriptor_name}')
            print("Deleted metric descriptor {}.".format(descriptor_name))


def main():
    import os
    project_id=os.environ["GOOGLE_CLOUD_PROJECT"]
    
    descriptor=AdminMetricDescriptor(project_id)
    print('=====================================') 
    descriptor.list_metric_descriptors()
    #print('=====================================') 
    #descriptor.delete_metric_descriptor('custom.googleapis.com/my_metric')

if __name__ == '__main__':
    main()
