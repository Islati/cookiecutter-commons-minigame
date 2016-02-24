import os
from craftbuildtools.template import TemplateRenderPlugin

# This plugin script is utilized by CraftBuildTools
# To generate project structures, from templates
# For the user

# It's part of a complete suite of Minecraft Development / Admin Tools
# And is totally free for use, extension, and so forth!

# Note: Don't worry about the dependencies right now. When it's ran through CraftBuildTools
# There's no issue with these dependencies being resolved.

class CookieCutterCommonsMinigame(TemplateRenderPlugin):
    def __init__(self):
        super(CookieCutterCommonsMinigame, self).__init__(
            name="cookiecutter_commons_minigame_template",
            template_name="Commons_Minigame", version="1",
            description="Template Render plugin used to generate a Commons-utilizing Minecraft Minigame Plugin."
        )

    def perform(self, **kwargs):
        from craftbuildtools import app, logger
        from craftbuildtools.utils import ChangeDir
        from cookiecutter.main import cookiecutter
        import click

        directory = kwargs.pop("directory")

        project_author = click.prompt("Project Author", default="Your Username")
        project_name = click.prompt("Project Name", default="My Spigot Project")
        project_version = click.prompt("Project Version", default="1.0.0")
        project_description = click.prompt("Project Description", default="A cookie-cutter spigot project")
        main_package = click.prompt("Main Package",
                                    default="com.yourdomain.%s" % project_name.lower().replace(' ', '_').replace('-',
                                                                                                                 '_'))

        main_class = click.prompt(
            "Main Class", default=project_name.replace(' ', '').replace("-", ""))

        user_class = click.prompt("User Class", default="%sUser" % main_class)
        user_manager_class = click.prompt("User Manager Class", default="%sManager" % user_class)

        repo_name = click.prompt("Repository Name", default=project_name.lower().replace(" ", ""))
        artifact_id = click.prompt("Artifact Name", default=project_name.lower().replace(" ", ""))
        plugin_dependencies = click.prompt("Plugin Dependencies (Comma Separated)", default="Commons")
        spigot_version = click.prompt("Spigot Version", default="1.8.8-R0.1-SNAPSHOT")
        output_dir = click.prompt("Lastly, where do you wish to store the project?",
                                  default=os.path.expanduser("~/Projects"))

        cookiecutter(
            os.path.join(directory),
            output_dir=output_dir,
            no_input=True,
            extra_context={
                "project_author": project_author,
                "project_name": project_name,
                "project_version": project_version,
                "project_description": project_description,
                "main_package": main_package,
                "main_class": main_class,
                "user_class": user_class,
                "user_manager_class": user_manager_class,
                "repo_name": repo_name,
                "artifact_id": artifact_id,
                "plugin_dependencies": plugin_dependencies,
                "spigot_version": spigot_version
            })

        project_main_path = os.path.join(output_dir, repo_name, "src", "main", "java")

        project_new_path = os.path.join(output_dir, repo_name)

        project_main_package_path = project_main_path

        if not os.path.exists(project_main_package_path):
            logger.error("Project has failed to create. Halting Execution.")
            exit(9)
            return

        project_package_path = main_package.split(".")
        for path in project_package_path:
            project_main_package_path = os.path.join(project_main_package_path, path)

            if not os.path.exists(project_main_package_path):
                os.mkdir(project_main_package_path)

        if not os.path.exists(project_main_package_path):
            os.makedirs(project_main_package_path)

        main_class_path = os.path.join(project_main_path, "%s.java" % main_class)

        if not os.path.exists(main_class_path):
            logger.error("Unable to locate path %s" % main_class_path)
            return  # todo clean up dir... Shit failed bruh.

        import shutil

        shutil.move(main_class_path, os.path.join(project_main_package_path, "%s.java" % main_class))
        directory_list = os.listdir(project_main_path)

        for dirname in directory_list:
            logger.info("Directory %s in MiniGame Template Render" % dirname)
            shutil.move(os.path.join(project_main_path, dirname), project_main_package_path)
            logger.info("Was Moved to %s to retain structure" % project_main_package_path)

        logger.info("Finished Generating project [%s] @ %s" % (project_name, project_new_path))

        # Get the project configuration directory.
        projects_config_dir = app.projects_folder

        # Create the project from prompt.
        from craftbuildtools.data import Project

        project = Project(
            name=project_name,
            directory=project_new_path,
            target_directory=os.path.join(project_new_path, "target"),
            build_command="mvn clean install"
        )

        import yaml

        # Save the project to file!
        with open(os.path.join(projects_config_dir, '%s.yml' % project.name), 'w') as project_new_config_file:
            yaml.dump(project.yaml(), project_new_config_file, default_flow_style=False)

        logger.info("Created %s.yml file in projects folder to allow management with CraftBuildTools!" % project_name)


cookiecutter_commons_minigame = CookieCutterCommonsMinigame()
