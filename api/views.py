from django.shortcuts import get_object_or_404
from rest_framework.throttling import AnonRateThrottle
from rest_framework.viewsets import ModelViewSet

from api.throttling import LunchBreakThrottle
from posts.models import Post
from api.serializers import PostSerializer
from api.permissions import AuthorOrReadOnly

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics, filters


def valid_serializer(serializer):
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def api_posts(request):
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data, many=True)
        return valid_serializer(serializer)

    post_list = Post.objects.all()
    serialize = PostSerializer(data=post_list, many=True)
    return Response(serialize.data)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_posts_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'PUT' or request.method == 'PATCH':
        serializer = PostSerializer(post, data=request.data, partial=True)
        return valid_serializer(serializer)

    if request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = PostSerializer(post)
    return Response(serializer.data)


class APIPostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class APIPostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    permission_classes = (AuthorOrReadOnly,)
    throttle_classes = (LunchBreakThrottle, AnonRateThrottle,)  # Подключили класс AnonRateThrottle
    filter_backends = (filters.SearchFilter, )
    search_fields = ('$text', )
