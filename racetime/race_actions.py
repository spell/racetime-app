import random
import re
import string
from datetime import timedelta

from django.conf import settings
from django.core.cache import cache
from django.urls import reverse
from django.utils import timezone

from racetime import forms, models
from racetime.utils import SafeException


class Join:
    commands = ['join', 'enter']

    def action(self, race, user, data):
        race.join(user)


class Leave:
    commands = ['leave', 'unenter']

    def action(self, race, user, data):
        entrant = race.in_race(user)
        if entrant:
            entrant.leave()
        else:
            raise SafeException('Possible sync error. Refresh to continue.')


class RequestInvite:
    commands = ['requestinvite']

    def action(self, race, user, data):
        race.request_to_join(user)


class CancelInvite:
    commands = ['cancelinvite']

    def action(self, race, user, data):
        entrant = race.in_race(user)
        if entrant:
            entrant.cancel_request()
        else:
            raise SafeException('Possible sync error. Refresh to continue.')


class AcceptInvite:
    commands = ['acceptinvite']

    def action(self, race, user, data):
        entrant = race.in_race(user)
        if entrant:
            entrant.accept_invite()
        else:
            raise SafeException('Possible sync error. Refresh to continue.')


class DeclineInvite:
    commands = ['declineinvite']

    def action(self, race, user, data):
        entrant = race.in_race(user)
        if entrant:
            entrant.decline_invite()
        else:
            raise SafeException('Possible sync error. Refresh to continue.')


class Ready:
    commands = ['ready']

    def action(self, race, user, data):
        entrant = race.in_race(user)
        if entrant:
            entrant.is_ready()
        else:
            raise SafeException('Possible sync error. Refresh to continue.')


class Unready:
    commands = ['unready']

    def action(self, race, user, data):
        entrant = race.in_race(user)
        if entrant:
            entrant.not_ready()
        else:
            raise SafeException('Possible sync error. Refresh to continue.')


class Done:
    commands = ['done']

    def action(self, race, user, data):
        entrant = race.in_race(user)
        if entrant:
            entrant.done()
        else:
            raise SafeException('Possible sync error. Refresh to continue.')


class Undone:
    commands = ['undone']

    def action(self, race, user, data):
        entrant = race.in_race(user)
        if entrant:
            entrant.undone()
        else:
            raise SafeException('Possible sync error. Refresh to continue.')


class Forfeit:
    commands = ['forfeit']

    def action(self, race, user, data):
        entrant = race.in_race(user)
        if entrant:
            entrant.forfeit()
        else:
            raise SafeException('Possible sync error. Refresh to continue.')


class Unforfeit:
    commands = ['unforfeit']

    def action(self, race, user, data):
        entrant = race.in_race(user)
        if entrant:
            entrant.unforfeit()
        else:
            raise SafeException('Possible sync error. Refresh to continue.')


class LeaveOrForfeit:
    commands = ['quit', 'brexit']

    def action(self, race, user, data):
        entrant = race.in_race(user)
        if entrant:
            if race.is_preparing:
                entrant.leave()
            else:
                entrant.forfeit()
        else:
            raise SafeException('Possible sync error. Refresh to continue.')


class UndoneOrUnforfeit:
    commands = ['undone']

    def action(self, race, user, data):
        entrant = race.in_race(user)
        if entrant and entrant.finish_time:
            entrant.undone()
        elif entrant and entrant.dnf:
            entrant.unforfeit()
        else:
            raise SafeException('Possible sync error. Refresh to continue.')


class AddComment:
    commands = ['comment']

    def action(self, race, user, data):
        form = forms.CommentForm(data)
        if not form.is_valid():
            raise SafeException(form.errors)

        entrant = race.in_race(user)
        comment = form.cleaned_data.get('comment', '').strip()
        if entrant and comment:
            entrant.add_comment(comment)
        else:
            raise SafeException('Possible sync error. Refresh to continue.')


class ShowGoal:
    commands = ['goal', 'info']

    def action(self, race, user, data):
        race.add_message('Goal: ' + race.goal_str)
        if race.info:
            race.add_message(race.info)


class ShowLog:
    commands = ['log']

    def action(self, race, user, data):
        race.add_message(
            'Chat log download: %s'
            % settings.RT_SITE_URI + reverse('race_log', args=(race.category.slug, race.slug))
        )


class ShowCSV:
    commands = ['csv']

    def action(self, race, user, data):
        race.add_message(
            'CSV results file: %s'
            % settings.RT_SITE_URI + reverse('race_csv', args=(race.category.slug, race.slug))
        )


class Help:
    commands = ['help']

    def action(self, race, user, data):
        race.add_message(
            'For help using the site and a list of chat commands, visit: %s'
            % settings.RT_SITE_URI + '/about/help'
        )


class Random:
    commands = ['random']
    shortcuts = {
        'bingo': '######',
        'sm64': '#####',
        'file': '??',
    }
    MAX_LENGTH = 16

    def action(self, race, user, data):
        comment = data.get('comment', '').strip()
        if comment in self.shortcuts:
            pattern = self.shortcuts[comment]
        else:
            pattern = comment

        if pattern and re.match('.*[#*?]', pattern):
            if len(pattern) > self.MAX_LENGTH:
                raise SafeException(
                    'Pattern too long. It should be at most %d characters.'
                    % self.MAX_LENGTH
                )
            else:
                result = re.sub('#', lambda *args: random.choice(string.digits), pattern)
                result = re.sub('\\*', lambda *args: random.choice(string.ascii_letters), result)
                result = re.sub('\\?', lambda *args: random.choice(string.ascii_letters + string.digits), result)
                models.Message.objects.create(
                    user=user,
                    race=race,
                    message='.random %s' % comment,
                )
                race.add_message(
                    'Random string result: ##bot##%(result)s##'
                    % {'result': result}
                )
        else:
            raise SafeException(
                'Usage: .random #*? (use # for a digit, * for a letter, ? for either)'
            )


commands = {
    command: action
    for action in [
        Join,
        Leave,
        RequestInvite,
        CancelInvite,
        AcceptInvite,
        DeclineInvite,
        Ready,
        Unready,
        Done,
        Undone,
        Forfeit,
        Unforfeit,
        LeaveOrForfeit,
        UndoneOrUnforfeit,
        AddComment,
        ShowGoal,
        ShowLog,
        ShowCSV,
        Help,
        Random,
    ] for command in action.commands
}


class Message:
    def action(self, race, user, data):
        if not self.guid_is_new(data.get('guid', '')):
            return

        form = forms.ChatForm(data)
        if not form.is_valid():
            raise SafeException(form.errors)
        message = form.save(commit=False)

        if message.message[0] == '.':
            command, msg = (message.message[1:] + ' ').split(' ', 1)
            command = command.lower()
            if command in commands:
                race_action = commands[command]()

                if isinstance(race_action, AddComment) and not msg.strip():
                    raise SafeException('Your comment cannot be blank.')

                try:
                    return race_action.action(race, user, {'comment': msg})
                except SafeException as ex:
                    if str(ex) == 'Possible sync error. Refresh to continue.':
                        raise SafeException(
                            f'You cannot .{command} at this time (is your stream live yet?).'
                            if command == 'ready' and race.streaming_required else
                            f'You cannot .{command} at this time (try reloading if you get stuck).'
                        )
                    raise

        self.assert_can_chat(race, user)

        message.user = user
        message.race = race
        message.save()

    def assert_can_chat(self, race, user):
        can_moderate = race.category.can_moderate(user)
        can_monitor = race.can_monitor(user)

        if (
            not can_monitor
            and not race.allow_midrace_chat
            and (race.is_pending or race.is_in_progress)
        ):
            raise SafeException(
                'You do not have permission to chat during the race.'
            )
        if (
            not can_monitor
            and not race.allow_non_entrant_chat
            and not race.in_race(user)
            and (race.is_pending or race.is_in_progress)
        ):
            raise SafeException(
                'You do not have permission to chat during the race.'
            )

        if not can_moderate and race.chat_is_closed:
            raise SafeException(
                'This race chat is now closed. No new messages may be added.'
            )

        if (
            not can_moderate
            and models.Message.objects.filter(
                user=user,
                race=race,
                posted_at__gte=timezone.now() - timedelta(seconds=5),
            ).count() > 10
        ):
            raise SafeException(
                'You are chatting too much. Please wait a few seconds.'
            )

    def guid_is_new(self, guid):
        """
        Check if we've seen the GUID posted with this message in the last 5
        minutes. If so, it's almost certainly a duplicate message and we should
        silently ignore it.
        """
        if not re.match(r'^[0-9a-z\-]+$', guid):
            raise SafeException(
                'Bad request, no GUID supplied. A unique string is required '
                'to prevent duplicate messaging.'
            )
        if cache.get('guid/message/' + guid):
            return False
        cache.set('guid/message/' + guid, True, 300)
        return True


