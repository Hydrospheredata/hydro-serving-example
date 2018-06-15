package io.hydrosphere.rrcf.impl

import java.nio.file.{Files, Path}

import io.circe.generic.auto._
import io.circe.parser._

import scala.io.Source
import scala.util.control.NonFatal

case class ForestParams(
  treesNum: Int = 100,
  samplesNum: Int = 100,
  shingleSize: Int = 4,
  timeDecay: Long = 10000,
  warmupScore: Double = -1
) {
  override def toString: String = {
    s"Number of trees: $treesNum; Samples per tree: $samplesNum; Shingle size: $shingleSize; Time-Decay: $timeDecay"
  }

  def warmupPointsNum = samplesNum * treesNum + shingleSize
}

object ForestParams {
  def loadParams(path: Path): ForestParams = {
    if (Files.exists(path)) {
      val paramFile = Source.fromFile(path.toFile)
      try {
        val forestParams = decode[ForestParams](paramFile.getLines().mkString("\n"))
        forestParams.right.getOrElse(ForestParams())
      } catch {
        case NonFatal(_) => ForestParams()
      }
      finally {
        paramFile.close()
      }
    } else {
      ForestParams()
    }
  }
}
