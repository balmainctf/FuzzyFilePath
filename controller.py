import sublime
import FuzzyFilePath.completion as Completion
from FuzzyFilePath.project.Project import Project
from FuzzyFilePath.project.CurrentFile import CurrentFile
from FuzzyFilePath.project.ProjectManager import ProjectManager
import FuzzyFilePath.common.settings as Settings
from FuzzyFilePath.common.verbose import verbose
from FuzzyFilePath.common.config import config

from FuzzyFilePath.FuzzyFilePath import FuzzyFilePath


ID = "Controller"
scope_cache = {}


#init
def plugin_loaded():
    """ load settings """
    update_settings()
    global_settings = sublime.load_settings(config["FFP_SETTINGS_FILE"])
    global_settings.add_on_change("update", update_settings)


def update_settings():
    """ restart projectFiles with new plugin and project settings """
    # invalidate cache
    global scope_cache
    scope_cache = {}
    # update settings
    global_settings = Settings.update()
    # update project settings
    ProjectManager.initialize(Project, global_settings)


#completions
def get_filepath_completions(view):
	completions = False
	if CurrentFile.is_valid():
	    verbose(ID, "get filepath completions")
	    completions = FuzzyFilePath.get_filepath_completions(scope_cache, view, CurrentFile.get_project_directory(), CurrentFile.get_directory())
	return completions


def on_query_completion_inserted(view, post_remove):
	if Completion.is_active():
	    verbose(ID, "query completion inserted")
	    FuzzyFilePath.update_inserted_filepath(view, post_remove)
	    Completion.stop()


def on_query_completion_aborted():
	Completion.stop()


#project
def on_project_focus(window):
	"""a new window has received focus"""
	verbose(ID, "focus project")
	ProjectManager.update_project(window)


def on_project_activated(window):
	"""a new project has received focus"""
	verbose(ID, "activate project")
	ProjectManager.activate_project(window)


#file
def on_file_created():
	"""a new file has been created"""
	ProjectManager.rebuild_filecache()


def on_file_focus(view):
	CurrentFile.evaluate_current(view, ProjectManager.get_current_project())