from datetime import timedelta

from src.core.config import settings
from src.submodules.hubstaff.schemas import HubStaffActivityReports
from src.utils import convert_number_to_decimal


def prepare_response_activities_list(data: HubStaffActivityReports):
    response = "Журнал часов\n"

    for report in data.reports:
        response += f"<s>{report.organization_name}\n</s>"
        for activity in report.activities:
            activity_percentage = convert_number_to_decimal(activity.activity / activity.tracked * 100)

            add_string = f"{activity.task.name} - {str(timedelta(seconds=activity.tracked))} <i>({activity_percentage}%)</i>\n"

            if len(response) + len(add_string) > 3896:
                response += f"...\n"
                break
            else:
                response += add_string

        total_avg_activity_percentage = convert_number_to_decimal(report.total_activity / report.total_tracked * 100)

        response += f"\n<b>Всего времени: {str(timedelta(seconds=report.total_tracked))}</b>"
        response += f"\n<b>Средняя активность: {total_avg_activity_percentage}%</b>"
        response += "\n"

    return response[:4096]


def prepare_response_today_time_tracked(data: HubStaffActivityReports):
    normal_time_tracked = convert_number_to_decimal(settings.DAILY_TIME_TRACKED_NORMAL_TO_SECONDS)

    response = f"Заполненные журналы работ за сегодня\n"

    for report in data.reports:
        response += f"<s>{report.organization_name}\n</s>"

        response += f"<u>Норма: {str(timedelta(seconds=settings.DAILY_TIME_TRACKED_NORMAL_TO_SECONDS))}\n</u>"
        response += f"<b>Отмечено времени: {str(timedelta(seconds=report.total_tracked))}\n</b>"

        response += f"\n"

        if convert_number_to_decimal(report.total_tracked) >= normal_time_tracked:
            response += f"Хороший человек!\n"
        else:
            response += f"Вспомните, всё ли вы отметили?\n"

    return response[:4096]


def prepare_response_today_activity(data: HubStaffActivityReports):
    normal_avg_activity = convert_number_to_decimal(settings.DAILY_AVG_ACTIVITY_NORMAL_TO_PERCENTAGE)

    response = f"Ваша активность за сегодня\n"

    for report in data.reports:
        response += f"<s>{report.organization_name}\n</s>"

        total_avg_activity_percentage = convert_number_to_decimal(report.total_activity / report.total_tracked * 100)

        response += f"<u>Норма: {normal_avg_activity}%\n</u>"
        response += f"<b>Отмечено активности: {total_avg_activity_percentage}%\n</b>"

        response += f"\n"

        if total_avg_activity_percentage >= normal_avg_activity:
            response += f"Хороший человек!\n"
        else:
            response += f"Повысте уровень активности в HubStaff\n"

    return response[:4096]
