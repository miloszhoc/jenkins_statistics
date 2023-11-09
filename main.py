from charts import FailuresPerDayChart, FailuresPerJobChart
from results_joiner import TestResultsJoiner
from tables import TestCaseAmountChangeForEachDayTable, TestCaseChangeForEachDayTable
from variables import JOINED_TEST_DATA_FILE_NAME, DASHBOARD_TEMPLATE, DASHBOARD_OUTPUT_FILE


class BuildDashboard():

    def __init__(self, dashboard_file, env, dashboard_elements) -> None:
        super().__init__()
        self.html_template = DASHBOARD_TEMPLATE
        self.env = env
        self.dashboard_output_file = dashboard_file
        self.dashboard_elements = dashboard_elements

    def create_dashboard(self):
        with open(self.html_template, 'r') as template:
            with open(self.dashboard_output_file, 'w+') as dashboard:
                template_content = template.read()
                new_content = ''
                for element_name, element in self.dashboard_elements.items():
                    new_content += f'<h3>{element_name}:</h3>'
                    new_content += element

                template_content = template_content.replace('[CONTENT]', new_content)
                template_content = template_content.replace('[ENV]', self.env)
                dashboard.write(template_content)


if __name__ == '__main__':
    joiner = TestResultsJoiner()
    joiner.join_results()
    f_per_day = FailuresPerDayChart(JOINED_TEST_DATA_FILE_NAME)
    per_day = f_per_day.draw_chart()

    t = FailuresPerJobChart(JOINED_TEST_DATA_FILE_NAME)
    per_job = t.draw_chart()

    y = TestCaseAmountChangeForEachDayTable(JOINED_TEST_DATA_FILE_NAME)
    table_amount = y.build_html_table()

    z = TestCaseChangeForEachDayTable(JOINED_TEST_DATA_FILE_NAME)
    table = z.build_html_table()

    dashboard_elements = {
        'Test case amount change for each day': table_amount,
        'Test case change for each day': table,
        'Test case failures per job': f'<img src={per_job} />',
        'Test case failures per day': f'<img src={per_day} />'
    }

    BuildDashboard(DASHBOARD_OUTPUT_FILE, 'QA', dashboard_elements).create_dashboard()
