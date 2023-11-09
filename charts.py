from matplotlib import pyplot as plt

from utils import read_json_file
from variables import NUMBER_OF_DAYS, JOINED_TEST_DATA_FILE_NAME


class FailuresPerDayChart:

    def __init__(self, all_data_json_file) -> None:
        self.all_data: dict = read_json_file(all_data_json_file)
        self.all_data = dict(sorted(self.all_data.items()))

    def _prepare_data(self):
        sum_of_failures_by_day = {}

        for date, entries in self.all_data.items():
            total_failures = 0
            for entry in entries:
                total_failures += int(entry["number_of_failed_cases"])
            sum_of_failures_by_day[date] = total_failures

        return sum_of_failures_by_day

    def draw_chart(self):
        chart_file_name = 'failures_per_day.png'
        sum_of_failures_by_day = self._prepare_data()

        days = list(sum_of_failures_by_day.keys())
        failures = list(sum_of_failures_by_day.values())

        plt.bar(days, failures, color='maroon', width=0.4)
        plt.xlabel("Total number of failures for each day")
        plt.ylabel(f"No. of failures")
        plt.title(f"Number of failures in last {NUMBER_OF_DAYS} days")
        plt.savefig(chart_file_name)
        plt.close()
        return chart_file_name


class FailuresPerJobChart():
    def __init__(self, all_data_json_file) -> None:
        self.all_data_json_file = all_data_json_file
        self.all_data = read_json_file(all_data_json_file)
        self.total_failed_cases = dict()
        self.date_range = ''

    def _prepare_data(self) -> dict:
        failed_cases = dict()
        for day, day_data in self.all_data.items():
            for failed_job in day_data:
                failed_cases[failed_job['job_name']] = 0

        for day, day_data in read_json_file(JOINED_TEST_DATA_FILE_NAME).items():
            for failed_job in day_data:
                failed_cases[failed_job['job_name']] += int(failed_job['number_of_failed_cases'])
        self.total_failed_cases = failed_cases

        return failed_cases

    def _get_date_range(self):
        pass

    def draw_chart(self):
        chart_file_name = 'failures_per_job.png'
        self._prepare_data()

        jobs = list(self.total_failed_cases.keys())
        failures = list(self.total_failed_cases.values())

        plt.bar(jobs, failures, color='maroon', width=0.4)
        plt.xlabel("Total number of failures for each job")
        plt.ylabel(f"No. of failures")
        plt.title(f"Total no. of failures in last {NUMBER_OF_DAYS} days")
        plt.savefig(chart_file_name)
        plt.close()
        return chart_file_name
