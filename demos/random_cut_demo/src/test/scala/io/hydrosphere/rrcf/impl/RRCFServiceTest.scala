package io.hydrosphere.rrcf.impl

import java.nio.file.{Files, Paths}

import akka.actor.ActorSystem
import akka.util.Timeout
import io.grpc.netty.{NettyChannelBuilder, NettyServerBuilder}
import io.hydrosphere.rrcf.ForestService
import io.hydrosphere.serving.contract.model_contract.ModelContract
import io.hydrosphere.serving.contract.model_field.ModelField
import io.hydrosphere.serving.contract.model_signature.ModelSignature
import io.hydrosphere.serving.tensorflow.TensorShape
import io.hydrosphere.serving.tensorflow.api.predict.PredictRequest
import io.hydrosphere.serving.tensorflow.api.prediction_service.PredictionServiceGrpc
import io.hydrosphere.serving.tensorflow.tensor.DoubleTensor
import org.scalatest.FunSpec

import scala.concurrent.ExecutionContext
import scala.concurrent.duration.FiniteDuration
import scala.collection.JavaConversions._

class RRCFServiceTest extends FunSpec {
  describe("RobustRandomCutForest service") {
    it("should parse param.json") {
      val param = ForestParams.loadParams(Paths.get(getClass.getResource("/model/param.json").toURI))
      assert(param.treesNum === 5)
      assert(param.samplesNum === 7)
      assert(param.shingleSize === 2)
      assert(param.timeDecay === 10000)
      assert(param.warmupScore === -69)
    }

    it("should detect anomalies in sin-cos transition scenario") {
      implicit val system: ActorSystem = ActorSystem("HelloSystem")
      implicit val timeout: Timeout = Timeout(FiniteDuration(30, "s"))

      val contract = ModelContract.fromAscii(
        Files.readAllLines(Paths.get(getClass.getResource("/model/contract.prototxt").toURI)).mkString("\n")
      )

      val param = ForestParams.loadParams(Paths.get(getClass.getResource("/model/param.json").toURI))

      val forestService = new ForestService(param, contract)
      val service = PredictionServiceGrpc.bindService(forestService, ExecutionContext.global)
      val server = NettyServerBuilder.forPort(9080).addService(service).build()
      server.start()

      val channel = NettyChannelBuilder.forAddress("0.0.0.0", 9080).usePlaintext().build()
      val client = PredictionServiceGrpc.blockingStub(channel)

      var sinCounter = 0.0

      (1 until forestService.forestParams.warmupPointsNum).foreach { _ =>
        client.predict(PredictRequest(
          inputs = Map(
            "features" -> DoubleTensor(TensorShape.scalar, Seq(math.sin(sinCounter))).toProto
          )))
        sinCounter += 0.1
      }

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
}
