"""CadQuery - A parametric 3D CAD scripting framework.

CadQuery is a Python library that allows you to build 3D models using
a fluent API. It wraps OpenCASCADE Technology (OCCT) via the OCP bindings.

Basic usage::

    import cadquery as cq

    result = cq.Workplane("XY").box(10, 10, 10)
"""

from .cq import (
    CQContext,
    CQObject,
    Workplane,
)
from .occ_impl.geom import (
    Vector,
    Matrix,
    Plane,
    Location,
)
from .occ_impl.shapes import (
    Shape,
    Vertex,
    Edge,
    Wire,
    Face,
    Shell,
    Solid,
    Compound,
)
from .occ_impl.exporters import (
    exporters,
)
from .assembly import (
    Assembly,
    Color,
    Constraint,
)
from .selectors import (
    Selector,
    NearestToPointSelector,
    ParallelDirSelector,
    DirectionSelector,
    PerpendicularDirSelector,
    TypeSelector,
    DirectionMinMaxSelector,
    BinarySelector,
    AndSelector,
    SumSelector,
    SubtractSelector,
    InverseSelector,
    StringSyntaxSelector,
)
from .sketch import Sketch

__version__ = "2.4.0"

__all__ = [
    "Assembly",
    "Color",
    "Compound",
    "Constraint",
    "CQContext",
    "CQObject",
    "Edge",
    "Face",
    "Location",
    "Matrix",
    "Plane",
    "Shape",
    "Shell",
    "Sketch",
    "Solid",
    "Vector",
    "Vertex",
    "Wire",
    "Workplane",
    "Selector",
    "NearestToPointSelector",
    "ParallelDirSelector",
    "DirectionSelector",
    "PerpendicularDirSelector",
    "TypeSelector",
    "DirectionMinMaxSelector",
    "BinarySelector",
    "AndSelector",
    "SumSelector",
    "SubtractSelector",
    "InverseSelector",
    "StringSyntaxSelector",
    "exporters",
    "__version__",
]
