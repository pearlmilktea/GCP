from google.cloud import monitoring_v3
import time

class TimeSeriesViewer():
    "Répertorie les series temporelles"
    def __init__(self, project_id:str, descriptor_name:str) -> None:
        self.project_id=project_id
        self.descriptor_name=descriptor_name

    def list_time_series(self) -> None:
        client = monitoring_v3.MetricServiceClient()
        project_name = f"projects/{self.project_id}"
        interval = monitoring_v3.TimeInterval()

        now = time.time()
        seconds = int(now)
        nanos = int((now - seconds) * 10 ** 9)
        interval = monitoring_v3.TimeInterval(
            {
                "end_time": {"seconds": seconds, "nanos": nanos},
                "start_time": {"seconds": (seconds - 1200), "nanos": nanos},
            }
        )

        results = client.list_time_series(
            request={
                "name": project_name,
                "filter": 'metric.type = "{}"'.format(self.descriptor_name),
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            }
        )
        for result in results:
            print(result)

    def list_time_series_header(self) -> None:
        client = monitoring_v3.MetricServiceClient()
        project_name = f"projects/{self.project_id}"
        now = time.time()
        seconds = int(now)
        nanos = int((now - seconds) * 10 ** 9)
        interval = monitoring_v3.TimeInterval(
            {
                "end_time": {"seconds": seconds, "nanos": nanos},
                "start_time": {"seconds": (seconds - 1200), "nanos": nanos},
            }
        )
        results = client.list_time_series(
            request={
                "name": project_name,
                "filter": 'metric.type = "{}"'.format(self.descriptor_name),
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.HEADERS,
            }
        )
        for result in results:
            print(result)

    def list_time_series_aggregate(self) -> None:
        client = monitoring_v3.MetricServiceClient()
        project_name = f"projects/{self.project_id}"

        now = time.time()
        seconds = int(now)
        nanos = int((now - seconds) * 10 ** 9)
        interval = monitoring_v3.TimeInterval(
            {
                "end_time": {"seconds": seconds, "nanos": nanos},
                "start_time": {"seconds": (seconds - 3600), "nanos": nanos},
            }
        )
        aggregation = monitoring_v3.Aggregation(
            {
                "alignment_period": {"seconds": 1200},  # 20 minutes
                "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
            }
        )

        results = client.list_time_series(
            request={
                "name": project_name,
                "filter": 'metric.type = "{}"'.format(self.descriptor_name),
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
                "aggregation": aggregation,
            }
        )
        for result in results:
            print(result)

    def list_time_series_reduce(self) -> None:
        client = monitoring_v3.MetricServiceClient()
        project_name = f"projects/{self.project_id}"

        now = time.time()
        seconds = int(now)
        nanos = int((now - seconds) * 10 ** 9)
        interval = monitoring_v3.TimeInterval(
            {
                "end_time": {"seconds": seconds, "nanos": nanos},
                "start_time": {"seconds": (seconds - 3600), "nanos": nanos},
            }
        )
        aggregation = monitoring_v3.Aggregation(
            {
                "alignment_period": {"seconds": 1200},  # 20 minutes
                "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
                "cross_series_reducer": monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
                "group_by_fields": ["resource.zone"],
            }
        )

        results = client.list_time_series(
            request={
                "name": project_name,
                "filter": 'metric.type = "{}"'.format(self.descriptor_name),
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
                "aggregation": aggregation,
            }
        )
        for result in results:
            print(result)

def main():
    import os
    project_id=os.environ["GOOGLE_CLOUD_PROJECT"]

    custom=TimeSeriesViewer(project_id,'custom.googleapis.com/in_gcs_images')
    custom.list_time_series()
    print('=====================================') 
    custom.list_time_series_header()
    print('=====================================') 
    custom.list_time_series_aggregate()

if __name__ == '__main__':
    main()
