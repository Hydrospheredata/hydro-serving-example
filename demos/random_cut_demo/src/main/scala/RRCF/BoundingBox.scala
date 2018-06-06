package RRCF

case class BoundingBox(var minValues: Array[Double], var maxValues: Array[Double]) {

  def union(newBoundingBox: BoundingBox): BoundingBox = {
    val newMinValues = this.minValues zip newBoundingBox.minValues map { case (oldMin, newMin) => oldMin.min(newMin) }
    val newMaxValues = this.maxValues zip newBoundingBox.maxValues map { case (oldMax, newMax) => oldMax.max(newMax) }
    BoundingBox(newMinValues, newMaxValues)
  }

  /**
    * Check what this particular cut is containted in this bb
    *
    * @param dimension
    * @param coordinate
    * @return
    */
  def contains(dimension: Int, coordinate: Double): Boolean = {
    (minValues(dimension) <= coordinate) && (coordinate <= maxValues(dimension))
  }

  /**
    * Check whether datapoint belongs to this bb
    *
    * @param dataPoint
    * @return
    */
  def contains(dataPoint: DataPoint): Boolean = {
    minValues zip dataPoint.array zip maxValues map { case ((min, point), max) => (min <= point) && (point <= max) } forall identity
  }

  // Bounding box of datapoint is datapoint (minValues == datapoint == maxValues)
  def this(dataPoint: DataPoint) = this(dataPoint.array, dataPoint.array)
}
