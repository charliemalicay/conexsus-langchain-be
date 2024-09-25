import requests

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from langchain.memory.chat_message_histories.in_memory import ChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .classes.langchain_hf_handler.langchain_hf_handler import LangchainHFHandler
from .models import ChatMessage, Conversation
from .serializers import ChatMessageSerializer, ConversationSerializer

llm = LangchainHFHandler()
memory = ConversationBufferMemory()

# Function Initialize Pipeline and Invoke Chat
@api_view(['POST', 'GET'])
def chat(request):
    # region Initialize Pipeline
    if request.method == 'GET':
        # memory.clear()
        # retrieved_chat_history = ChatMessageHistory(messages=[])

        llm.init_pipeline()

        # reloaded_chain = ConversationChain(
        #     llm=llm,
        #     memory=ConversationBufferMemory(
        #         chat_memory=retrieved_chat_history),
        #     verbose=True
        # )

        return JsonResponse({ "data": {"message": "Initialize Complete"} }, status=200)
    # endregion

    # region Post Invoke Prompt
    elif request.method == 'POST':
        try:
            request_data = JSONParser().parse(request)
            prompt = request_data.get('prompt')

            llm.invoke_prompt()

            return JsonResponse({ "data": {'id': 'bot' , 'message': llm.chain_output}}, status=200)

        except Exception as err:
            return Response(f"Got Error {str(err)}", status=status.HTTP_400_BAD_REQUEST)
    # endregion
