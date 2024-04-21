from json import dumps as json_dumps
from typing import Any, Dict, Union

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from employee.employee_service_impl import employee_service_impl
from employee.models import Employee
from employee.schemas import EmployeeIn
from employee.views import router
from ninja import NinjaAPI, Router
from ninja.responses import NinjaJSONEncoder
from ninja.testing import TestClient
from ninja_jwt.routers.obtain import obtain_pair_router


class TokenTestClient(TestClient):
    def __init__(self, router_or_app: Union[NinjaAPI, Router], token: str) -> None:
        super().__init__(router_or_app)
        self.token = token

    def request(
        self,
        method: str,
        path: str,
        data: Dict = {},
        json: Any = None,
        **request_params: Any,
    ) -> "NinjaResponse":
        h = {"headers": {"Authorization": f"Bearer {self.token}"}}
        request_params.update(h)
        if json is not None:
            request_params["body"] = json_dumps(json, cls=NinjaJSONEncoder)
        func, request, kwargs = self._resolve(method, path, data, request_params)
        return self._call(func, request, kwargs)  # type: ignore


class HelloTest(TestCase):
    def setUp(self):
        self.employee_in = EmployeeIn(
            first_name="John",
            last_name="Doe",
            department_id=1,
        )
        employee_service_impl.create_obj(payload=self.employee_in, user_email="huacai")

        login_client = TestClient(obtain_pair_router)
        d = {"password": "string", "username": "string"}
        User = get_user_model()
        User.objects.create_superuser(**d)

        resp = login_client.post("/pair", json=d).json()
        token = resp["data"]["access"]
        self.token_client = TokenTestClient(router, token)

    def test_get_obj(self):
        response = self.token_client.get("/employees/1")

        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset(
            self.employee_in.dict(),
            response.json()["data"],
            f"query input obj: {self.employee_in}",
        )

    def test_create_obj(self):
        create_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "department_id": 2,
        }
        response = self.token_client.post("/employees", json=create_data)
        self.assertEqual(response.status_code, 200)
        # Check if returned object matches created object
        self.assertEqual(response.json()["data"]["id"], 2)

    def test_list_obj(self):
        response = self.token_client.get("/employees")
        self.assertEqual(response.status_code, 200)
        # Check if response contains list of employees
        self.assertIsInstance(response.json()["data"]["details"], list)
        self.assertEqual(
            response.json()["data"]["details"][0]["first_name"],
            self.employee_in.first_name,
        )

    def test_update_obj(self):
        update_data = {
            "first_name": " Updated",
            "last_name": " Name",
            "department_id": 1,
        }
        response = self.token_client.put("/employees/1", json=update_data)
        self.assertEqual(response.status_code, 200)

        update_data_response = self.token_client.get("/employees/1")

        # Check if the object is updated correctly
        self.assertEqual(
            update_data_response.json()["data"]["first_name"], update_data["first_name"]
        )

    def test_partial_update_obj(self):
        partial_update_data = {"first_name": "Partially Updated"}
        response = self.token_client.patch("/employees/1", json=partial_update_data)
        self.assertEqual(response.status_code, 200)
        # Check if the object is partially updated correctly

        update_data_response = self.token_client.get("/employees/1")

        # Check if the object is updated correctly
        self.assertEqual(
            update_data_response.json()["data"]["first_name"],
            partial_update_data["first_name"],
        )

    def test_delete_obj(self):
        response = self.token_client.delete("/employees/1")
        self.assertEqual(response.status_code, 200)
        # Check if object does not exist anymore
        with self.assertRaises(ObjectDoesNotExist):
            Employee.objects.get(pk=1, is_deleted=False)
