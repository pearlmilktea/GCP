from google.cloud import monitoring_v3
from google.api import label_pb2 as ga_label
from google.api import metric_pb2 as ga_metric

from collections import namedtuple
from collections import defaultdict
import time

"1) RESSOURCE DESCRIPTOR : correspond a la recherche Ressource dans 'Explorateur de metriques'"
RessourceDescriptor = namedtuple( 'RessourceDescriptor', ['resource_type', 'zone'] )

"""
2) METRIC DESCRIPTOR : correspond a la recherche Metric, quand on a clique sur Ressource dans 'Explorateur de metriques'
    type
        exemple avec type='my_metric' : cela va creer 'custom.googleapis.com/my_metric'"
    description
        décrit la ressource active quand on laisse la souris sur custom/my_metric
"""
MetricDescriptor = namedtuple( 'MetricDescriptor', ['description', 'type'] )

"3) LABEL DESCRIPTOR : apparait dans le menu filtre associe au titre & description du label"
LabelDescriptor = namedtuple( 'LabelDescriptor', ['labelKey', 'description'] )


class CustomMetricModel():
    "Permet la creation de custom metriques dans cloud monitoring"
    def __init__(self, project_id, resource_descriptor, metric_descriptor, label_descriptor) -> None:
        self.client = monitoring_v3.MetricServiceClient()
        self.project_name = f"projects/{project_id}"
        self.resource_descriptor=resource_descriptor
        self.metric_descriptor=metric_descriptor
        self.label_descriptor=label_descriptor

    def create_metric_descriptor(self) -> None:
        "Creation du metric descriptor"
        descriptor = ga_metric.MetricDescriptor()
        descriptor.type = f"custom.googleapis.com/{self.metric_descriptor.type}"
        descriptor.metric_kind = ga_metric.MetricDescriptor.MetricKind.GAUGE
        descriptor.value_type = ga_metric.MetricDescriptor.ValueType.DOUBLE
        descriptor.description = self.metric_descriptor.description

        labels = ga_label.LabelDescriptor()
        labels.key = self.label_descriptor.labelKey
        labels.value_type = ga_label.LabelDescriptor.ValueType.STRING
        labels.description = self.label_descriptor.description
        descriptor.labels.append(labels)

        descriptor = self.client.create_metric_descriptor(
            name=self.project_name, metric_descriptor=descriptor
        )
        print(f"Created {descriptor.name}")

    def write_time_series(self, label_name:str, value:float) -> None:
        "Ecriture en serie temporelle basee sur un label que lon specifie"
        series = monitoring_v3.TimeSeries()
        series.metric.type = f"custom.googleapis.com/{self.metric_descriptor.type}"
        series.resource.type = self.resource_descriptor.resource_type
        if self.resource_descriptor=="gce_instance":
            series.resource.labels["instance_id"] = "1234567890123456789"
        if self.resource_descriptor.zone is not None:
            series.resource.labels["zone"] = self.resource_descriptor.zone
        series.metric.labels[self.label_descriptor.labelKey] = label_name

        now = time.time()
        seconds = int(now)
        nanos = int((now - seconds) * 10 ** 9)
        interval = monitoring_v3.TimeInterval(
            {"end_time": {"seconds": seconds, "nanos": nanos}}
        )
        
        point = monitoring_v3.Point({"interval": interval, "value": {"double_value": value}})
        series.points = [point]
        self.client.create_time_series(name=self.project_name, time_series=[series])

def main(): 
    import os
    project_id=os.environ["GOOGLE_CLOUD_PROJECT"]

    "Parametres de la custom metrique qu on va cree"
    resource_descriptor=RessourceDescriptor("global", None)
    metric_descriptor=MetricDescriptor("Describe the volumetry variation in gcs buckets", "GCS/custom_blob_volumetry")
    label_descriptor=LabelDescriptor("blob_volumetry", "Volumetry metrics of gcs blobs")

    "On la cree"
    custom=CustomMetricModel(project_id, resource_descriptor, metric_descriptor, label_descriptor)
    custom.create_metric_descriptor()

    "Rajout de la metrique basee sur un label associe sur le label descriptor qu on a cree"
    custom.write_time_series("average",3.14)


if __name__ == '__main__':
    main()