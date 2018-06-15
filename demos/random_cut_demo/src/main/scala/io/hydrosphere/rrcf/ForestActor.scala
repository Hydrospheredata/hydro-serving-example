package io.hydrosphere.rrcf

import java.util.UUID

import akka.actor.{Actor, ActorLogging, Props}
import io.hydrosphere.rrcf.impl.{DataPoint, ForestParams, RRCF}
import io.hydrosphere.serving.tensorflow.TensorShape
import io.hydrosphere.serving.tensorflow.api.predict.PredictResponse
import io.hydrosphere.serving.tensorflow.tensor.DoubleTensor

class ForestActor(val forestParams: ForestParams) extends Actor with ActorLogging {

  log.info("Warmup state for {} requests", forestParams.warmupPointsNum)
  /**
    * State of actor when it actually infers the forest.
    * No state transitions from here.
    * @param forest forest to infer from
    * @return
    */
  def infer(forest: RRCF): Receive = {
    case datapoint: DataPoint =>
      val origin = sender()
      val uuid = UUID.randomUUID()
      log.info(s"[{}] Request recieved", uuid)
      val score = forest.recieve(datapoint)
      log.info(s"[{}] Response: {}", uuid, score)
      origin ! wrapResult(score)
  }

  /**
    * State of actor, when it accumulates points and returns specified constant.
    * Changes context to `infer` when accumulated enough points.
    * @param buffer buffer with points
    * @return
    */
  def warmup(buffer: List[DataPoint]): Receive = {
    case datapoint: DataPoint =>
      val origin = sender()
      val uuid = UUID.randomUUID()
      log.info(s"[{}] Request recieved during warmup", uuid)
      val newBuffer = buffer :+ datapoint
      val warmupPercent =  ((newBuffer.length.toDouble / forestParams.warmupPointsNum.toDouble) * 100).formatted("%2.2f%%")
      log.info(f"[{}] Forest is initializing {}", uuid, warmupPercent)

      if (newBuffer.length >= forestParams.warmupPointsNum) {
        log.info(f"[{}] Warmed up", uuid)
        val forest = new RRCF(forestParams, buffer.toArray)
        log.info("[{}] Infer state", uuid)
        val score = forest.recieve(datapoint)
        log.info(s"[{}] Response: {}", uuid, score)
        origin ! wrapResult(score)
        context become infer(forest)
      } else {
        origin ! wrapResult(forestParams.warmupScore)
        context become warmup(newBuffer)
      }
  }

  /**
    * Initial state of actor is `warmup`
    * @return
    */
  override def receive: Receive = warmup(List.empty)

  private def wrapResult(score: Double): PredictResponse = {
    PredictResponse(
      outputs = Map(
        "score" -> DoubleTensor(TensorShape.scalar, Seq(score)).toProto
      )
    )
  }
}

object ForestActor {
  def props(forestParams: ForestParams) = Props(new ForestActor(forestParams))
}
