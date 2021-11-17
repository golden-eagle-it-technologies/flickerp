import bleach
import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse

from task.models import Task, TaskList

"""
First the "smoketests" - do they respond at all for a logged in admin user?
Next permissions tests - some views should respond for staffers only.
After that, view contents and behaviors.
"""


@pytest.mark.django_db
def test_task_setup(task_setup):
    assert Task.objects.all().count() == 6


def test_view_list_lists(task_setup, admin_client):
    url = reverse("task:lists")
    response = admin_client.get(url)
    assert response.status_code == 200


def test_view_reorder(task_setup, admin_client):
    url = reverse("task:reorder_tasks")
    response = admin_client.get(url)
    assert response.status_code == 201  # Special case return value expected


def test_view_external_add(task_setup, admin_client, settings):
    default_list = TaskList.objects.first()
    settings.task_DEFAULT_LIST_SLUG = default_list.slug
    assert settings.task_DEFAULT_LIST_SLUG == default_list.slug
    url = reverse("task:external_add")
    response = admin_client.get(url)
    assert response.status_code == 200


def test_view_mine(task_setup, admin_client):
    url = reverse("task:mine")
    response = admin_client.get(url)
    assert response.status_code == 200


def test_view_list_completed(task_setup, admin_client):
    tlist = TaskList.objects.get(slug="zip")
    url = reverse(
        "task:list_detail_completed", kwargs={"list_id": tlist.id, "list_slug": tlist.slug}
    )
    response = admin_client.get(url)
    assert response.status_code == 200


def test_view_list(task_setup, admin_client):
    tlist = TaskList.objects.get(slug="zip")
    url = reverse("task:list_detail", kwargs={"list_id": tlist.id, "list_slug": tlist.slug})
    response = admin_client.get(url)
    assert response.status_code == 200


def test_view_add_list(task_setup, admin_client):
    url = reverse("task:add_list")
    response = admin_client.get(url)
    assert response.status_code == 200


def test_view_task_detail(task_setup, admin_client):
    task = Task.objects.first()
    url = reverse("task:task_detail", kwargs={"task_id": task.id})
    response = admin_client.get(url)
    assert response.status_code == 200


def test_del_task(task_setup, admin_user, client):
    task = Task.objects.first()
    url = reverse("task:delete_task", kwargs={"task_id": task.id})
    # View accepts POST, not GET
    client.login(username="admin", password="password")
    response = client.get(url)
    assert response.status_code == 403
    response = client.post(url)
    assert not Task.objects.filter(id=task.id).exists()


def test_task_toggle_done(task_setup, admin_user, client):
    task = Task.objects.first()
    assert not task.completed
    url = reverse("task:task_toggle_done", kwargs={"task_id": task.id})
    # View accepts POST, not GET
    client.login(username="admin", password="password")
    response = client.get(url)
    assert response.status_code == 403

    client.post(url)
    task.refresh_from_db()
    assert task.completed


def test_view_search(task_setup, admin_client):
    url = reverse("task:search")
    response = admin_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_no_javascript_in_task_note(task_setup, client):
    task_list = TaskList.objects.first()
    user = get_user_model().objects.get(username="u2")
    title = "Some Unique String"
    note = "foo <script>alert('oh noez');</script> bar"
    data = {
        "task_list": task_list.id,
        "created_by": user.id,
        "priority": 10,
        "title": title,
        "note": note,
        "add_edit_task": "Submit",
    }

    client.login(username="u2", password="password")
    url = reverse("task:list_detail", kwargs={"list_id": task_list.id, "list_slug": task_list.slug})

    response = client.post(url, data)
    assert response.status_code == 302

    # Retrieve new task and compare notes field
    task = Task.objects.get(title=title)
    assert task.note != note  # Should have been modified by bleach since note included javascript!
    assert task.note == bleach.clean(note, strip=True)


@pytest.mark.django_db
def test_created_by_unchanged(task_setup, client):

    task_list = TaskList.objects.first()
    u2 = get_user_model().objects.get(username="u2")
    title = "Some Unique String with unique chars: ab78539e"
    note = "a note"
    data = {
        "task_list": task_list.id,
        "created_by": u2.id,
        "priority": 10,
        "title": title,
        "note": note,
        "add_edit_task": "Submit",
    }

    client.login(username="u2", password="password")
    url_add_task = reverse(
        "task:list_detail", kwargs={"list_id": task_list.id, "list_slug": task_list.slug}
    )

    response = client.post(url_add_task, data)
    assert response.status_code == 302

    # Retrieve new task and compare created_by
    task = Task.objects.get(title=title)
    assert task.created_by == u2

    # Now that we've created the task, edit it as another user.
    # After saving, created_by should remain unchanged.
    extra_g2_user = get_user_model().objects.get(username="extra_g2_user")

    client.login(username="extra_g2_user", password="password")

    url_edit_task = reverse("task:task_detail", kwargs={"task_id": task.id})

    dataTwo = {
        "task_list": task.task_list.id,
        "created_by": extra_g2_user.id,  # this submission is attempting to change created_by
        "priority": 10,
        "title": task.title,
        "note": "the note was changed",
        "add_edit_task": "Submit",
    }

    response = client.post(url_edit_task, dataTwo)
    assert response.status_code == 302

    task.refresh_from_db()

    # Proof that the task was saved:
    assert task.note == "the note was changed"

    # client was unable to modify created_by:
    assert task.created_by == u2


@pytest.mark.django_db
@pytest.mark.parametrize("test_input, expected", [(True, True), (False, False)])
def test_completed_unchanged(test_input, expected, task_setup, client):
    """Tasks are marked completed/uncompleted by buttons,
    not via checkbox on the task edit form. Editing a task should
    not change its completed status. Test with both completed and incomplete Tasks."""

    task = Task.objects.get(title="Task 1", created_by__username="u1")
    task.completed = test_input
    task.save()
    assert task.completed == expected

    url_edit_task = reverse("task:task_detail", kwargs={"task_id": task.id})

    data = {
        "task_list": task.task_list.id,
        "title": "Something",
        "note": "the note was changed",
        "add_edit_task": "Submit",
        "completed": task.completed,
    }

    client.login(username="u1", password="password")
    response = client.post(url_edit_task, data)
    assert response.status_code == 302

    # Prove the task is still marked complete/incomplete
    # (despite the default default state for completed being False)
    task.refresh_from_db()
    assert task.completed == expected


@pytest.mark.django_db
def test_no_javascript_in_comments(task_setup, client):
    user = get_user_model().objects.get(username="u2")
    client.login(username="u2", password="password")

    task = Task.objects.first()
    task.created_by = user
    task.save()

    user.groups.add(task.task_list.group)

    comment = "foo <script>alert('oh noez');</script> bar"
    data = {"comment-body": comment, "add_comment": "Submit"}
    url = reverse("task:task_detail", kwargs={"task_id": task.id})

    response = client.post(url, data)
    assert response.status_code == 200

    task.refresh_from_db()
    newcomment = task.comment_set.last()
    assert newcomment != comment  # Should have been modified by bleach
    assert newcomment.body == bleach.clean(comment, strip=True)


# ### PERMISSIONS ###


def test_view_add_list_nonadmin(task_setup, client):
    url = reverse("task:add_list")
    client.login(username="you", password="password")
    response = client.get(url)
    assert response.status_code == 302  # Redirected to login


def test_view_del_list_nonadmin(task_setup, client):
    tlist = TaskList.objects.get(slug="zip")
    url = reverse("task:del_list", kwargs={"list_id": tlist.id, "list_slug": tlist.slug})
    client.login(username="you", password="password")
    response = client.get(url)
    assert response.status_code == 302  # Fedirected to login


def test_del_list_not_in_list_group(task_setup, admin_client):
    tlist = TaskList.objects.get(slug="zip")
    url = reverse("task:del_list", kwargs={"list_id": tlist.id, "list_slug": tlist.slug})
    response = admin_client.get(url)
    assert response.status_code == 403


def test_view_list_mine(task_setup, client):
    """View a list in a group I belong to.
    """
    tlist = TaskList.objects.get(slug="zip")  # User u1 is in this group's list
    url = reverse("task:list_detail", kwargs={"list_id": tlist.id, "list_slug": tlist.slug})
    client.login(username="u1", password="password")
    response = client.get(url)
    assert response.status_code == 200


def test_view_list_not_mine(task_setup, client):
    """View a list in a group I don't belong to.
    """
    tlist = TaskList.objects.get(slug="zip")  # User u1 is in this group, user u2 is not.
    url = reverse("task:list_detail", kwargs={"list_id": tlist.id, "list_slug": tlist.slug})
    client.login(username="u2", password="password")
    response = client.get(url)
    assert response.status_code == 403


def test_view_task_mine(task_setup, client):
    # Users can always view their own tasks
    task = Task.objects.filter(created_by__username="u1").first()
    client.login(username="u1", password="password")
    url = reverse("task:task_detail", kwargs={"task_id": task.id})
    response = client.get(url)
    assert response.status_code == 200


def test_view_task_my_group(task_setup, client, django_user_model):
    """User can always view tasks that are NOT theirs IF the task is in a shared group.
    u1 and u2 are in different groups in the fixture -
    Put them in the same group."""
    g1 = Group.objects.get(name="Workgroup One")
    u2 = django_user_model.objects.get(username="u2")
    u2.groups.add(g1)

    # Now u2 should be able to view one of u1's tasks.
    task = Task.objects.filter(created_by__username="u1").first()
    url = reverse("task:task_detail", kwargs={"task_id": task.id})
    client.login(username="u2", password="password")
    response = client.get(url)
    assert response.status_code == 200


def test_view_task_not_in_my_group(task_setup, client):
    # User canNOT view a task that isn't theirs if the two users are not in a shared group.
    # For this we can use the fixture data as-is.
    task = Task.objects.filter(created_by__username="u1").first()
    url = reverse("task:task_detail", kwargs={"task_id": task.id})
    client.login(username="u2", password="password")
    response = client.get(url)
    assert response.status_code == 403


def test_setting_task_STAFF_ONLY_False(task_setup, client, settings):
    # We use Django's user_passes_test to call `staff_check` utility function on all views.
    # Just testing one view here; if it works, it works for all of them.
    settings.task_STAFF_ONLY = False
    url = reverse("task:lists")
    client.login(username="u2", password="password")
    response = client.get(url)
    assert response.status_code == 200


def test_setting_task_STAFF_ONLY_True(task_setup, client, settings, django_user_model):
    # We use Django's user_passes_test to call `staff_check` utility function on some views.
    # Just testing one view here...
    settings.task_STAFF_ONLY = True
    url = reverse("task:lists")

    # Remove staff privileges from user u2; they should not be able to access
    u2 = django_user_model.objects.get(username="u2")
    u2.is_staff = False
    u2.save()

    client.login(username="u2", password="password")
    response = client.get(url)
    assert response.status_code == 302  # Redirected to login view