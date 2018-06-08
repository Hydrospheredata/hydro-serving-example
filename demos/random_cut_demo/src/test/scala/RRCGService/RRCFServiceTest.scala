package RRCGService

import java.util.concurrent.TimeUnit

import RRCF.ForestParams
import akka.actor.ActorSystem
import akka.util.Timeout
import example.ForestService
import io.grpc.netty.{NettyChannelBuilder, NettyServerBuilder}
import io.hydrosphere.serving.tensorflow.TensorShape
import io.hydrosphere.serving.tensorflow.api.predict.{PredictRequest, PredictResponse}
import io.hydrosphere.serving.tensorflow.api.prediction_service.PredictionServiceGrpc
import io.hydrosphere.serving.tensorflow.tensor.DoubleTensor
import org.scalatest.FunSuite

import scala.concurrent.ExecutionContext
import scala.concurrent.duration.FiniteDuration

class RRCFServiceTest extends FunSuite {
  test("sinCos") {
    val system = ActorSystem("HelloSystem")
    implicit val timeout = Timeout(FiniteDuration(30, "s"))
    val forestService = new ForestService(ForestParams(), 1, system)
    val service = PredictionServiceGrpc.bindService(forestService, ExecutionContext.global)
    val server = NettyServerBuilder.forPort(9080).addService(service).build()
    server.start()

    val channel = NettyChannelBuilder.forAddress("0.0.0.0", 9080).usePlaintext(true).build()
    val client = PredictionServiceGrpc.blockingStub(channel)

    var sinCounter = 0.0

    (1 until 100 * 100 + 100).foreach(_ => {
      client.predict(PredictRequest(
        inputs = Map(
          "features" -> DoubleTensor(TensorShape.scalar, Seq(math.sin(sinCounter))).toProto
        )))
      sinCounter += 0.1
    }
    )
    val normalScore = client.predict(PredictRequest(
      inputs = Map(
        "features" -> DoubleTensor(TensorShape.scalar, Seq(math.sin(sinCounter))).toProto
      )))

    val anomalyScore = client.predict(PredictRequest(
      inputs = Map(
        "features" -> DoubleTensor(TensorShape.scalar, Seq(math.cos(sinCounter))).toProto
      )))
    println("Normal score", normalScore.outputs("score").doubleVal)
    println("Anomaly score", anomalyScore.outputs("score").doubleVal)
    server.shutdown()
  }
}
