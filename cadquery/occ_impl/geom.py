"""Geometry primitives and transformations for CadQuery.

This module provides Vector, Matrix, and Plane classes used throughout
the CadQuery geometry pipeline.
"""

import math
from typing import Optional, Tuple, Union, overload

from OCP.gp import (
    gp_Vec,
    gp_Pnt,
    gp_Dir,
    gp_Trsf,
    gp_GTrsf,
    gp_XYZ,
    gp_Ax1,
    gp_Ax3,
)


class Vector:
    """A 3D vector with common operations.

    Wraps the OCC gp_Vec class and provides a more Pythonic interface.
    """

    def __init__(self, *args):
        if len(args) == 3:
            self._wrapped = gp_Vec(*args)
        elif len(args) == 1:
            if isinstance(args[0], gp_Vec):
                self._wrapped = args[0]
            elif isinstance(args[0], gp_Pnt):
                self._wrapped = gp_Vec(args[0].XYZ())
            elif isinstance(args[0], gp_Dir):
                self._wrapped = gp_Vec(args[0])
            elif isinstance(args[0], (list, tuple)) and len(args[0]) == 3:
                self._wrapped = gp_Vec(*args[0])
            else:
                raise TypeError(f"Cannot construct Vector from {type(args[0])!r}")
        elif len(args) == 2:
            # 2-arg form: treat as (x, y) in the XY plane, z=0
            self._wrapped = gp_Vec(args[0], args[1], 0)
        else:
            raise TypeError(f"Vector expects 1, 2, or 3 arguments, got {len(args)}")

    @property
    def x(self) -> float:
        return self._wrapped.X()

    @property
    def y(self) -> float:
        return self._wrapped.Y()

    @property
    def z(self) -> float:
        return self._wrapped.Z()

    def Length(self) -> float:
        return self._wrapped.Magnitude()

    def normalized(self) -> "Vector":
        """Return a unit vector in the same direction."""
        return Vector(self._wrapped.Normalized())

    def dot(self, other: "Vector") -> float:
        return self._wrapped.Dot(other._wrapped)

    def cross(self, other: "Vector") -> "Vector":
        return Vector(self._wrapped.Crossed(other._wrapped))

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self._wrapped.Added(other._wrapped))

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self._wrapped.Subtracted(other._wrapped))

    def __mul__(self, scalar: float) -> "Vector":
        return Vector(self._wrapped.Multiplied(scalar))

    def __rmul__(self, scalar: float) -> "Vector":
        return self.__mul__(scalar)

    def __neg__(self) -> "Vector":
        return Vector(self._wrapped.Reversed())

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y}, {self.z})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Vector):
            return self._wrapped.IsEqual(other._wrapped, 1e-9, 1e-9)
        return NotImplemented

    def toPnt(self) -> gp_Pnt:
        return gp_Pnt(self._wrapped.XYZ())

    def toDir(self) -> gp_Dir:
        return gp_Dir(self._wrapped)

    def toTuple(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.z)

    def getAngle(self, ot
