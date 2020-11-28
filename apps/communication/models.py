from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Email(models.Model):
    """
    This is a record of an email sent to a customer.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='emails',
        verbose_name="User",
        null=True
        )

    email_address = models.EmailField(null=True, blank=True)
    subject = models.TextField(max_length=255)
    body_text = models.TextField()
    body_html = models.TextField(blank=True)
    date_sent = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'communication'
        ordering = ['-date_sent']
        verbose_name = 'Email'
        verbose_name_plural = 'Emails'

    def __str__(self):
        if self.user:
            return _("Email to %(user)s with subject '%(subject)s'") % {
                'user': self.user.get_username(), 'subject': self.subject}
        else:
            return _("Email to %(email)s with subject '%(subject)s'") % {
                'email': self.email, 'subject': self.subject}