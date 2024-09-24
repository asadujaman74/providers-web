from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.search import index
from wagtail.images.models import Image


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    template = 'app/blog_index_page.html'  # Explicitly specify the template

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        # Make sure you're referencing your custom BlogPage here
        context['posts'] = BlogPage.objects.live().order_by('-first_published_at')
        return context


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'  # No reverse relation created here
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
        FieldPanel('main_image'),
    ]

    class Meta:
        # Ensure no clash between BlogPage models by specifying a unique related_name
        default_related_name = 'custom_blogpage'
