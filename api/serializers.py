from rest_framework import serializers
from posts.models import Post, Group, Comment, Tag, TagPost


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class PostSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(
        queryset=Group.objects.all(),
        slug_field='slug',
        required=False,
    )
    tag = TagSerializer(
        required=False,
        many=True,
    )

    character_quantity = serializers.SerializerMethodField()
    publication_date = serializers.CharField(source='created', read_only=True)

    class Meta:
        model = Post
        fields = ('text', 'author', 'publication_date', 'group', 'tag', 'character_quantity')
        read_only_fields = ('author',)

    def get_character_quantity(self, obj):
        return len(obj.text)

    def create(self, validated_data):

        if 'tag' not in self.initial_data:
            post = Post.objects.create(**validated_data)
            return post

        tags = validated_data.pop('tag')

        post = Post.objects.create(**validated_data)

        for tag in tags:
            current_tag, status = Tag.objects.get_or_create(
                **tag
            )
            TagPost.objects.create(tag=current_tag, post=post)

        return post

    def update(self, instance, validated_data):
        tags = validated_data.pop('tag')

        instance.text = validated_data.get('text', instance.text)
        instance.author = validated_data.get('author', instance.author)
        instance.created = validated_data.get('created', instance.created)
        instance.group = validated_data.get('group', instance.group)
        instance.save()

        for tag in tags:
            current_tag, status = Tag.objects.get_or_create(
                **tag
            )
            TagPost.objects.create(tag=current_tag, post=instance)

        return instance


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'text', 'created')
