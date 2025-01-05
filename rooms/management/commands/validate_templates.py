from django.core.management.base import BaseCommand
from django.template.loader import get_template
from django.template import TemplateSyntaxError
from django.conf import settings
import os


class Command(BaseCommand):
    """Command to validate all Django templates in the project."""

    help = 'Validates all Django templates in the project'

    def handle(self, *args, **options):
        """Handle the command execution."""
        template_dirs = settings.TEMPLATES[0]['DIRS']
        template_dirs.append(
            os.path.join(settings.BASE_DIR, 'rooms/templates')
        )

        errors_found = False

        for template_dir in template_dirs:
            self.stdout.write(
                f"Checking templates in: {template_dir}"
            )
            for root, dirs, files in os.walk(template_dir):
                for file in files:
                    if file.endswith('.html'):
                        template_path = os.path.join(root, file)
                        try:
                            template_name = os.path.relpath(
                                template_path,
                                template_dir
                            )
                            get_template(template_name)
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"✓ {template_name}"
                                )
                            )
                        except TemplateSyntaxError as e:
                            errors_found = True
                            self.stdout.write(
                                self.style.ERROR(
                                    f"✗ {template_name}: {str(e)}"
                                )
                            )

        if errors_found:
            self.stdout.write(
                self.style.ERROR('Template validation failed!')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('All templates are valid!')
            )
