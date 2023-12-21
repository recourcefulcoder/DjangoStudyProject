from django.db import models

from workplace import models as wp_models


def create_user_statistics(
    user,
    include_tasks,
    date_from,
    date_to,
    *args,
    **kwargs,
):
    queryset = user.tasks.filter(
        models.Q(created_at__gte=date_from, deadline__lte=date_to)
        | models.Q(created_at__gte=date_from, completed_at__lte=date_to),
    )

    tasks_status_count = user.tasks.values("status").annotate(
        count=models.Count("status"),
    )

    content = {
        "tasks_count": queryset.count(),
    } | {elem["status"]: elem["count"] for elem in tasks_status_count}

    if include_tasks:
        content["tasks"] = []
        for task in queryset.all():
            task_data = {
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "creation_date": task.created_at.strftime("%d-%m-%Y %H:%M:%S"),
            }
            if task_data["status"] == "completed":
                task_data |= {
                    "completion_date": task.completed_at.strftime(
                        "%d-%m-%Y %H:%M:%S",
                    ),
                    "time_spent": str(
                        task.completed_at - task.created_at,
                    ).split(".")[0],
                }

            content["tasks"].append(task_data)

    return content


def create_company_statistics(
    company,
    include_users,
    date_from,
    date_to,
    include_tasks=False,
    **kwargs,
):
    queryset = company.users.filter(
        role="employee",
    ).prefetch_related(
        models.Prefetch(
            "tasks",
            queryset=wp_models.Task.objects.filter(
                models.Q(created_at__gte=date_from, deadline__lte=date_to)
                | models.Q(
                    status__in=["in_process", "on_checking", "rejected"],
                )
                | models.Q(
                    created_at__gte=date_from,
                    completed_at__lte=date_to,
                ),
            ),
        ),
    )
    print(queryset)

    return {}
