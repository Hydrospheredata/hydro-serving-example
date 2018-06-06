package example

import java.io.{File, PrintWriter}

import RRCF.{DataPoint, ForestParams, RRCF}
import akka.actor.ActorSystem
import akka.util.Timeout
import io.grpc.netty.{NettyChannelBuilder, NettyServerBuilder}
import io.hydrosphere.serving.tensorflow.TensorShape
import io.hydrosphere.serving.tensorflow.api.predict.PredictRequest
import io.hydrosphere.serving.tensorflow.api.prediction_service.PredictionServiceGrpc
import io.hydrosphere.serving.tensorflow.tensor.DoubleTensor

import scala.concurrent.ExecutionContext
import scala.concurrent.duration.FiniteDuration

object Main extends App {

  var counter: Long = 1

  override def main(args: Array[String]): Unit = {
  	val port = sys.env.get("APP_PORT").map(_.toInt).getOrElse(9090)

    val system = ActorSystem("HelloSystem")
    implicit val timeout = Timeout(FiniteDuration(30, "s"))
    val forestParams = ForestParams.loadParams()

    println(s"Forest: \n ${forestParams.toString} \n is starting.")

    val forestService = new ForestService(forestParams, system)
    val service = PredictionServiceGrpc.bindService(forestService, ExecutionContext.global)
    val server = NettyServerBuilder.forPort(port).addService(service).build()
    val x = server.start()
    println(s"Server started on port ${port}")
    x.awaitTermination()

    // val r = new scala.util.Random()
    // val channel = NettyChannelBuilder.forAddress("0.0.0.0", port).usePlaintext(true).build()
    // val client = PredictionServiceGrpc.blockingStub(channel)
    // var outlierFlag = false
    // var outlierCounter = 10

    // var sinCounter = 0.0

    // while (sinCounter < Double.MaxValue) {
    //   sinCounter += 0.1
    //   if ((r.nextDouble() >= 0.005) && !outlierFlag) {
    //     val normalScore = client.predict(PredictRequest(
    //       inputs = Map(
    //         "features" -> DoubleTensor(TensorShape.scalar, Seq(math.sin(sinCounter))).toProto
    //       )))
    //     println("Normal score", normalScore.outputs("score").doubleVal)

    //   } else {
    //     outlierFlag = true
    //     outlierCounter -= 1
    //     val anomalyScore = client.predict(PredictRequest(
    //       inputs = Map(
    //         "features" -> DoubleTensor(TensorShape.scalar, Seq(0.32)).toProto
    //       )))
    //     println("Anomaly score", anomalyScore.outputs("score").doubleVal)
    //     if (outlierCounter == 0) {
    //       outlierCounter = 10
    //       outlierFlag = false
    //     }
    //   }
    // }
  }

  def measureTime[R](task: String)(block: => R): R = {
    val t0 = System.nanoTime()
    val result = block // call-by-name
    val t1 = System.nanoTime()
    println(s"Elapsed time ($task): \t" + (t1 - t0) / 1e9 + "s")
    result
  }

  def periodicDataGenerator(): Array[Double] = {
    //        Array(2.0, 2.0)
    //    counter += 1
    val r = new scala.util.Random()
    if (r.nextBoolean()) Array(r.nextGaussian() / 2 + 10, r.nextGaussian() / 2 + 3)
    else Array(r.nextGaussian() / 2 - 6, r.nextGaussian() / 2 - 5, r.nextGaussian() / 2 + 5)
    //    Array(math.sin(counter))
  }

  def outlierDataGenerator(): Array[Double] = {
    //    counter += 1
    val r = new scala.util.Random()
    Array(r.nextGaussian() + 2, r.nextGaussian() - 1)
    //    Array(0.0)
    //    Array(math.cos(counter))
  }

}
