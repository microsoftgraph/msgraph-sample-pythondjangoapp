<!-- markdownlint-disable MD002 MD041 -->

In this exercise you will incorporate the Microsoft Graph into the application. For this application, you will use the [Requests-OAuthlib](https://requests-oauthlib.readthedocs.io/en/latest/) library to make calls to Microsoft Graph.

## Get calendar events from Outlook

1. Start by adding a method to **./tutorial/graph_helper.py** to fetch the calendar events. Add the following method.

    :::code language="python" source="../demo/graph_tutorial/tutorial/graph_helper.py" id="GetCalendarSnippet":::

    Consider what this code is doing.

    - The URL that will be called is `/v1.0/me/events`.
    - The `$select` parameter limits the fields returned for each events to just those the view will actually use.
    - The `$orderby` parameter sorts the results by the date and time they were created, with the most recent item being first.

1. In **./tutorial/views.py**, change the `from tutorial.graph_helper import get_user` line to the following.

    ```python
    from tutorial.graph_helper import get_user, get_calendar_events
    ```

1. Add the following view to **./tutorial/views.py**.

    ```python
    def calendar(request):
      context = initialize_context(request)

      token = get_token(request)

      events = get_calendar_events(token)

      context['errors'] = [
        { 'message': 'Events', 'debug': format(events)}
      ]

      return render(request, 'tutorial/home.html', context)
    ```

1. Open **./tutorial/urls.py** and replace the existing `path` statements for `calendar` with the following.

    ```python
    path('calendar', views.calendar, name='calendar'),
    ```

1. Sign in and click the **Calendar** link in the nav bar. If everything works, you should see a JSON dump of events on the user's calendar.

## Display the results

Now you can add a template to display the results in a more user-friendly manner.

1. Create a new file in the **./tutorial/templates/tutorial** directory named `calendar.html` and add the following code.

    :::code language="html" source="../demo/graph_tutorial/tutorial/templates/tutorial/calendar.html" id="CalendarSnippet":::

    That will loop through a collection of events and add a table row for each one.

1. Add the following `import` statement to the top of the **./tutorials/views.py** file.

    ```python
    import dateutil.parser
    ```

1. Replace the `calendar` view in **./tutorial/views.py** with the following code.

    :::code language="python" source="../demo/graph_tutorial/tutorial/views.py" id="CalendarViewSnippet":::

1. Refresh the page and the app should now render a table of events.

    ![A screenshot of the table of events](./images/add-msgraph-01.png)
