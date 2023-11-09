from utils import read_json_file


class TestCaseAmountChangeForEachDayTable:

    def __init__(self, all_data_json_file) -> None:
        self.all_data_json_file = all_data_json_file
        self.all_data = read_json_file(all_data_json_file)
        self.transformed_data = None

    def _prepare_data(self):
        transformed_data = {}

        for day, day_data in self.all_data.items():
            for failed_job in day_data:
                transformed_data[failed_job['job_name']] = {}

        for day, day_data in self.all_data.items():
            for failed_job in day_data:
                transformed_data[failed_job['job_name']].update({day: int(failed_job['number_of_failed_cases'])})

        self.transformed_data = transformed_data

    def build_html_table(self):
        self._prepare_data()

        # table headers
        html_table = "<table>\n<thead>\n<tr>\n<th>Job Name</th>"
        dates = sorted(set([date for job_data in self.transformed_data.values() for date in job_data.keys()]))
        for date in dates:
            html_table += f"<th>{date}</th>"
        html_table += "</tr>\n</thead>\n<tbody>\n"

        # table content
        for job_name, job_data in self.transformed_data.items():
            html_table += "<tr>\n"
            html_table += f"<td>{job_name}</td>"
            for date in dates:
                if date in job_data:
                    html_table += f"<td>{job_data[date]}</td>"
                else:
                    html_table += "<td>-</td>"
            html_table += "</tr>\n"

        html_table += "</tbody>\n</table>"
        return html_table


class TestCaseChangeForEachDayTable:

    def __init__(self, all_data_json_file) -> None:
        self.all_data_json_file = all_data_json_file
        self.all_data = read_json_file(all_data_json_file)
        self.transformed_data = None

    def _prepare_data(self):
        transformed_data = {}

        for day, day_data in self.all_data.items():
            for failed_job in day_data:
                transformed_data[failed_job['job_name']] = {}

        for day, day_data in self.all_data.items():
            for failed_job in day_data:
                transformed_data[failed_job['job_name']].update({day: sorted(failed_job['failed_cases'])})

        self.transformed_data = transformed_data

    def build_html_table(self):
        self._prepare_data()

        # table headers
        html_table = "<table>\n<thead>\n<tr>\n<th>Job Name</th>"
        dates = sorted(set([date for job_data in self.transformed_data.values() for date in job_data.keys()]))
        for date in dates:
            html_table += f"<th>{date}</th>"
        html_table += "</tr>\n</thead>\n<tbody>\n"

        # table content
        for job_name, job_data in self.transformed_data.items():
            html_table += "<tr>\n"
            html_table += f"<td>{job_name}</td>"
            for date in dates:
                if date in job_data:
                    html_table += f"<td>{', <br>'.join(job_data[date])}</td>"
                else:
                    html_table += "<td>-</td>"
            html_table += "</tr>\n"

        html_table += "</tbody>\n</table>"
        return html_table
