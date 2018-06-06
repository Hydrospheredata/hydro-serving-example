package example

import java.util.UUID

import RRCF.{DataPoint, ForestParams, RRCF}
import akka.actor.{Actor, ActorLogging, Props}
import io.hydrosphere.serving.tensorflow.TensorShape
import io.hydrosphere.serving.tensorflow.api.predict.{PredictRequest, PredictResponse}
import io.hydrosphere.serving.tensorflow.tensor.DoubleTensor

import scala.concurrent.{ExecutionContext, Future}

class ForestActor(val forestParams: ForestParams)(implicit val ec: ExecutionContext) extends Actor with ActorLogging {

  var pointsInBuffer = 0
  val requiredPoints = forestParams.samplesNum * forestParams.treesNum + forestParams.shingleSize
  val initBuffer = new Array[DataPoint](forestParams.samplesNum * forestParams.treesNum + forestParams.shingleSize)
  var randomForest: Option[RRCF] = None


  override def receive = {

    case datapoint: DataPoint =>
      val uuid = UUID.randomUUID()
      log.info(s"Request recieved: $uuid")
      val origin = sender()
      var score = -20.0
      randomForest match {
        case Some(forest) =>
          score = forest.recieve(datapoint)

        case None =>
          initBuffer(pointsInBuffer) = datapoint
          pointsInBuffer += 1
          if (pointsInBuffer == requiredPoints)
            randomForest = Some(new RRCF(forestParams, initBuffer))
          log.info(f"Forest is initializing: ${pointsInBuffer.toDouble / requiredPoints}%2.2f")
          score = -1 // Since forest is uninitialized for this point
      }

      log.info(s"Request ($uuid) response: $score")

      origin ! PredictResponse(
        outputs = Map(
          "score" -> DoubleTensor(TensorShape.scalar, Seq(score)).toProto
        )
      )
  }
}

object ForestActor {
  def props(forestParams: ForestParams)(implicit executionContext: ExecutionContext) = Props(new ForestActor(forestParams))
}
