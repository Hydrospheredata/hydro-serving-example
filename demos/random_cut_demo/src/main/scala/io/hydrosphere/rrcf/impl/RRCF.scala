package io.hydrosphere.rrcf.impl

import java.io._


class RRCF(val forestParams: ForestParams, val initialData: Array[DataPoint]) {

  require(initialData.length == forestParams.warmupPointsNum)

  val trees = new Array[RRCT](forestParams.treesNum)
  val shingledData: Array[DataPoint] = initialData.sliding(forestParams.shingleSize, 1).map(x => DataPoint(x.flatMap(_.array))).toArray
  assert(shingledData.length == forestParams.samplesNum)
  val shingler = new Shingler(initialData.takeRight(forestParams.shingleSize))

  (0 until forestParams.treesNum).par.foreach(index => trees(index) = new RRCT(shingledData))

  def recieve(dataPoint: DataPoint): Double = {
    val newShingle = shingler.insert(dataPoint)
    val score = trees.par.map(_.calculateCoDisplacement(newShingle)).sum / forestParams.treesNum
    trees.par.foreach(_.insertDatapoint(newShingle))
    score
  }

  def averageTreeIntersection = {
    def intersectionRate(tree1: RRCT, tree2: RRCT): Double = {
      val commonDatapoints: Double = tree1.leafStorage.keySet.intersect(tree2.leafStorage.keySet).size.toDouble
      commonDatapoints / tree1.leafStorage.keySet.size
    }

    val intersectionRates = trees.toSeq.combinations(2).map { case Seq(a, b) => intersectionRate(a, b) }
    intersectionRates.foldLeft((0.0, 1)) { case ((avg, idx), next) => (avg + (next - avg) / idx, idx + 1) }._1
  }


}
