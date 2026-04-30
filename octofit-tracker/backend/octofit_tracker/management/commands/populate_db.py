from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, LeaderboardEntry
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete existing data
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        LeaderboardEntry.objects.all().delete()
        Team.objects.all().delete()
        User.objects.all().delete()

        # Create users (super heroes)
        marvel_heroes = [
            {'username': 'ironman', 'email': 'ironman@marvel.com'},
            {'username': 'captainamerica', 'email': 'cap@marvel.com'},
            {'username': 'spiderman', 'email': 'spiderman@marvel.com'},
        ]
        dc_heroes = [
            {'username': 'batman', 'email': 'batman@dc.com'},
            {'username': 'superman', 'email': 'superman@dc.com'},
            {'username': 'wonderwoman', 'email': 'wonderwoman@dc.com'},
        ]
        marvel_users = [User.objects.create_user(**hero, password='password') for hero in marvel_heroes]
        dc_users = [User.objects.create_user(**hero, password='password') for hero in dc_heroes]

        # Create teams
        marvel_team = Team.objects.create(name='Team Marvel')
        marvel_team.members.set(marvel_users)
        dc_team = Team.objects.create(name='Team DC')
        dc_team.members.set(dc_users)

        # Create activities
        for user in marvel_users + dc_users:
            Activity.objects.create(
                user=user,
                activity_type='run',
                duration=30,
                calories_burned=300,
                date=timezone.now().date()
            )

        # Create workouts
        workout1 = Workout.objects.create(name='Pushups', description='Do 20 pushups')
        workout2 = Workout.objects.create(name='Situps', description='Do 30 situps')
        workout1.suggested_for.set(marvel_users)
        workout2.suggested_for.set(dc_users)

        # Create leaderboard entries
        for i, user in enumerate(marvel_users + dc_users, 1):
            LeaderboardEntry.objects.create(user=user, score=100 * i, rank=i)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data'))
