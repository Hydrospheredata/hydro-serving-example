package io.hydrosphere.rrcf.impl

import java.nio.file.{Files, Path}

import io.circe.generic.auto._
import io.circe.parser._

import scala.io.Source
import scala.util.control.NonFatal

case class ForestParams(
  treesNum: Int = 300,
  samplesNum: Int = 300,
  shingleSize: Int = 2,
  timeDecay: Long = 1000,
  warmupScore: Double = -1
) {
  override def toString: String = {
    s"Number of trees: $treesNum; Samples per tree: $samplesNum; Shingle size: $shingleSize; Time-Decay: $timeDecay"
  }

  def warmupPointsNum = samplesNum + shingleSize - 1
}

object ForestParams {
  def loadParams(path: Path): ForestParams = {
    if (Files.exists(path)) {
      println(s"Loading from$path")
      val paramFile = Source.fromFile(path.toFile)
      try {
        val forestParams = decode[ForestParams](paramFile.getLines().mkString("\n"))
        forestParams.right.getOrElse(ForestParams())
      } catch {
        case NonFatal(ex) =>
          println(ex)
          ForestParams()
      }
      finally {
        paramFile.close()
      }
    } else {
      println(s"Cant find config at $path. Using default params")
      ForestParams()
    }
  }
}
