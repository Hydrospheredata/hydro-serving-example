package RRCF

import java.io.File
import java.lang.Exception

import io.circe._
import io.circe.generic.auto._
import io.circe.parser._
import io.circe.syntax._

import scala.io.Source

case class ForestParams(featuresNum: Int = 1, treesNum: Int = 100, samplesNum: Int = 100,
                        shingleSize: Int = 4, timeDecay: Long = 10000) {

  override def toString: String = s"featuresNum: $featuresNum; Number of trees: $treesNum; Samples per tree: $samplesNum; Shingle size: $shingleSize; Time-Decay: $timeDecay"
}

object ForestParams {
  def loadParams(name: String = "param.json"): ForestParams = {
    try {
      val paramFile = Source.fromFile(s"/model/files/$name")
      val forestParams = decode[ForestParams](paramFile.getLines().mkString("\n"))
      paramFile.close()
      forestParams match {
        case Left(_) => ForestParams()
        case Right(params) => params
      }
    } catch {
      case _ => ForestParams()
    }
  }
}
