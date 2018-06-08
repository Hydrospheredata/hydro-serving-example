package RRCF


class RRCF(val forestParams: ForestParams, initialData: Array[DataPoint]) {

  require(initialData.length >= forestParams.treesNum * forestParams.samplesNum + forestParams.shingleSize - 1)

  val trees = new Array[RRCT](forestParams.treesNum)
  val shingledData: List[DataPoint] = initialData.sliding(forestParams.shingleSize, 1).map(x => DataPoint(x.flatMap(_.array).toArray)).toList
  val shuffledInitShingles: List[DataPoint] = scala.util.Random.shuffle(shingledData)
  val shingler = new Shingler(initialData.takeRight(forestParams.shingleSize))

  (0 until forestParams.treesNum).par.foreach(index => trees(index) =
    new RRCT(shuffledInitShingles.slice(index * forestParams.samplesNum, (index + 1) * forestParams.samplesNum).toArray))

  def recieve(dataPoint: DataPoint): Double = {
    val newShingle = shingler.insert(dataPoint)
    val score = trees.par.map(_.calculateCoDisplacement(newShingle)).sum / forestParams.treesNum
    trees.par.foreach(_.insertDatapoint(newShingle))
    score
  }
}
