package io.hydrosphere.rrcf

import java.nio.file.{Files, Paths}

import akka.actor.ActorSystem
import akka.util.Timeout
import io.grpc.netty.NettyServerBuilder
import io.hydrosphere.rrcf.impl.ForestParams
import io.hydrosphere.serving.contract.model_contract.ModelContract
import io.hydrosphere.serving.tensorflow.api.prediction_service.PredictionServiceGrpc

import scala.concurrent.ExecutionContext
import scala.concurrent.duration.FiniteDuration

object Main extends App {
  val port = sys.env.get("APP_PORT").map(_.toInt).getOrElse(9090)
  val modelRoot = Paths.get("/model")

  implicit val timeout: Timeout = Timeout(FiniteDuration(30, "s"))
  implicit val system: ActorSystem = ActorSystem("HelloSystem")

  val contract = ModelContract.parseFrom(Files.readAllBytes(modelRoot.resolve("contract.protobin")))
  val forestParams = ForestParams.loadParams(modelRoot.resolve("files/params.json"))

  println(s"Forest: \n ${forestParams.toString} \n is starting.")

  val forestService = new ForestService(forestParams, contract)
  val service = PredictionServiceGrpc.bindService(forestService, ExecutionContext.global)
  val server = NettyServerBuilder.forPort(port).addService(service).build()

  val x = server.start()
  println(s"Server started on port $port")
  x.awaitTermination()
}
