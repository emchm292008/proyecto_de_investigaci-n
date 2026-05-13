"""Paquete de controladores."""

from .entidades_controller import router as entidades_controller
from .investigacion_controller import router as investigacion_controller

__all__ = ["entidades_controller", "investigacion_controller"]