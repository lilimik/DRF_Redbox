from django.db.models import Manager, Count


class PostManager(Manager):
    def annotate_comments_count(self):
        return self.annotate(
            comments_count=Count('comments'),
        )
