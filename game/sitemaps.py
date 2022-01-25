from django.contrib.sitemaps import Sitemap
from game.models import Post

class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Post.objects.filter(active=True)

    def lastmod(self, obj):
        return obj.updated
