package RRCF


import scala.collection.mutable

class Shingler(firstFrame: Seq[DataPoint]) {
  val size: Int = firstFrame.size
  val slidingWindow: mutable.Queue[DataPoint] = scala.collection.mutable.Queue[DataPoint](firstFrame: _*)

  def insert(point: DataPoint): DataPoint = {
    slidingWindow.dequeue()
    slidingWindow.enqueue(point)
    DataPoint(slidingWindow.flatMap(_.array).toArray)
  }
}

