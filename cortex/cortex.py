import json
import requests
from typing import List, Tuple

class Cortex:
    def __init__(self, base_url: str = "http://127.0.0.1:39281"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
        self.execute("cortex start")

    def execute(self, command: str):
        # Implement the execute function as needed
        pass

    def get_configuration(self) -> dict:
        response = self.session.get(f"{self.base_url}/v1/configs")
        return response.json()

    def update_configuration(self, config: dict) -> Tuple[int, str]:
        response = self.session.post(f"{self.base_url}/v1/configs", json=config)
        return response.status_code, response.text

    def get_server_health(self) -> int:
        response = self.session.get(f"{self.base_url}/healthz")
        return response.status_code

    def terminate_server(self) -> int:
        response = self.session.delete(f"{self.base_url}/processManager/destroy")
        return response.status_code

    def get_models(self) -> List[dict]:
        response = self.session.get(f"{self.base_url}/v1/models")
        return response.json().get('data', [])

    def start_model(self, model: dict) -> Tuple[int, str]:
        response = self.session.post(f"{self.base_url}/v1/models/start", json=model)
        return response.status_code, response.text

    def stop_model(self, model: str) -> Tuple[int, str]:
        response = self.session.post(f"{self.base_url}/v1/models/stop", json={"model": model})
        return response.status_code, response.text

    def delete_model(self, model: str) -> dict:
        response = self.session.delete(f"{self.base_url}/v1/models/{model}")
        return response.json()

    def get_model(self, model: str) -> dict:
        response = self.session.get(f"{self.base_url}/v1/models/{model}")
        return response.json()

    def update_model(self, model: str, update_request: dict) -> dict:
        response = self.session.patch(f"{self.base_url}/v1/models/{model}", json=update_request)
        return response.json()

    def add_remote_model(self, request: dict) -> dict:
        response = self.session.post(f"{self.base_url}/v1/models/add", json=request)
        return response.json()

    def import_model(self, request: dict) -> dict:
        response = self.session.post(f"{self.base_url}/v1/models/import", json=request)
        return response.json()

    def stop_model_download(self, task_id: str) -> dict:
        response = self.session.delete(f"{self.base_url}/v1/models/pull", json={"taskId": task_id})
        return response.json()

    def pull_model(self, request: dict) -> dict:
        response = self.session.post(f"{self.base_url}/v1/models/pull", json=request)
        return response.json()

    def remove_model_source(self, request: dict) -> dict:
        response = self.session.delete(f"{self.base_url}/v1/models/sources", json=request)
        return response.json()

    def add_model_source(self, source_path: str) -> dict:
        response = self.session.post(f"{self.base_url}/v1/models/", json={"source": source_path})
        return response.json()

    def get_threads(self) -> List[dict]:
        response = self.session.get(f"{self.base_url}/v1/threads")
        return response.json().get('data', [])

    def create_thread(self, title: str) -> dict:
        response = self.session.post(f"{self.base_url}/v1/threads", json={"metadata": {"title": title}})
        return response.json()

    def delete_thread(self, thread_id: str) -> dict:
        response = self.session.delete(f"{self.base_url}/v1/threads/{thread_id}")
        return response.json()

    def get_thread(self, thread_id: str) -> dict:
        response = self.session.get(f"{self.base_url}/v1/threads/{thread_id}")
        return response.json()

    def update_thread_metadata(self, thread_id: str, request: dict) -> str:
        response = self.session.put(f"{self.base_url}/v1/threads/{thread_id}", json=request)
        return response.text

    def get_messages(self, thread_id: str, query_parameters: dict) -> dict:
        response = self.session.get(f"{self.base_url}/v1/threads/{thread_id}/messages", params=query_parameters)
        return response.json()

    def create_message(self, thread_id: str, content: dict) -> dict:
        response = self.session.post(f"{self.base_url}/v1/threads/{thread_id}/messages", json=content)
        return response.json()

    def delete_message(self, thread_id: str, message_id: str) -> dict:
        response = self.session.delete(f"{self.base_url}/v1/threads/{thread_id}/messages/{message_id}")
        return response.json()

    def retrieve_message(self, thread_id: str, message_id: str) -> dict:
        response = self.session.get(f"{self.base_url}/v1/threads/{thread_id}/messages/{message_id}")
        return response.json()

    def modify_message_metadata(self, thread_id: str, message_id: str, metadata: str) -> dict:
        response = self.session.patch(f"{self.base_url}/v1/threads/{thread_id}/messages/{message_id}", json={"metadata": metadata})
        return response.json()

    def get_hardware(self) -> dict:
        response = self.session.get(f"{self.base_url}/v1/hardware")
        return response.json()

    def activate_gpus(self, gpus: dict) -> dict:
        response = self.session.post(f"{self.base_url}/v1/hardware/activate", json=gpus)
        return response.json()

    def get_files(self) -> List[dict]:
        response = self.session.get(f"{self.base_url}/v1/files")
        return response.json().get('data', [])

    def upload_file(self, file_path: str, purpose: str) -> dict:
        with open(file_path, 'rb') as file:
            files = {'file': (file_path, file), 'purpose': (None, purpose)}
            response = self.session.post(f"{self.base_url}/v1/files", files=files)
        return response.json()

    def delete_file(self, file_id: str) -> dict:
        response = self.session.delete(f"{self.base_url}/v1/files/{file_id}")
        return response.json()

    def retrieve_file(self, file_id: str) -> dict:
        response = self.session.get(f"{self.base_url}/v1/files/{file_id}")
        return response.json()

    def get_file_content(self, file_id: str, save_path: str, thread: str = None):
        params = {'thread': thread} if thread else {}
        response = self.session.get(f"{self.base_url}/v1/files/{file_id}/content", params=params)
        with open(save_path, 'wb') as file:
            file.write(response.content)

    def get_installed_engines(self, engine_name: str) -> List[dict]:
        response = self.session.get(f"{self.base_url}/v1/engines/{engine_name}")
        return response.json()

    def get_default_engine(self, engine_name: str) -> dict:
        response = self.session.get(f"{self.base_url}/v1/engines/{engine_name}/default")
        return response.json()

    def set_default_engine_variant(self, engine_name: str, variant: dict) -> dict:
        response = self.session.post(f"{self.base_url}/v1/engines/{engine_name}/default", json=variant)
        return response.json()

    def uninstall_engine(self, engine_name: str, variant: dict) -> dict:
        response = self.session.delete(f"{self.base_url}/v1/engines/{engine_name}/install", json=variant)
        return response.json()

    def install_engine(self, engine_name: str, specification: dict) -> dict:
        response = self.session.post(f"{self.base_url}/v1/engines/{engine_name}/install", json=specification)
        return response.json()

    def unload_engine(self, engine_name: str) -> dict:
        response = self.session.delete(f"{self.base_url}/v1/engines/{engine_name}/load")
        return response.json()

    def load_engine(self, engine_name: str) -> dict:
        response = self.session.post(f"{self.base_url}/v1/engines/{engine_name}/load")
        return response.json()

    def get_released_engines(self, engine_name: str) -> List[dict]:
        response = self.session.get(f"{self.base_url}/v1/engines/{engine_name}/releases")
        return response.json()

    def get_latest_engine_release(self, engine_name: str) -> List[dict]:
        response = self.session.get(f"{self.base_url}/v1/engines/{engine_name}/releases/latest")
        return response.json()

    def update_engine(self, engine_name: str) -> dict:
        response = self.session.post(f"{self.base_url}/v1/engines/{engine_name}/update")
        return response.json()

    def create_embedding(self, embedding_request: dict) -> List[dict]:
        response = self.session.post(f"{self.base_url}/embeddings", json=embedding_request)
        return response.json()

    def create_chat_completion(self, request: dict) -> dict:
        response = self.session.post(f"{self.base_url}/v1/chat/completions", json=request)
        return response.json()