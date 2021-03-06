from rest_framework import serializers
import markdown2
from .models import ProgrammingLanguage, Snippet
from omaralbeik import server_variables as sv


class ProgrammingLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammingLanguage
        fields = ("id", "name", "slug", "icon_url",)


class SnippetSerializer(serializers.ModelSerializer):
    html_text = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()
    website_url = serializers.SerializerMethodField()
    meta = serializers.SerializerMethodField()

    class Meta:
        model = Snippet
        fields = (
            "id",
            "name",
            "slug",
            "summary",
            "html_text",
            "website_url",
            "date_published",
            "language",
            "meta",
        )

    # return snippet as HTML
    def get_html_text(self, snippet):
        return markdown2.markdown(snippet.text, extras=["fenced-code-blocks"])

    # return snippet's web URL.
    def get_website_url(self, snippet):
        return "{}/snippets?id={}".format(sv.CLIENT_PROD_URL, snippet.slug)

    # return snippet's language.
    def get_language(self, snippet):
        serializer = ProgrammingLanguageSerializer(snippet.language)
        return serializer.data

    # return snippet's meta fields.
    def get_meta(self, snippet):
        return {
            "title": snippet.name,
            "description": snippet.summary,
            "keywords": [snippet.language.name],
            "canonical": self.get_website_url(snippet),
        }
