from .BaseController import BaseController
import os


class ProjectController(BaseController):
    def __init__(self):
        super().__init__()

    def get_project_path(self, project_id: str):
        if not project_id or project_id in {".", ".."} or "/" in project_id or "\\" in project_id:
            raise ValueError("Invalid project_id")

        project_dir = os.path.join(self.files_dir, project_id)
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)

        return project_dir
