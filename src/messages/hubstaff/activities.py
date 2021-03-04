from datetime import timedelta

from src.schemas.hubstaff import HubStaffActivityReports
from src.utils import convert_number_to_decimal


def prepare_response_activities_list(data: HubStaffActivityReports):
    response = "<b>Журнал часов\n</b>"

    for report in data.reports:
        response += f"<b>{report.organization_name}\n</b>"
        for activity in report.activities:
            activity_percentage = convert_number_to_decimal(activity.activity / activity.tracked * 100)

            response += f"{activity.task.name} - {str(timedelta(seconds=activity.tracked))} <i>({activity_percentage}%)</i>\n"

        total_avg_activity_percentage = convert_number_to_decimal(report.total_activity / report.total_tracked * 100)

        response += f"\n<b>Всего времени: {str(timedelta(seconds=report.total_tracked))}</b>"
        response += f"\n<b>Средняя активность: {total_avg_activity_percentage}%</b>"
        response += "\n"

    return response[:4096]
