package RRCF

import scala.util.Random


sealed trait Reservoir {
  /**
    * Insert element in the reservoir. There is a chance that element will not be inserted.
    *
    * @param point new element
    * @return deleted element (if it was deleted, else None)
    */
  def insert(point: DataPoint): Option[DataPoint]
}

class TimeDecayReservoir(var timeDecay: Int, storage: Array[DataPoint]) extends Reservoir {
  val pointsStorage: Array[TimestampedDataPoint] = storage.map(new TimestampedDataPoint(0, _)).clone()
  var sizeCounter = 0
  val size: Long = pointsStorage.length
  val r = new Random()

  // Exponentially weight points according to their timestamps
  private def scorePoint(point: TimestampedDataPoint): Double = {
    // TODO increasing coefficient in the nominator will smooth  exponent?
    math.pow(r nextDouble(), 1.0 / (timeDecay - point.timestamp))
  }


  // Compute scores for every point in reservoir. Lowest score is threshold for adding new point
  // New point is swapped with point with the lowest score
  override def insert(newPoint: DataPoint): Option[DataPoint] = {

    val (minIndex, minScore) = pointsStorage.zipWithIndex map { case (point, index) => (index, scorePoint(point)) } minBy (_._2)
    val newScore = math.pow(r.nextDouble(), 1.0 / timeDecay)
    //      println(newScore, minScore)
    if (minScore < newScore) {
      val oldPoint = pointsStorage(minIndex).copy()
      pointsStorage.update(minIndex, new TimestampedDataPoint(0, newPoint))
      pointsStorage.foreach(_.incrementTimestamp())
      Some(oldPoint)
    } else {
      None
    }

  }

  class TimestampedDataPoint(var timestamp: Long, val point: DataPoint) extends DataPoint(point.array) {
    def incrementTimestamp(): Unit = {
      timestamp += 1
    }
  }

}
