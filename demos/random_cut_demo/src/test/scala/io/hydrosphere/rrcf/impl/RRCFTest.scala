package io.hydrosphere.rrcf.impl

import org.scalatest.FunSuite

import scala.util.Random

class RRCFTest extends FunSuite {

  test("forestOfDuplicates") {

    val fp = ForestParams()
    val initData = for (_ <- 0 until fp.samplesNum + fp.shingleSize - 1) yield DataPoint(Array(2.0, 2.0))

    val forest = new RRCF(fp, initialData = initData.toArray)

    val dataScore = forest.recieve(DataPoint(Array(2.0, 2.0)))
    val outlierScore = forest.recieve(DataPoint(Array(2.0, 2.0)))
    assert(dataScore == outlierScore)
    assert(dataScore == 0)
  }

  test("outlierScoreIsGreater") {
    val r = new scala.util.Random()

    def dataGenerator(r: Random): Array[Double] = {
      Array(r.nextGaussian() / 6 + 2, r.nextGaussian() / 6 + 2)
    }

    def outlierGenerator(r: Random): Array[Double] = {
      Array(r.nextGaussian() / 6 + 3, r.nextGaussian() / 6 + 3)
    }

    val fp = ForestParams()
    val initData = for (_ <- 0 until fp.samplesNum + fp.shingleSize - 1) yield DataPoint(dataGenerator(r))
    val forest = new RRCF(fp, initialData = initData.toArray)

    val dataScore = forest.recieve(DataPoint(dataGenerator(r)))
    val outlierScore = forest.recieve(DataPoint(outlierGenerator(r)))
    assert(dataScore < outlierScore)
  }

  test("repeatedInsertion") {
    val r = new scala.util.Random()

    def dataGenerator(r: Random): Array[Double] = {
      Array(r.nextGaussian() / 6 + 2, r.nextGaussian() / 6 + 2)
    }

    val fp = ForestParams()
    val initData = for (_ <- 0 until fp.samplesNum + fp.shingleSize - 1) yield DataPoint(dataGenerator(r))
    val forest = new RRCF(fp, initialData = initData.toArray)

    (1 to 1000).foreach(_ => forest.recieve(DataPoint(dataGenerator(r))))

  }

  test("repeatedDuplicateInsertionAfterRandomInit") {
    val r = new scala.util.Random()

    def dataGenerator(r: Random): Array[Double] = {
      Array(r.nextGaussian() / 6 + 2, r.nextGaussian() / 6 + 2)
    }

    def constGenerator(r: Random): Array[Double] = {
      Array(2.0, 2.0)
    }

    def constGenerator2(r: Random): Array[Double] = {
      Array(3.0, 3.0)
    }

    val fp = ForestParams()
    val initData = for (_ <- 0 until fp.samplesNum + fp.shingleSize - 1) yield DataPoint(dataGenerator(r))
    val forest = new RRCF(fp, initialData = initData.toArray)

    (1 to 100).foreach(_ => forest.recieve(DataPoint(constGenerator(r))))
    (1 to 100).foreach(_ => forest.recieve(DataPoint(constGenerator2(r))))
  }

  def measureTime[R](task: String)(block: => R): R = {
    val t0 = System.nanoTime()
    val result = block // call-by-name
    val t1 = System.nanoTime()
    println(s"Elapsed time ($task): \t" + (t1 - t0) / 1e9 + "s")
    result
  }
}
