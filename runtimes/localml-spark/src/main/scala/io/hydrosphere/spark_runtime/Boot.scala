package io.hydrosphere.spark_runtime

import akka.actor.ActorSystem
import akka.http.scaladsl.Http
import akka.http.scaladsl.marshallers.sprayjson.SprayJsonSupport._
import akka.http.scaladsl.server.Directives._
import akka.stream.ActorMaterializer
import akka.util.Timeout
import ch.megard.akka.http.cors.CorsDirectives._
import ch.megard.akka.http.cors.CorsSettings
import io.hydrosphere.spark_ml_serving.common._
import scala.concurrent.duration._
import scala.util.Properties
import LocalPipelineModel._
import spray.json._
import akka.http.scaladsl.model.StatusCodes

/**
  * Created by Bulat on 19.05.2017.
  */
object Boot extends App {
  import SparkUtils._
  implicit val system = ActorSystem("ml_server")
  implicit val materializer = ActorMaterializer()
  implicit val ex = system.dispatcher
  implicit val timeout = Timeout(2.minutes)

  val pipelineModel = PipelineLoader.load("/model")
  println("Model loaded. Ready to serve.")

  pipelineModel.getStages.foreach(println)

  val addr = "0.0.0.0"
  val port = Properties.envOrElse("APP_HTTP_PORT", "9090").toInt

  val corsSettings = CorsSettings.defaultSettings

  val routes = cors(corsSettings) {
    get {
      path("health") {
        complete {
          "Hi"
        }
      }
    } ~
      post {
        path(Segment) { modelName =>
          import MapAnyJson._
          entity(as[List[Map[String, Any]]]) {
            case Nil =>
              println(s"Incoming request. Empty.")
              complete(StatusCodes.BadRequest)
            case mapList =>
              import SparkUtils._
              val inputKeys = mapList.head.keys.toList
              println(pipelineModel.inputCols)
              if (!inputKeys.containsSlice(pipelineModel.inputCols)) {
                println(s"Incoming request. No input columns detected.")
                complete(StatusCodes.BadRequest)
              } else {
                println(s"Incoming request. Params: $mapList")
                val columns = inputKeys.map { colName =>
                  val colData = mapList.map { row =>
                    row(colName)
                  }
                  LocalDataColumn(colName, colData)
                }
                val inputLDF = LocalData(columns)
                val result = pipelineModel.transform(inputLDF)
                complete {
                  val res = result.toMapList.asInstanceOf[List[Any]]
                  println(s"Results: $res")
                  res
                }
              }
          }
        }
      }
  }
  println(s"Running @ $addr:$port")
  Http().bindAndHandle(routes, addr, port)
}
