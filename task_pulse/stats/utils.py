from django.contrib.auth import get_user_model

from workplace import models


def create_user_statistics_file(user, include_tasks, date_from, date_to):
    queryset = user.tasks.filter()
