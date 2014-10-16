""" Helpers for snappybouncer tests. """

from django.db.models.signals import post_save

from snappybouncer.models import Ticket, fire_snappy_if_new


class PostSaveHelper(object):
    """ Helper for managing post save hooks during tests. """

    def replace(self):
        """ Unhook post save hooks. """
        has_listeners = lambda: post_save.has_listeners(Ticket)
        assert has_listeners(), (
            "Ticket model has no post_save listeners. Make sure"
            " helpers cleaned up properly in earlier tests.")
        post_save.disconnect(fire_snappy_if_new, sender=Ticket)
        assert not has_listeners(), (
            "Ticket model still has post_save listeners. Make sure"
            " helpers cleaned up properly in earlier tests.")

    def restore(self):
        """ Restore post save hooks. """
        has_listeners = lambda: post_save.has_listeners(Ticket)
        assert not has_listeners(), (
            "Ticket model still has post_save listeners. Make sure"
            " helpers removed them properly in earlier tests.")
        post_save.connect(fire_snappy_if_new, sender=Ticket)
