package io.hydrosphere.rrcf

import akka.actor.{ActorRef, ActorSystem}
import akka.pattern.ask
import akka.util.Timeout
import io.hydrosphere.rrcf.impl.{DataPoint, ForestParams}
import io.hydrosphere.serving.contract.model_contract.ModelContract
import io.hydrosphere.serving.contract.model_field.ModelField
import io.hydrosphere.serving.contract.model_signature.ModelSignature
import io.hydrosphere.serving.tensorflow.types.DataType
import io.hydrosphere.serving.tensorflow.api.predict.{PredictRequest, PredictResponse}
import io.hydrosphere.serving.tensorflow.api.prediction_service.PredictionServiceGrpc.PredictionService

import scala.concurrent.Future

class ForestService(
  val forestParams: ForestParams,
  val modelContract: ModelContract
)(implicit val timeout: Timeout, val actorSystem: ActorSystem) extends PredictionService {
  import actorSystem._

  val signature: ModelSignature = modelContract.signatures.find(_.signatureName == "infer").getOrElse(throw new IllegalArgumentException("Can't find 'infer' signature in contract"))
  val input: ModelField = signature.inputs.find(_.name == "features").getOrElse(throw new IllegalArgumentException("Can't find 'features' input"))

  require(input.typeOrSubfields.isDtype, "RRCF only supports non-recursive types")
  val cType: DataType = input.typeOrSubfields.dtype.get
  require(cType == DataType.DT_DOUBLE, "RRCF expects 'feature' to be DT_DOUBLE")

  val forestActor: ActorRef = actorSystem.actorOf(ForestActor.props(forestParams))

  override def predict(request: PredictRequest): Future[PredictResponse] = {
    val inputs = request.inputs.getOrElse("features", throw new IllegalArgumentException("Can't find 'features' tensor"))
    require(inputs.dtype == cType, "Request type doesn't meet the contract")
    require(inputs.tensorShape == input.shape, "Request shape doesn't meet the contract")
    val datapoint = DataPoint(inputs.doubleVal.toArray)
    val f = forestActor ? datapoint
    f.mapTo[PredictResponse]
  }
}
