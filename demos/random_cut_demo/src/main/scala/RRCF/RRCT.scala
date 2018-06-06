package RRCF


import scala.collection.mutable
import scala.util.Random


// TODO make RRCT care about shingles? If so, the influence of outlier on neighbour normal nodes will be diminished(?)
// TODO
class RRCT(initialData: Array[DataPoint], timeDecay: Int = 1000) {
  val r = new Random()
  val treeSize: Int = initialData.length
  val leafStorage = new mutable.ListBuffer[Leaf]()
  private[this] val initialLeaf = Leaf(initialData(0), None) // TODO do not generate this class field
  var rootNode: Tree = initialLeaf
  leafStorage.append(initialLeaf) // TODO change to hashtable
  val reservoir: Reservoir = new TimeDecayReservoir(timeDecay, initialData)
  initialData.drop(1).foreach(initializeWithDatapoint)


  /**
    * Given new datapoint calculate it's position in the tree.
    * Calculated position has link to it's parent and it's children,
    * but other nodes in the tree do not have link to this node.
    *
    * Dimension and coordinate to cut are determined proportionally to dimension's diameter.
    * If dimension and coordinate separates newDatapoint and possibleSiblingNode - than cut is correct and returned.
    * Else, go deeper in the tree according to the cutNode and try to cut again.
    *
    * @param newDataPoint new datapoint
    * @return calculated CutNode
    */
  private[this] def calculateRandomCut(newDataPoint: DataPoint, possibleSiblingNode: Tree): Option[CutNode] = {
    val dataPointBoundingBox = new BoundingBox(newDataPoint)
    val commonBoundingBox = dataPointBoundingBox.union(possibleSiblingNode.boundingBox)
    val diameters = commonBoundingBox.minValues zip commonBoundingBox.maxValues map { case (min, max) => max - min }
    val diameterCut = diameters.sum * r.nextDouble() // TODO it samples from semi-interval [0;1) but we need [0;1]
    val dimensionCut = diameters.indices.view.map(i => (i, diameters.take(i + 1).sum >= diameterCut)).find(_._2).head._1
    val previousDimensionsOffset = diameters.take(dimensionCut).sum
    val coordinateCut = commonBoundingBox.minValues(dimensionCut) + diameterCut - previousDimensionsOffset
    assert(commonBoundingBox.contains(dimensionCut, coordinateCut))
    possibleSiblingNode match {
      case siblingCutNode: CutNode =>
        if (!siblingCutNode.boundingBox.contains(dimensionCut, coordinateCut)) {

          val returnNode: CutNode = new CutNode(dimensionCut, coordinateCut, 1 + siblingCutNode.childrenSize,
            commonBoundingBox, left = null, right = null, siblingCutNode.parent)
          val leaf = Leaf(newDataPoint, Some(returnNode))
          if (newDataPoint.array(dimensionCut) <= coordinateCut) {
            returnNode.left = leaf
            returnNode.right = siblingCutNode
          } else {
            returnNode.left = siblingCutNode
            returnNode.right = leaf
          }
          Some(returnNode)
        } else {
          if (siblingCutNode.isDatapointInLeftSubtree(newDataPoint)) {
            calculateRandomCut(newDataPoint, siblingCutNode.left)
          } else {
            calculateRandomCut(newDataPoint, siblingCutNode.right)
          }
        }
      case siblingLeaf: Leaf =>
        if (siblingLeaf.dataPoint.equals(newDataPoint)) {
          siblingLeaf.parent
        } else {
          val returnNode = new CutNode(dimensionCut, coordinateCut, 1 + siblingLeaf.childrenSize,
            commonBoundingBox, left = null, right = null, siblingLeaf.parent)
          val leaf = Leaf(newDataPoint, Some(returnNode))
          if (returnNode.isDatapointInLeftSubtree(newDataPoint)) {
            returnNode.left = leaf
            returnNode.right = siblingLeaf
          } else {
            returnNode.right = leaf
            returnNode.left = siblingLeaf
          }
          Some(returnNode)
        }
    }
  }

  /**
    * Calculate collusive displacement of the new datapoint. To calculate collusive displacement you must calculate
    * |children(sibling(x))|/|children(x)| for every x in path from new datapoint leaf to root.
    *
    * @param dataPoint evaluated datapoint
    * @return maximum collusive displacement found.
    */
  def calculateCoDisplacement(dataPoint: DataPoint): Double = {

    val coDisplacementEvaluator = (data: (CutNode, Boolean)) => {
      data match {
        case (node: CutNode, isLeft: Boolean) => if (isLeft) node.right.childrenSize.toDouble / node.left.childrenSize
        else node.left.childrenSize.toDouble / node.right.childrenSize
      }
    }

    val shadowCut = calculateRandomCut(dataPoint, rootNode)

    shadowCut match {
      case None => 0.0 // if new cut has no cutNode - the tree consists only of duplicates, hence they are not anomalous
      case Some(shadowCutNode) =>
        val pathToRoot = mutable.ListBuffer.empty[(CutNode, Boolean)]
        var tempNode = shadowCutNode
        pathToRoot.append((tempNode, tempNode.isDatapointInLeftSubtree(dataPoint)))
        while (tempNode.parent.isDefined) {
          val parent = tempNode.parent.get
          pathToRoot.append((parent, parent.left == tempNode))
          tempNode = tempNode.parent.get
        }
        pathToRoot.map(coDisplacementEvaluator).max
    }
  }


  /**
    * Try to insert new datapoint in the tree. Point is not guaranteed to be inserted, since reservoir
    * decides whether to add points randomly.
    *
    * @param dataPoint new datapoint.
    * @return True if it was inserted by reservoir, hence inserted in the tree, False otherwise.
    */
  def insertDatapoint(dataPoint: DataPoint): Boolean = {
    reservoir.insert(dataPoint) match {
      case None => false
      case Some(deletedDatapoint) =>
        deleteDatapoint(deletedDatapoint)
        initializeWithDatapoint(dataPoint)
        assert(rootNode.childrenSize == treeSize)
        true
    }
  }

  /**
    * Insert datapoint in the tree and propagate changes with childrenSize and boundingBox to the top.
    *
    * @param dataPoint
    */
  def initializeWithDatapoint(dataPoint: DataPoint): Unit = {
    val newCut = calculateRandomCut(dataPoint, rootNode)
    val oldChildrenSize = rootNode.childrenSize // For post-condition
    newCut match {
      case None => rootNode.childrenSize += 1; // This is happening only in case if duplicate leaf was added to the root node without cutNodes
      case Some(newCutNode) =>

        if (newCutNode.isDatapointInLeftSubtree(dataPoint)) {
          //Duplicate check
          leafStorage.find(_.dataPoint.equals(dataPoint)) match {
            case Some(duplicateLeaf) => newCutNode.left = duplicateLeaf; duplicateLeaf.childrenSize += 1
            case None => leafStorage.append(newCutNode.left.asInstanceOf[Leaf])
          }
          newCutNode.right.parent = Some(newCutNode)
        } else {
          //Duplicate check
          leafStorage.find(_.dataPoint.equals(dataPoint)) match {
            case Some(duplicateLeaf) => newCutNode.right = duplicateLeaf; duplicateLeaf.childrenSize += 1
            case None => leafStorage.append(newCutNode.right.asInstanceOf[Leaf])
          }
          newCutNode.left.parent = Some(newCutNode)
        }
        newCutNode.parent match {
          case None => rootNode = newCutNode; // If new cut node has no parents - it's the new root node
          case Some(parent) => if (parent.isDatapointInLeftSubtree(dataPoint)) parent.left = newCutNode else parent.right = newCutNode
        }
        newCutNode.updateBoundingBox()
        newCutNode.updateChildrenSize()
    }
    assert(rootNode.childrenSize - 1 == oldChildrenSize)
  }

  /**
    * Given DataPoint delete it from the tree structure. This is the utility method which should be only invoked from
    * insertDatapoint method
    *
    * @param dataPoint
    */
  private[this] def deleteDatapoint(dataPoint: DataPoint): Unit = {
    val leaf = locateDatapointInTree(dataPoint)
    if (leaf.childrenSize > 1) { // If leaf has duplicates, simply delete one of the duplicates without changing tree
      leaf.childrenSize -= 1
      leaf.parent.foreach(_.updateChildrenSize())
    } else {
      leaf.parent match { // Else delete leaf's parent and attach  leaf's parent's sibling to the grandparent
        case None => throw new Exception("Deleting is launched too soon.")
        case Some(parent) =>
          val sibling = parent.getAnotherSibling(leaf)
          parent.parent match {
            case None =>
              rootNode = sibling; sibling.parent = None; // Sibling become root if sole leaf of root is deleted
            case Some(grandParent) =>
              if (grandParent.isDatapointInLeftSubtree(dataPoint)) grandParent.left = sibling else grandParent.right = sibling
              sibling.parent = Some(grandParent)
              grandParent.updateBoundingBox()
              grandParent.updateChildrenSize()
          }
          leafStorage.remove(leafStorage.zipWithIndex.find(_._1.dataPoint.equals(dataPoint)).get._2)
      }
    }
    assert(rootNode.childrenSize == treeSize - 1)
  }

  /**
    * Given datapoint return correspoing leaf from the tree by looking into the linked list with all leafs
    *
    * @param dataPoint
    * @return
    */
  private[this] def locateDatapointInTree(dataPoint: DataPoint): Leaf = {

    // TODO decide what to do with older version
    //    def locateDatapointFromNode(dataPoint: DataPoint, node: Tree): Leaf = {
    //      node match {
    //        case cutNode: CutNode =>
    //          if (cutNode.isDatapointInLeftSubtree(dataPoint)) {
    //            locateDatapointFromNode(dataPoint, cutNode.left)
    //          } else {
    //            locateDatapointFromNode(dataPoint, cutNode.right)
    //          }
    //        case leaf: Leaf => if (leaf.dataPoint.equals(dataPoint)) leaf else throw new Exception("Datapoint is not in the tree.")
    //      }
    //    }

    //    locateDatapointFromNode(dataPoint, rootNode)

    leafStorage.find(_.dataPoint.equals(dataPoint)) match {
      case None => throw new Exception("Datapoint is not in the tree.")
      case Some(leaf) => leaf
    }
  }
}
