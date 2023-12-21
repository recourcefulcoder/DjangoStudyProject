import workplace.models

TASK_STATE_ORDER = [elem[0] for elem in workplace.models.TASK_STATES]


def sort_menu_choices(choices):
    # this function changes list of possible task states in
    # "tasks" page of the workplace, so that it has particular
    # order - as in TASK_STATES variable in workplace.models
    new_list = []

    for elem in TASK_STATE_ORDER:
        if elem in choices:
            new_list.append(elem)

    return new_list
