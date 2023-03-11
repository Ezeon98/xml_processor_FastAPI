import json
import requests


class FieldFilterConnector:
    def __init__(self, base_url: str, logger=object) -> None:
        """Allows you to interact with the datareader API"""
        self._logger = logger
        self._base_url = base_url

    def auth(self, user: str, password: str) -> None:
        """It authenticates itself in the API and generates the token"""
        try:
            header = {"Content-Type": "application/json"}

            payload = json.dumps({"username": user, "password": password})

            self._logger.info("Realizando autenticacion con API.")

            response = requests.post(f"{self._base_url}/api/auth", headers=header, data=payload)

            if response.status_code == 200:
                message = json.loads(response.text)
                self._token = message["token"]
                self._logger.info("Autenticacion realizada con exito.")
                print("Autenticacion realizada con exito.")

        except Exception as ex:
            self._logger.error("Ocurrio un error al intentar obtener el token.")
            raise ex

    def charge_db(self, field_name: str, field_value: str):
        try:
            header = {"Authorization": f"Bearer {self._token}"}

            payload = json.dumps({"field_name": field_name, "field_value": field_value})

            self._logger.info(f"Cargando campo {field_name}, valor: {field_value}")
            session = requests.Session()
            session.max_redirects = 60
            init_session = session.get(self._base_url)
            if init_session.status_code == 200:
                response = session.post(
                    f"{self._base_url}/api/field/", headers=header, data=payload
                )
                if response.status_code == 200:
                    message = json.loads(response.text)
                    self._logger.info(f"Campo cargado con exito: {message}")
                    return True
                else:
                    self._logger.error(
                        f"No se pudo cargar {field_name} - {field_value} en base de datos"
                    )
                    return False
            else:
                raise Exception

        except Exception:
            self._logger.error(("No se pudo conectar a la base de datos"))

    def remove_field_filters(self, field_name: str):
        try:
            header = {"Authorization": f"Bearer {self._token}"}

            payload = json.dumps({"field_name": field_name})

            self._logger.info(f"Eliminando valores del campo: {field_name}")

            response = requests.post(
                f"{self._base_url}/api/field/remove", headers=header, data=payload
            )
            if response.status_code == 200:
                message = json.loads(response.text)
                self._logger.info(f"Se eliminaron registros de campo: {message}")
                return True
            else:
                self._logger.info(f"No se pudo eleminar registros de campo: {field_name}")
                return False
        except Exception:
            self._logger.error(("No se pudo eliminar campo en base de datos"))

    def search_fields(self, field_name: str, field_value: str):
        try:
            header = {"Authorization": f"Bearer {self._token}"}

            payload = json.dumps({"field_name": field_name, "field_value": field_value})

            self._logger.info(f"Buscando campos {field_name}, valor: {field_value}")
            session = requests.Session()
            session.max_redirects = 60
            init_session = session.get(self._base_url)
            if init_session.status_code == 200:
                response = session.post(
                    f"{self._base_url}/api/field/search", headers=header, data=payload
                )
                if response.status_code == 200:
                    message = json.loads(response.text)
                    self._logger.info(f"Valor encontrado con exito: {field_value}")
                    return message
                else:
                    self._logger.error(
                        f"No se pudo encontrar {field_name} - {field_value} en base de datos"
                    )
                    return False
            else:
                raise Exception

        except Exception:
            self._logger.error(("No se pudo conectar a la base de datos"))
