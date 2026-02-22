import json
from pathlib import Path
from random import randint

from ..config import app_logger


class WorkflowGenerator:
    def __init__(self, src: str = "resources/workflows"):
        self.src = Path(src)
        self.workflows: dict[str, dict] = {}
        self.SEED_LOW = 10**14
        self.SEED_HIGH = 10**15 - 1

    def get_json(self, file_name: str) -> dict:
        if file_name not in self.workflows:
            try:
                data = (self.src / file_name).read_text()
                self.workflows[file_name] = json.loads(data)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                raise RuntimeError("could not load the workflow") from e
        return self.workflows[file_name]

    def get_seed(self) -> int:
        return randint(self.SEED_LOW, self.SEED_HIGH)

    def get_realistic_image_workflow(
        self, prompt: str, width: int = 1024, height: int = 1024, batch: int = 1
    ):
        file_name = "realistic_image_workflow.json"
        workflow = self.get_json(file_name=file_name)

        try:
            workflow["131"]["inputs"]["text"] = prompt
            workflow["132"]["inputs"]["width"] = width
            workflow["132"]["inputs"]["height"] = height
            workflow["132"]["inputs"]["batch_size"] = batch
            # we can add batch as well in 132
            workflow["133"]["inputs"]["seed"] = self.get_seed()
            return workflow
        except KeyError as e:
            app_logger.critical("realistic image workflow could not be built")
            raise RuntimeError("realistic image workflow could not be built") from e

    def get_product_image_workflow(
        self,
        reference_image_name: str,
        prompt: str,
        width: int = 1024,
        height: int = 1024,
        batch: int = 1,
    ) -> dict:
        file_name = "product_image_workflow.json"
        workflow = self.get_json(file_name=file_name)
        try:
            workflow["47"]["inputs"]["image"] = reference_image_name
            workflow["131"]["inputs"]["text"] = prompt
            workflow["132"]["inputs"]["width"] = width
            workflow["132"]["inputs"]["height"] = height
            workflow["132"]["inputs"]["batch_size"] = batch
            workflow["133"]["inputs"]["seed"] = self.get_seed()
            return workflow
        except KeyError as e:
            app_logger.critical("product photo graphy prompt could not be built")
            raise RuntimeError("product photo graphy prompt could not be built") from e
