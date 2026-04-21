"""Assembly module for combining multiple shapes into a compound structure.

Provides the Assembly class which allows building hierarchical assemblies
of CadQuery shapes with location/transform support.
"""

from typing import Optional, List, Tuple, Union, Dict
from OCP.TopoDS import TopoDS_Compound
from OCP.BRep import BRep_Builder
from OCP.TopLoc import TopLoc_Location
from OCP.gp import gp_Trsf

from .shapes import Shape
from .geom import Vector


class Assembly:
    """A hierarchical assembly of shapes.

    Assemblies allow combining multiple shapes into a single compound,
    with optional per-child location transforms.

    Example::

        asm = Assembly(name="my_assembly")
        asm.add(box, name="box", loc=Vector(0, 0, 0))
        asm.add(cylinder, name="cyl", loc=Vector(10, 0, 0))
        compound = asm.toCompound()
    """

    def __init__(
        self,
        shape: Optional[Shape] = None,
        name: Optional[str] = None,
        loc: Optional[Vector] = None,
    ):
        """Initialize an Assembly.

        Args:
            shape: Optional root shape for this assembly node.
            name: Optional name for this assembly.
            loc: Optional translation vector for this assembly node.
                 Defaults to origin (0, 0, 0).
        """
        # Default name falls back to "root" to make it clearer this is a
        # top-level node when no explicit name is provided.
        self.name = name or "root"
        self.shape = shape
        self.loc = loc or Vector(0, 0, 0)
        self.children: List[Tuple["Assembly", str]] = []
        self._metadata: Dict[str, object] = {}

    def add(
        self,
        item: Union[Shape, "Assembly"],
        name: Optional[str] = None,
        loc: Optional[Vector] = None,
    ) -> "Assembly":
        """Add a shape or sub-assembly to this assembly.

        Args:
            item: A Shape or Assembly to add as a child.
            name: Optional name for the child node.
            loc: Optional translation offset for the child.

        Returns:
            self, to allow method chaining.
        """
        if isinstance(item, Shape):
            child = Assembly(shape=item, name=name, loc=loc)
        elif isinstance(item, Assembly):
            child = item
            if name is not None:
                child.name = name
            if loc is not None:
                child.loc = loc
        else:
            raise TypeError(f"Expected Shape or Assembly, got {type(item)}")

        self.children.append((child, child.name))
        return self

    def toCompound(self) -> Shape:
        """Convert this assembly to a single TopoDS_Compound Shape.

        All child shapes are combined into a compound, with location
        transforms applied.

        Returns:
            A Shape wrapping a TopoDS_Compound.
        """
        builder = BRep_Builder()
        compound = TopoDS_Compound()
        builder.MakeCompound(compound)

        self._addToCompound(builder, compound, self.loc)

        return Shape(compound)

    def _addToCompound(
        self,
        builder: BRep_Builder,
        compound: TopoDS_Compound,
        parent_loc: V
