from django.db import models


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

    return {user.__str__(): content}


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
    )

    content = {
        "company": company.__str__(),
    }

    values = {
        "tasks_count": [],
        "active": [],
        "completed": [],
        "given": [],
        "review": [],
    }

    users_content = {}

    for coworker in queryset:
        statistics = create_user_statistics(
            coworker,
            include_tasks,
            date_from,
            date_to,
        )
        users_content.update(statistics)
        for key, value in statistics[coworker.__str__()].items():
            if key in values:
                values[key].append(value)

    content["total_tasks"] = {key: sum(value) for key, value in values.items()}

    content["average_tasks_values"] = {
        key: round(sum(value) / len(value), 2) for key, value in values.items()
    }

    if include_users:
        content["users"] = users_content

    return content
