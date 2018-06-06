package example

import RRCF.{DataPoint, ForestParams, RRCF}
import akka.actor.{ActorRef, ActorSystem, Props}
import io.hydrosphere.serving.onnx.onnx.TensorProto
import io.hydrosphere.serving.tensorflow.TensorShape
import io.hydrosphere.serving.tensorflow.api.predict.{PredictRequest, PredictResponse}
import io.hydrosphere.serving.tensorflow.api.prediction_service.PredictionServiceGrpc.PredictionService
import io.hydrosphere.serving.tensorflow.tensor.{DoubleTensor, TypedTensorFactory}
import io.hydrosphere.serving.tensorflow.types.DataType
import io.hydrosphere.serving.tensorflow.types.DataType.{DT_BFLOAT16, DT_BOOL, DT_COMPLEX128, DT_COMPLEX64, DT_DOUBLE, DT_FLOAT, DT_HALF, DT_INT16, DT_INT32, DT_INT64, DT_INT8, DT_INVALID, DT_MAP, DT_QINT16, DT_QINT32, DT_QINT8, DT_QUINT16, DT_QUINT8, DT_RESOURCE, DT_STRING, DT_UINT16, DT_UINT32, DT_UINT64, DT_UINT8, DT_VARIANT, Unrecognized}
import akka.pattern.ask
import akka.util.Timeout

import scala.concurrent.Future

class ForestService(val forestParams: ForestParams, val numberOfFeatures: Long, val actorSystem: ActorSystem)(implicit timeout: Timeout) extends PredictionService {
  import actorSystem._
  val forestActor: ActorRef = actorSystem.actorOf(ForestActor.props(forestParams))

  override def predict(request: PredictRequest): Future[PredictResponse] = {
    require(request.inputs.isDefinedAt("features"))
    val inputs = request.inputs.getOrElse("features", ???)
    require(inputs.dtype == DT_DOUBLE)
    require(inputs.doubleVal.length == numberOfFeatures)
    val datapoint = DataPoint(inputs.doubleVal.toArray)
    val f = forestActor ? datapoint
    f.mapTo[PredictResponse]
  }
}
