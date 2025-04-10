from service_objects.services import Service
from django.utils import timezone
from ..models import Job
from ..serializers.model_serializers import JobSerializer
from ..constants import constant


class CreateJob(Service):
    def process(self):
        serializer = self.data.get("serializer")
        serializer.save()


class FetchJobList(Service):
    def process(self):
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return serializer.data


class FetchJobInstance(Service):
    def process(self):
        try:
            job = Job.objects.get(pk=self.data.get("job_id"))
        except Job.DoesNotExist:
            return None
        return job


class UpdateJobStatus(Service):
    def process(self):
        request_data = self.data.get("request_data")
        if request_data['status'] == constant['JobDone']:
            request_data['finished_date'] = timezone.now()
        serializer = JobSerializer(self.data.get("job_instance"), data=self.data.get("request_data"), partial=True)
        if serializer.is_valid():
            serializer.save()
            return True
        return False


class RemoveFinishedJobs(Service):
    def process(self):
        jobs_to_remove = Job.objects.filter(status=constant['JobDone'])
        num_jobs_removed = jobs_to_remove.count()
        jobs_to_remove.delete()
        return f"Successfully removed {num_jobs_removed} finished jobs."
