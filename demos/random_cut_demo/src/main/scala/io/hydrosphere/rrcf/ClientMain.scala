package io.hydrosphere.rrcf

import io.grpc.netty.NettyChannelBuilder
import io.hydrosphere.serving.tensorflow.TensorShape
import io.hydrosphere.serving.tensorflow.api.predict.PredictRequest
import io.hydrosphere.serving.tensorflow.api.prediction_service.PredictionServiceGrpc
import io.hydrosphere.serving.tensorflow.tensor.DoubleTensor

object ClientMain extends App {
  val port = 9090
  val r = new scala.util.Random()
  val channel = NettyChannelBuilder.forAddress("0.0.0.0", port).usePlaintext().build()
  val client = PredictionServiceGrpc.blockingStub(channel)
  var outlierFlag = false
  var outlierCounter = 10

  var sinCounter = 0.0

  while (sinCounter < Double.MaxValue) {
    sinCounter += 0.1
    if ((r.nextDouble() >= 0.005) && !outlierFlag) {
      val normalScore = client.predict(PredictRequest(
        inputs = Map(
          "features" -> DoubleTensor(TensorShape.vector(-1), Seq(math.sin(sinCounter))).toProto
        )))
      println("Normal score", normalScore.outputs("score").doubleVal)

    } else {
      outlierFlag = true
      outlierCounter -= 1
      val anomalyScore = client.predict(PredictRequest(
        inputs = Map(
          "features" -> DoubleTensor(TensorShape.vector(-1), Seq(math.cos(sinCounter))).toProto
        )))
      println("Anomaly score", anomalyScore.outputs("score").doubleVal)
      if (outlierCounter == 0) {
        outlierCounter = 10
        outlierFlag = false
      }
    }
  }

  def measureTime[R](task: String)(block: => R): R = {
    val t0 = System.nanoTime()
    val result = block // call-by-name
    val t1 = System.nanoTime()
    println(s"Elapsed time ($task): \t" + (t1 - t0) / 1e9 + "s")
    result
  }

}
