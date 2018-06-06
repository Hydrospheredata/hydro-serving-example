package RRCF

sealed trait Tree {
  var parent: Option[CutNode]
  var boundingBox: BoundingBox
  var childrenSize: Int
}

/**
  * Each CutNode represents non-leaf node in the Tree
  *
  * @param dimension     index of the dimension in which the cut was made
  * @param cutCoordinate value by which cut was made
  * @param childrenSize  number of leaves under that node
  * @param boundingBox   bounding box defined by children of that node.
  * @param left          subtree built with samples which are less or equal than cutCoordinate in selected dimension
  * @param right         subtree built with samples which are greater than cutCoordinate in selected dimension
  */
class CutNode(var dimension: Int, var cutCoordinate: Double, var childrenSize: Int, var boundingBox: BoundingBox,
              var left: Tree, var right: Tree, var parent: Option[CutNode]) extends Tree {

  def isDatapointInLeftSubtree(dataPoint: DataPoint): Boolean = {
    dataPoint.array(dimension) <= cutCoordinate
  }

  /**
    * Recalculate it's children size and propagate till the root
    */
  def updateChildrenSize(): Unit = {
    this.childrenSize = this.left.childrenSize + this.right.childrenSize
    if (this.childrenSize <= 0) throw new Exception("Children size have to be positive")
    this.parent.foreach(_.updateChildrenSize())
  }

  /**
    * Recalulate it's bounding box and propagate till the root
    */
  def updateBoundingBox(): Unit = {
    this.boundingBox = this.left.boundingBox.union(this.right.boundingBox)
    this.parent.foreach(_.updateBoundingBox())
  }

  def getAnotherSibling(child: Tree): Tree = {
    if ((child != this.left) && (child != this.right)) throw new Exception("This is not the direct child of this node.") // Very useful to check links
    if (child == this.left) this.right else this.left
  }

}

case class Leaf(dataPoint: DataPoint, var parent: Option[CutNode]) extends Tree {
  override var boundingBox = new BoundingBox(dataPoint)
  override var childrenSize = 1
}
