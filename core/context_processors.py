from core.notifications.adapters import DjangoMessagesAdapter


def notifications(request):

    return {
        "notifications": DjangoMessagesAdapter.to_dtos(request)
    }