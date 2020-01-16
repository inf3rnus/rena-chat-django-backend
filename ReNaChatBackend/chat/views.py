from django.shortcuts import render
from django.http import HttpResponse

from .models import Message, Conversation
from .serializers import MessageSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
# Create your views here.
@api_view(['get'])
@permission_classes([IsAuthenticated])
def get_conversation_messages(request):
    paginator = LimitOffsetPagination()
    conversation_id = request.GET.get('conversation_id', None)
    limit = request.GET.get('limit', None)
    offset = request.GET.get('offset', None)
    print('[get_conversation_messages] - conversation_id is: ', conversation_id)
    print('[get_conversation_messages] - limit is: ', limit)
    print('[get_conversation_messages] - offset is: ', offset)
    try:
        # Verify user is in conversation requested.
        conversation = Conversation.objects.get(pk=conversation_id)
        conversation.users.get(pk=request.user.id)
    except:
        print('[get_conversation_messages] - User requesting messages is not in the conversation')
        return HttpResponse(status=401)
    # Filter based off of given conversation
    query_set = Message.objects.filter(conversation_id=conversation_id)
    context = paginator.paginate_queryset(query_set, request)
    print('[get_conversation_messages] - Context is: ', context)
    serializer = MessageSerializer(context, many=True)
    return paginator.get_paginated_response(serializer.data)