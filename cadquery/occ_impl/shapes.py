"""Core shape wrappers around OpenCASCADE topology.

This module provides Python-friendly wrappers around the OCC BRep topology
classes, forming the foundation for all solid modeling operations in CadQuery.
"""

from typing import Optional, Tuple, Union, List

from OCC.Core.TopoDS import (
    TopoDS_Shape,
    TopoDS_Vertex,
    TopoDS_Edge,
    TopoDS_Wire,
    TopoDS_Face,
    TopoDS_Shell,
    TopoDS_Solid,
    TopoDS_Compound,
)
from OCC.Core.BRep import BRep_Builder
from OCC.Core.BRepBuilderAPI import (
    BRepBuilderAPI_MakeVertex,
    BRepBuilderAPI_MakeEdge,
    BRepBuilderAPI_MakeFace,
    BRepBuilderAPI_MakeSolid,
)
from OCC.Core.BRepPrimAPI import (
    BRepPrimAPI_MakeBox,
    BRepPrimAPI_MakeCylinder,
    BRepPrimAPI_MakeSphere,
)
from OCC.Core.BRepAlgoAPI import (
    BRepAlgoAPI_Fuse,
    BRepAlgoAPI_Cut,
    BRepAlgoAPI_Common,
)
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Ax2, gp_Dir
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop_VolumeProperties, brepgprop_SurfaceProperties
from OCC.Core.TopAbs import TopAbs_SOLID, TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX
from OCC.Core.TopExp import TopExp_Explorer

from .geom import Vector


class Shape:
    """Base class for all CadQuery shapes wrapping a TopoDS_Shape."""

    def __init__(self, obj: TopoDS_Shape):
        self._shape = obj

    @property
    def wrapped(self) -> TopoDS_Shape:
        """Return the underlying OCC shape object."""
        return self._shape

    def is_null(self) -> bool:
        """Return True if the shape is null (uninitialized)."""
        return self._shape.IsNull()

    def volume(self) -> float:
        """Compute the volume of the shape. Returns 0.0 for non-solid shapes."""
        props = GProp_GProps()
        brepgprop_VolumeProperties(self._shape, props)
        return props.Mass()

    def area(self) -> float:
        """Compute the surface area of the shape."""
        props = GProp_GProps()
        brepgprop_SurfaceProperties(self._shape, props)
        return props.Mass()

    def center_of_mass(self) -> Vector:
        """Return the center of mass of the shape."""
        props = GProp_GProps()
        brepgprop_VolumeProperties(self._shape, props)
        c = props.CentreOfMass()
        return Vector(c.X(), c.Y(), c.Z())

    def fuse(self, other: "Shape") -> "Shape":
        """Boolean union of this shape with another."""
        fuse_op = BRepAlgoAPI_Fuse(self._shape, other._shape)
        fuse_op.Build()
        return Shape(fuse_op.Shape())

    def cut(self, other: "Shape") -> "Shape":
        """Boolean subtraction of another shape from this one."""
        cut_op = BRepAlgoAPI_Cut(self._shape, other._shape)
        cut_op.Build()
        return Shape(cut_op.Shape())

    def intersect(self, other: "Shape") -> "Shape":
        """Boolean intersection of this shape with another."""
        common_op = BRepAlgoAPI_Common(self._shape, other._shape)
        common_op.Build()
        return Shape(common_op.Shape())

    def __repr__(self) -> str:
        return f"<Shape: {type(self._shape).__name__}>"


class Solid(Shape):
    """Represents a 3D solid body."""

    @classmethod
    def make_box(
        cls,
        length: float,
        width: float,
        height: float,
        pnt: Optional[Vector] = None,
    ) -> "Solid":
        """Create an axis-aligned box.

        Args:
            length: Dimension along X axis.
            width: Dimension along Y axis.
            height: Dimension along Z axis.
            pnt: Optional origin point (default: origin).
        """
        origin = pnt if pnt is not None else Vector(0, 0, 0)
        box = BRepPrimAPI_MakeBox(
            gp_Pnt(origin.x, origin.y, origin.z), length, width, height
        )
        return cls(box.Shape())

    @classmethod
    def make_cylinder(
        cls,
        radius: float,
        height: float,
        pnt: Optional[Vector] = None,
        direction: Optional[Vector] = None,
    ) -> "Solid":
        """Create a cylinder along a given axis.

        Args:
            radius: Radius of the cylinder.
            height: Height of the cylinder.
            pnt: Base center point (default: origin).
            direction: Axis direction (default: Z axis).
        """
        origin = pnt if pnt is not None else Vector(0, 0, 0)
        axis_dir = direction if direction is not None else Vector(0, 0, 1)
        ax2 = gp_Ax2(
            gp_Pnt(origin.x, origin.y, origin.z),
            gp_Dir(axis_dir.x, axis_dir.y, axis_dir.z),
        )
        cyl = BRepPrimAPI_MakeCylinder(ax2, radius, height)
        return cls(cyl.Shape())

    @classmethod
    def make_sphere(
        cls,
        radius: float,
        pnt: Optional[Vector] = None,
    ) -> "Solid":
        """Create a sphere centered at a given point.

        Args:
            radius: Radius of the sphere.
            pnt: Center point (default: origin).
        """
        origin = pnt if pnt is not None else Vector(0, 0, 0)
        sphere = BRepPrimAPI_MakeSphere(
            gp_Pnt(origin.x, origin.y, origin.z), radius
        )
        return cls(sphere.Shape())
