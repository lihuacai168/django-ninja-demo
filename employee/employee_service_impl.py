# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: 花菜
# @File: employee_service_impl.py
# @Time : 2023/6/15 11:01
# @Email: lihuacai168@gmail.com

from core.service import GenericCURDSoftDelete
from employee.models import Employee


class EmployeeServiceImpl(GenericCURDSoftDelete):
    """
    Employee CURD service
    """

    def __init__(self):
        super(EmployeeServiceImpl, self).__init__(model=Employee)


employee_service_impl = EmployeeServiceImpl()
